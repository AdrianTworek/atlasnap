from fastapi_users.db import SQLAlchemyBaseUserTableUUID

from app.core.database import TimestampedBase


class User(SQLAlchemyBaseUserTableUUID, TimestampedBase):
    """User model."""

    __tablename__ = "users"
