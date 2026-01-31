from typing import TYPE_CHECKING

from fastapi_users.db import (
    SQLAlchemyBaseOAuthAccountTableUUID,
    SQLAlchemyBaseUserTableUUID,
)
from sqlalchemy.orm import Mapped, relationship

from app.core.database import Base, TimestampedBase

if TYPE_CHECKING:
    from app.media.models import Media


class OAuthAccount(SQLAlchemyBaseOAuthAccountTableUUID, Base):
    pass


class User(SQLAlchemyBaseUserTableUUID, TimestampedBase):
    """User model."""

    oauth_accounts: Mapped[list[OAuthAccount]] = relationship(
        "OAuthAccount", lazy="joined"
    )

    media: Mapped[list["Media"]] = relationship(
        "Media", back_populates="user", cascade="all, delete-orphan"
    )
