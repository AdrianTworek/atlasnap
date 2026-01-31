import uuid
from enum import Enum
from typing import TYPE_CHECKING, Optional

from sqlalchemy import JSON, Boolean, ForeignKey, Enum as SQLEnum, Integer, String, Text
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import TimestampedBase

if TYPE_CHECKING:
    from app.auth.models import User


class Media(TimestampedBase):
    """Media model for storing photos and videos."""

    class Type(str, Enum):
        """Media type enum."""

        IMAGE = "image"
        VIDEO = "video"

    class Status(str, Enum):
        """Media status enum."""

        PENDING = "pending"
        PROCESSING = "processing"
        COMPLETED = "completed"
        FAILED = "failed"

    __tablename__ = "media"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True), primary_key=True, default=uuid.uuid4
    )

    # User relationship
    user_id: Mapped[uuid.UUID] = mapped_column(
        ForeignKey("user.id", ondelete="CASCADE"), nullable=False, index=True
    )
    user: Mapped["User"] = relationship("User", back_populates="media")

    # Media properties
    media_type: Mapped[Type] = mapped_column(SQLEnum(Type), nullable=False, index=True)
    status: Mapped[Status] = mapped_column(
        SQLEnum(Status), default=Status.PENDING, nullable=False, index=True
    )

    # S3 storage
    s3_key: Mapped[str] = mapped_column(String(500), nullable=False, unique=True)
    s3_bucket: Mapped[str] = mapped_column(String(255), nullable=False)
    original_filename: Mapped[str] = mapped_column(String(500), nullable=False)

    # File metadata
    file_size: Mapped[int] = mapped_column(Integer, nullable=False)
    mime_type: Mapped[str] = mapped_column(String(100), nullable=False)

    # User metadata
    user_tags: Mapped[Optional[list[str]]] = mapped_column(JSON, nullable=True)
    description: Mapped[Optional[str]] = mapped_column(Text, nullable=True)
    is_favorite: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
