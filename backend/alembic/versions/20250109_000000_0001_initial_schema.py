"""Initial schema

Revision ID: 0001
Revises:
Create Date: 2025-01-09 00:00:00.000000

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0001'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # Create users table
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('username', sa.String(50), nullable=False),
        sa.Column('email', sa.String(255), nullable=False),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('is_active', sa.Boolean(), default=True),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_users_id', 'users', ['id'], unique=False)
    op.create_index('ix_users_username', 'users', ['username'], unique=True)
    op.create_index('ix_users_email', 'users', ['email'], unique=True)

    # Create puzzles table
    op.create_table(
        'puzzles',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('title', sa.String(255), nullable=False),
        sa.Column('size', sa.Integer(), nullable=False),
        sa.Column('grid', sa.Text(), nullable=False),
        sa.Column('solution', sa.Text(), nullable=False),
        sa.Column('clues_across', sa.Text(), nullable=False),
        sa.Column('clues_down', sa.Text(), nullable=False),
        sa.Column('scheduled_date', sa.Date(), nullable=True),
        sa.Column('difficulty', sa.String(20), default='medium'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index('ix_puzzles_id', 'puzzles', ['id'], unique=False)
    op.create_index('ix_puzzles_scheduled_date', 'puzzles', ['scheduled_date'], unique=True)

    # Create solves table
    op.create_table(
        'solves',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('puzzle_id', sa.Integer(), nullable=False),
        sa.Column('time_ms', sa.Integer(), nullable=False),
        sa.Column('completed_at', sa.DateTime(), nullable=True),
        sa.Column('is_completed', sa.Boolean(), default=True),
        sa.Column('attempt_count', sa.Integer(), default=1),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['puzzle_id'], ['puzzles.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'puzzle_id', name='unique_user_puzzle_solve'),
    )
    op.create_index('ix_solves_id', 'solves', ['id'], unique=False)
    op.create_index('ix_solves_user_id', 'solves', ['user_id'], unique=False)
    op.create_index('ix_solves_puzzle_id', 'solves', ['puzzle_id'], unique=False)

    # Create friend_requests table
    op.create_table(
        'friend_requests',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('sender_id', sa.Integer(), nullable=False),
        sa.Column('receiver_id', sa.Integer(), nullable=False),
        sa.Column('status', sa.String(20), default='pending'),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.Column('updated_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['sender_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['receiver_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('sender_id', 'receiver_id', name='unique_friend_request'),
    )
    op.create_index('ix_friend_requests_id', 'friend_requests', ['id'], unique=False)
    op.create_index('ix_friend_requests_sender_id', 'friend_requests', ['sender_id'], unique=False)
    op.create_index('ix_friend_requests_receiver_id', 'friend_requests', ['receiver_id'], unique=False)

    # Create friendships table
    op.create_table(
        'friendships',
        sa.Column('id', sa.Integer(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.Column('friend_id', sa.Integer(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['friend_id'], ['users.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('user_id', 'friend_id', name='unique_friendship'),
    )
    op.create_index('ix_friendships_id', 'friendships', ['id'], unique=False)
    op.create_index('ix_friendships_user_id', 'friendships', ['user_id'], unique=False)
    op.create_index('ix_friendships_friend_id', 'friendships', ['friend_id'], unique=False)


def downgrade() -> None:
    op.drop_table('friendships')
    op.drop_table('friend_requests')
    op.drop_table('solves')
    op.drop_table('puzzles')
    op.drop_table('users')
