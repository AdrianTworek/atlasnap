import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


from .models import Media
from .constants import MAX_MEDIA_UPLOADS_NUM


# Upload flow schemas
class UploadRequest(BaseModel):
    """Single file upload request."""

    filename: str = Field(..., min_length=1, max_length=255)
    content_type: str
    file_size: int = Field(..., gt=0)


class UploadResponse(BaseModel):
    """Presigned URL response."""

    upload_url: str
    key: str
    bucket: str
    expires_in: int = 3600


class BatchUploadRequest(BaseModel):
    """Batch upload request."""

    files: list[UploadRequest] = Field(..., max_length=MAX_MEDIA_UPLOADS_NUM)


class BatchUploadResponse(BaseModel):
    """Batch presigned URLs response."""

    uploads: list[UploadResponse]


class ConfirmUploadRequest(BaseModel):
    """Confirm single upload."""

    key: str
    original_filename: str
    content_type: str
    file_size: int


class BatchConfirmRequest(BaseModel):
    """Confirm batch uploads."""

    files: list[ConfirmUploadRequest] = Field(..., max_length=MAX_MEDIA_UPLOADS_NUM)


class BatchConfirmResponse(BaseModel):
    """Batch confirmation response."""

    created: int
    failed: int
    media_ids: list[uuid.UUID]


# Download flow schemas
class DownloadUrlResponse(BaseModel):
    """Download URL response."""

    url: str
    expires_in: int = 3600


# CRUD
class MediaUpdate(BaseModel):
    """Update media metadata."""

    description: Optional[str] = None
    user_tags: Optional[list[str]] = None
    is_favorite: Optional[bool] = None


class MediaRead(BaseModel):
    """Media response."""

    id: uuid.UUID
    user_id: uuid.UUID
    media_type: Media.Type
    status: Media.Status
    s3_key: str
    s3_bucket: str
    original_filename: str
    file_size: int
    mime_type: str
    user_tags: Optional[list[str]] = None
    description: Optional[str] = None
    is_favorite: bool
    created_at: datetime
    updated_at: datetime

    model_config = {"from_attributes": True}


class MediaList(BaseModel):
    """Paginated media list."""

    items: list[MediaRead]
    total: int
    page: int
    size: int
    pages: int
