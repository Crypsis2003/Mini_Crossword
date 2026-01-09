"""Friends router."""

import logging
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from app.database import get_db
from app.schemas.friend import (
    FriendRequestCreate,
    FriendRequestResponse,
    FriendResponse,
    FriendRequestAction,
    FriendsListResponse,
)
from app.services.friend_service import FriendService
from app.services.stats_service import StatsService
from app.services.user_service import UserService
from app.utils.auth import get_current_user
from app.models.user import User

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/friends", tags=["friends"])


@router.get("", response_model=FriendsListResponse)
def get_friends_list(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Get current user's friends and pending requests."""
    friend_service = FriendService(db)
    stats_service = StatsService(db)
    user_service = UserService(db)

    # Get friends with stats
    friends_with_since = friend_service.get_friends_with_since(current_user.id)
    friends = []
    for friend, friendship in friends_with_since:
        friend_stats = stats_service.get_user_stats(friend.id)
        friends.append(FriendResponse(
            id=friend.id,
            username=friend.username,
            since=friendship.created_at,
            total_solves=friend_stats["total_solves"],
            average_time_ms=friend_stats["average_time_ms"],
        ))

    # Get pending sent requests
    pending_sent = friend_service.get_pending_sent_requests(current_user.id)
    pending_sent_responses = []
    for req in pending_sent:
        receiver = user_service.get_by_id(req.receiver_id)
        pending_sent_responses.append(FriendRequestResponse(
            id=req.id,
            sender_id=req.sender_id,
            sender_username=current_user.username,
            receiver_id=req.receiver_id,
            receiver_username=receiver.username if receiver else "Unknown",
            status=req.status,
            created_at=req.created_at,
        ))

    # Get pending received requests
    pending_received = friend_service.get_pending_received_requests(current_user.id)
    pending_received_responses = []
    for req in pending_received:
        sender = user_service.get_by_id(req.sender_id)
        pending_received_responses.append(FriendRequestResponse(
            id=req.id,
            sender_id=req.sender_id,
            sender_username=sender.username if sender else "Unknown",
            receiver_id=req.receiver_id,
            receiver_username=current_user.username,
            status=req.status,
            created_at=req.created_at,
        ))

    return FriendsListResponse(
        friends=friends,
        pending_sent=pending_sent_responses,
        pending_received=pending_received_responses,
    )


@router.post("/request", response_model=FriendRequestResponse)
def send_friend_request(
    request_data: FriendRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Send a friend request to another user."""
    friend_service = FriendService(db)
    user_service = UserService(db)

    logger.info(f"User {current_user.username} sending friend request to {request_data.username}")

    friend_request = friend_service.send_friend_request(current_user, request_data.username)

    receiver = user_service.get_by_id(friend_request.receiver_id)

    return FriendRequestResponse(
        id=friend_request.id,
        sender_id=friend_request.sender_id,
        sender_username=current_user.username,
        receiver_id=friend_request.receiver_id,
        receiver_username=receiver.username if receiver else "Unknown",
        status=friend_request.status,
        created_at=friend_request.created_at,
    )


@router.post("/request/{request_id}/accept", response_model=FriendRequestResponse)
def accept_friend_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Accept a friend request."""
    friend_service = FriendService(db)
    user_service = UserService(db)

    logger.info(f"User {current_user.username} accepting friend request {request_id}")

    friend_request = friend_service.accept_friend_request(request_id, current_user)

    sender = user_service.get_by_id(friend_request.sender_id)

    return FriendRequestResponse(
        id=friend_request.id,
        sender_id=friend_request.sender_id,
        sender_username=sender.username if sender else "Unknown",
        receiver_id=friend_request.receiver_id,
        receiver_username=current_user.username,
        status=friend_request.status,
        created_at=friend_request.created_at,
    )


@router.post("/request/{request_id}/reject", response_model=FriendRequestResponse)
def reject_friend_request(
    request_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Reject a friend request."""
    friend_service = FriendService(db)
    user_service = UserService(db)

    logger.info(f"User {current_user.username} rejecting friend request {request_id}")

    friend_request = friend_service.reject_friend_request(request_id, current_user)

    sender = user_service.get_by_id(friend_request.sender_id)

    return FriendRequestResponse(
        id=friend_request.id,
        sender_id=friend_request.sender_id,
        sender_username=sender.username if sender else "Unknown",
        receiver_id=friend_request.receiver_id,
        receiver_username=current_user.username,
        status=friend_request.status,
        created_at=friend_request.created_at,
    )


@router.delete("/{friend_id}")
def remove_friend(
    friend_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Remove a friend."""
    friend_service = FriendService(db)

    if not friend_service.are_friends(current_user.id, friend_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Friend not found",
        )

    logger.info(f"User {current_user.username} removing friend {friend_id}")

    friend_service.remove_friend(current_user.id, friend_id)

    return {"message": "Friend removed successfully"}


@router.get("/search")
def search_users(
    q: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """Search for users to add as friends."""
    if len(q) < 2:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Search query must be at least 2 characters",
        )

    user_service = UserService(db)
    friend_service = FriendService(db)

    users = user_service.search_users(q, limit=10)

    # Exclude current user and get friendship status
    results = []
    for user in users:
        if user.id == current_user.id:
            continue

        is_friend = friend_service.are_friends(current_user.id, user.id)
        has_pending = friend_service.get_pending_request(current_user.id, user.id) is not None

        results.append({
            "id": user.id,
            "username": user.username,
            "is_friend": is_friend,
            "has_pending_request": has_pending,
        })

    return results
