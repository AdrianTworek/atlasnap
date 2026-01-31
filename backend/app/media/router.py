from fastapi import APIRouter, Depends, Query, Response, status

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.dependencies import current_active_verified_user
from app.auth.models import User
from app.core.database import get_async_session
from .models import Media

from .services import MediaService
from .dependencies import get_media_by_id
from .schemas import (
    BatchConfirmRequest,
    BatchConfirmResponse,
    BatchUploadRequest,
    BatchUploadResponse,
    DownloadUrlResponse,
    MediaList,
    MediaRead,
    MediaUpdate,
)

router = APIRouter()


@router.post("/upload/urls", response_model=BatchUploadResponse)
def get_upload_urls(
    request: BatchUploadRequest,
    user: User = Depends(current_active_verified_user),
):
    """Generate presigned URLs for uploading files."""
    return MediaService.generate_upload_urls(user, request)


@router.post("/upload/confirm", response_model=BatchConfirmResponse)
async def confirm_uploads(
    request: BatchConfirmRequest,
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_verified_user),
):
    """Confirm uploads after files are uploaded to S3."""
    return await MediaService.confirm_uploads(session, user, request)


@router.get("/{media_id}/download-url", response_model=DownloadUrlResponse)
async def get_download_url(
    media: Media = Depends(get_media_by_id),
):
    """Get download URL for media."""
    return MediaService.get_download_url(media)


@router.get("", response_model=MediaList)
async def list_media(
    media_type: Media.Type | None = Query(None),
    status: Media.Status | None = Query(None),
    is_favorite: bool | None = Query(None),
    page: int = Query(1, ge=1),
    size: int = Query(20, ge=1, le=100),
    session: AsyncSession = Depends(get_async_session),
    user: User = Depends(current_active_verified_user),
):
    """List user's media with filters."""
    items, total = await MediaService.list(
        session, user.id, media_type, status, is_favorite, page, size
    )
    pages = (total + size - 1) // size if total else 0

    return MediaList(
        items=[MediaRead.model_validate(m) for m in items],
        total=total,
        page=page,
        size=size,
        pages=pages,
    )


@router.get("/{media_id}", response_model=MediaRead)
async def get_media(media: Media = Depends(get_media_by_id)):
    """Get single media by ID."""
    return MediaRead.model_validate(media)


@router.patch("/{media_id}", response_model=MediaRead)
async def update_media(
    data: MediaUpdate,
    media: Media = Depends(get_media_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    """Update media metadata."""
    updated = await MediaService.update(session, media, data)
    return MediaRead.model_validate(updated)


@router.delete("/{media_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_media(
    media: Media = Depends(get_media_by_id),
    session: AsyncSession = Depends(get_async_session),
):
    """Delete media."""
    await MediaService.delete(session, media)
    return Response(status_code=status.HTTP_204_NO_CONTENT)
