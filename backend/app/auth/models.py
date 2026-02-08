from typing import TYPE_CHECKING, Optional

from fastapi_users_db_sqlalchemy import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
)
import sqlalchemy as sa
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.core.database import Base, TimestampedBase

if TYPE_CHECKING:
    from app.media.models import Media


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, TimestampedBase):
    """User model."""

    # User properties
    avatar_url: Mapped[Optional[str]] = mapped_column(sa.String(500), nullable=True)

    # Auth
    has_password: Mapped[bool] = mapped_column(
        sa.Boolean, default=True, server_default=sa.text("true"), nullable=False
    )
    oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )

    # Relationships
    media: Mapped[list["Media"]] = relationship(
        "Media", back_populates="user", cascade="all, delete-orphan"
    )
