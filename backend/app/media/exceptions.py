from uuid import UUID


class MediaError(Exception):
    """Base exception for media."""


class MediaNotFound(MediaError):
    """Media does not exist or user doesn't have access to it."""

    def __init__(self, media_id: UUID):
        self.media_id = media_id
        super().__init__(f"Media with ID {media_id} not found")


class UnsupportedMediaType(MediaError):
    """Content type not allowed."""

    def __init__(self, content_type: str):
        self.content_type = content_type
        super().__init__(f"Unsupported content type: {content_type}")


class FileTooLarge(MediaError):
    """File exceeds size limit."""

    def __init__(self, max_mb: int):
        self.max_mb = max_mb
        super().__init__(f"File exceeds {max_mb}MB limit")
