"""Friend-related Pydantic schemas."""

from datetime import datetime
from typing import Optional
from enum import Enum

from pydantic import BaseModel


class FriendRequestStatus(str, Enum):
    """Friend request status enum."""

    PENDING = "pending"
    ACCEPTED = "accepted"
    REJECTED = "rejected"


class FriendRequestCreate(BaseModel):
    """Schema for creating a friend request."""

    username: str  # Username of the person to add


class FriendRequestAction(BaseModel):
    """Schema for accepting/rejecting a friend request."""

    request_id: int
    action: str  # "accept" or "reject"


class FriendRequestResponse(BaseModel):
    """Schema for friend request response."""

    id: int
    sender_id: int
    sender_username: str
    receiver_id: int
    receiver_username: str
    status: str
    created_at: datetime

    model_config = {"from_attributes": True}


class FriendResponse(BaseModel):
    """Schema for friend response."""

    id: int
    username: str
    since: datetime  # When friendship was established
    total_solves: Optional[int] = 0
    average_time_ms: Optional[int] = None

    model_config = {"from_attributes": True}


class FriendsListResponse(BaseModel):
    """Schema for friends list response."""

    friends: list[FriendResponse]
    pending_sent: list[FriendRequestResponse]
    pending_received: list[FriendRequestResponse]
