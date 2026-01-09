"""Friend relationship models."""

from datetime import datetime
from sqlalchemy import Column, Integer, DateTime, ForeignKey, String, UniqueConstraint
from sqlalchemy.orm import relationship

from app.database import Base


class FriendRequest(Base):
    """Friend request model for pending requests."""

    __tablename__ = "friend_requests"

    id = Column(Integer, primary_key=True, index=True)
    sender_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    receiver_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    status = Column(String(20), default="pending")  # pending, accepted, rejected
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relationships
    sender = relationship("User", foreign_keys=[sender_id], back_populates="sent_friend_requests")
    receiver = relationship("User", foreign_keys=[receiver_id], back_populates="received_friend_requests")

    # Prevent duplicate requests
    __table_args__ = (
        UniqueConstraint("sender_id", "receiver_id", name="unique_friend_request"),
    )

    def __repr__(self):
        return f"<FriendRequest(sender={self.sender_id}, receiver={self.receiver_id}, status={self.status})>"


class Friendship(Base):
    """Bidirectional friendship model (created when request is accepted)."""

    __tablename__ = "friendships"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    friend_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)

    # Ensure unique friendships
    __table_args__ = (
        UniqueConstraint("user_id", "friend_id", name="unique_friendship"),
    )

    def __repr__(self):
        return f"<Friendship(user_id={self.user_id}, friend_id={self.friend_id})>"
