from datetime import datetime
import uuid

from fastapi_users import schemas


class UserRead(schemas.BaseUser[uuid.UUID]):
    avatar_url: str | None
    created_at: datetime
    updated_at: datetime


class UserCreate(schemas.BaseUserCreate):
    pass


class UserUpdate(schemas.BaseUserUpdate):
    pass
