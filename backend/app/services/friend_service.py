"""Friend service for friend-related business logic."""

from typing import Optional

from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import or_, and_

from app.models.user import User
from app.models.friend import FriendRequest, Friendship


class FriendService:
    """Service class for friend operations."""

    def __init__(self, db: Session):
        self.db = db

    def get_friend_request(self, request_id: int) -> Optional[FriendRequest]:
        """Get friend request by ID."""
        return self.db.query(FriendRequest).filter(FriendRequest.id == request_id).first()

    def get_pending_request(self, sender_id: int, receiver_id: int) -> Optional[FriendRequest]:
        """Get pending friend request between two users."""
        return (
            self.db.query(FriendRequest)
            .filter(
                FriendRequest.sender_id == sender_id,
                FriendRequest.receiver_id == receiver_id,
                FriendRequest.status == "pending",
            )
            .first()
        )

    def are_friends(self, user_id: int, other_user_id: int) -> bool:
        """Check if two users are friends."""
        friendship = (
            self.db.query(Friendship)
            .filter(
                Friendship.user_id == user_id,
                Friendship.friend_id == other_user_id,
            )
            .first()
        )
        return friendship is not None

    def send_friend_request(self, sender: User, receiver_username: str) -> FriendRequest:
        """Send a friend request to another user."""
        # Find receiver by username
        receiver = (
            self.db.query(User)
            .filter(User.username == receiver_username.lower())
            .first()
        )

        if not receiver:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found",
            )

        if receiver.id == sender.id:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Cannot send friend request to yourself",
            )

        # Check if already friends
        if self.are_friends(sender.id, receiver.id):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Already friends with this user",
            )

        # Check for existing pending request (in either direction)
        existing_request = (
            self.db.query(FriendRequest)
            .filter(
                or_(
                    and_(
                        FriendRequest.sender_id == sender.id,
                        FriendRequest.receiver_id == receiver.id,
                    ),
                    and_(
                        FriendRequest.sender_id == receiver.id,
                        FriendRequest.receiver_id == sender.id,
                    ),
                ),
                FriendRequest.status == "pending",
            )
            .first()
        )

        if existing_request:
            # If there's a pending request from the other user, accept it
            if existing_request.sender_id == receiver.id:
                return self.accept_friend_request(existing_request.id, sender)

            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Friend request already pending",
            )

        # Create new friend request
        friend_request = FriendRequest(
            sender_id=sender.id,
            receiver_id=receiver.id,
            status="pending",
        )

        self.db.add(friend_request)
        self.db.commit()
        self.db.refresh(friend_request)

        return friend_request

    def accept_friend_request(self, request_id: int, user: User) -> FriendRequest:
        """Accept a friend request."""
        friend_request = self.get_friend_request(request_id)

        if not friend_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Friend request not found",
            )

        if friend_request.receiver_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot accept this friend request",
            )

        if friend_request.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Friend request is not pending",
            )

        # Update request status
        friend_request.status = "accepted"

        # Create bidirectional friendship
        friendship1 = Friendship(
            user_id=friend_request.sender_id,
            friend_id=friend_request.receiver_id,
        )
        friendship2 = Friendship(
            user_id=friend_request.receiver_id,
            friend_id=friend_request.sender_id,
        )

        self.db.add(friendship1)
        self.db.add(friendship2)
        self.db.commit()
        self.db.refresh(friend_request)

        return friend_request

    def reject_friend_request(self, request_id: int, user: User) -> FriendRequest:
        """Reject a friend request."""
        friend_request = self.get_friend_request(request_id)

        if not friend_request:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Friend request not found",
            )

        if friend_request.receiver_id != user.id:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Cannot reject this friend request",
            )

        if friend_request.status != "pending":
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Friend request is not pending",
            )

        friend_request.status = "rejected"
        self.db.commit()
        self.db.refresh(friend_request)

        return friend_request

    def get_friends(self, user_id: int) -> list[User]:
        """Get all friends of a user."""
        friendships = (
            self.db.query(Friendship)
            .filter(Friendship.user_id == user_id)
            .all()
        )

        friend_ids = [f.friend_id for f in friendships]
        return self.db.query(User).filter(User.id.in_(friend_ids)).all()

    def get_friends_with_since(self, user_id: int) -> list[tuple[User, Friendship]]:
        """Get all friends with friendship creation date."""
        friendships = (
            self.db.query(Friendship, User)
            .join(User, Friendship.friend_id == User.id)
            .filter(Friendship.user_id == user_id)
            .all()
        )
        return [(user, friendship) for friendship, user in friendships]

    def get_pending_sent_requests(self, user_id: int) -> list[FriendRequest]:
        """Get pending friend requests sent by user."""
        return (
            self.db.query(FriendRequest)
            .filter(
                FriendRequest.sender_id == user_id,
                FriendRequest.status == "pending",
            )
            .all()
        )

    def get_pending_received_requests(self, user_id: int) -> list[FriendRequest]:
        """Get pending friend requests received by user."""
        return (
            self.db.query(FriendRequest)
            .filter(
                FriendRequest.receiver_id == user_id,
                FriendRequest.status == "pending",
            )
            .all()
        )

    def remove_friend(self, user_id: int, friend_id: int) -> bool:
        """Remove a friend (unfriend)."""
        # Delete both directions of friendship
        self.db.query(Friendship).filter(
            or_(
                and_(Friendship.user_id == user_id, Friendship.friend_id == friend_id),
                and_(Friendship.user_id == friend_id, Friendship.friend_id == user_id),
            )
        ).delete()

        self.db.commit()
        return True
