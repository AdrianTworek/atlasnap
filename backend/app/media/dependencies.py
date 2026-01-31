from uuid import UUID

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import current_active_verified_user
from app.auth.models import User
from app.core.database import get_async_session
from .models import Media
from .services import MediaService


async def get_media_by_id(
    media_id: UUID,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_verified_user),
) -> Media:
    """Fetch media, ensuring ownership."""
    return await MediaService.get(session, media_id, user.id)
