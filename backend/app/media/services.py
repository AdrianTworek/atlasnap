from uuid import UUID

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.settings import settings
from app.core.aws.s3 import s3_service
from app.auth.models import User
from .exceptions import FileTooLarge, MediaNotFound, UnsupportedMediaType
from .models import Media
from .schemas import (
    BatchConfirmRequest,
    BatchConfirmResponse,
    BatchUploadRequest,
    BatchUploadResponse,
    DownloadUrlResponse,
    MediaUpdate,
    UploadResponse,
)


def get_media_type(content_type: str) -> Media.Type:
    """Determine media type from MIME type."""
    if content_type in settings.allowed_image_types:
        return Media.Type.IMAGE
    if content_type in settings.allowed_video_types:
        return Media.Type.VIDEO
    raise UnsupportedMediaType(content_type)


def validate_upload(content_type: str, file_size: int) -> None:
    """Validate file before upload."""
    allowed = settings.allowed_image_types + settings.allowed_video_types
    if content_type not in allowed:
        raise UnsupportedMediaType(content_type)

    max_bytes = settings.max_upload_size_mb * 1024 * 1024
    if file_size > max_bytes:
        raise FileTooLarge(settings.max_upload_size_mb)


class MediaService:
    """Service for media operations."""

    @staticmethod
    def generate_upload_urls(
        user: User, request: BatchUploadRequest
    ) -> BatchUploadResponse:
        """Generate presigned URLs for batch upload."""
        uploads = []
        for file in request.files:
            validate_upload(file.content_type, file.file_size)

            key = s3_service.generate_upload_key(user.id, file.filename)
            url = s3_service.create_presigned_upload_url(key, file.content_type)

            uploads.append(
                UploadResponse(upload_url=url, key=key, bucket=settings.s3_bucket_name)
            )

        return BatchUploadResponse(uploads=uploads)

    @staticmethod
    async def confirm_uploads(
        session: AsyncSession, user: User, request: BatchConfirmRequest
    ) -> BatchConfirmResponse:
        """Confirm uploads and create media records."""
        media_ids: list[UUID] = []
        failed = 0

        for file in request.files:
            try:
                media = Media(
                    user_id=user.id,
                    media_type=get_media_type(file.content_type),
                    status=Media.Status.PENDING,
                    s3_key=file.key,
                    s3_bucket=settings.s3_bucket_name,
                    original_filename=file.original_filename,
                    file_size=file.file_size,
                    mime_type=file.content_type,
                )
                session.add(media)
                await session.flush()
                media_ids.append(media.id)
            except Exception:
                failed += 1

        await session.commit()
        return BatchConfirmResponse(
            created=len(media_ids), failed=failed, media_ids=media_ids
        )

    @staticmethod
    def get_download_url(media: Media, expires_in: int = 3600) -> DownloadUrlResponse:
        """Get download URL for media."""
        url = s3_service.create_presigned_download_url(
            media.s3_key, filename=media.original_filename
        )
        return DownloadUrlResponse(url=url, expires_in=expires_in)

    @staticmethod
    async def list(
        session: AsyncSession,
        user_id: UUID,
        media_type: Media.Type | None = None,
        status: Media.Status | None = None,
        is_favorite: bool | None = None,
        page: int = 1,
        size: int = 20,
    ) -> tuple[list[Media], int]:
        """List media for a user with filters."""
        query = select(Media).where(Media.user_id == user_id)

        if media_type:
            query = query.where(Media.media_type == media_type)
        if status:
            query = query.where(Media.status == status)
        if is_favorite is not None:
            query = query.where(Media.is_favorite == is_favorite)

        count_result = await session.execute(
            select(func.count()).select_from(query.subquery())
        )
        total = count_result.scalar_one()

        query = (
            query.order_by(Media.created_at.desc())
            .offset((page - 1) * size)
            .limit(size)
        )

        result = await session.execute(query)
        return list(result.scalars().all()), total

    @staticmethod
    async def get(session: AsyncSession, media_id: UUID, user_id: UUID) -> Media:
        """Get a media by ID for user."""
        result = await session.execute(
            select(Media).where(Media.id == media_id, Media.user_id == user_id)
        )
        media = result.scalar_one_or_none()
        if not media:
            raise MediaNotFound(media_id)
        return media

    @staticmethod
    async def update(session: AsyncSession, media: Media, data: MediaUpdate) -> Media:
        """Update media metadata."""
        for field, value in data.model_dump(exclude_unset=True).items():
            setattr(media, field, value)
        await session.commit()
        await session.refresh(media)
        return media

    @staticmethod
    async def delete(session: AsyncSession, media: Media) -> None:
        """Delete media and S3 object."""
        s3_service.delete_object(media.s3_key)
        await session.delete(media)
        await session.commit()
