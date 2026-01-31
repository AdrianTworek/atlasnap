from typing import Optional
import uuid
from datetime import datetime

import boto3
from botocore.config import Config
from botocore.exceptions import ClientError

from app.core.settings import settings


class S3Service:
    """Service for S3 operations."""

    def __init__(self):
        self._client: boto3.client | None = None

    @property
    def client(self):
        """Lazy initialization of the S3 client."""
        if self._client is None:
            self._client = boto3.client(
                "s3",
                aws_access_key_id=settings.aws_access_key_id.get_secret_value(),
                aws_secret_access_key=settings.aws_secret_access_key.get_secret_value(),
                region_name=settings.aws_region,
                endpoint_url=settings.s3_endpoint_url,
                config=Config(signature_version="s3v4"),
            )
        return self._client

    def generate_upload_key(self, user_id: uuid.UUID, filename: str) -> str:
        """Generate a unique S3 key for upload."""
        ext = filename.rsplit(".", 1)[-1] if "." in filename else ""
        timestamp = datetime.utcnow().strftime("%Y/%m/%d")
        unique_id = uuid.uuid4().hex[:8]
        return f"media/{user_id}/{timestamp}/{unique_id}.{ext}"

    def generate_thumbnail_key(self, original_key: str) -> str:
        """Generate thumbnail key from original key."""
        return original_key.replace("media/", "thumbnails/", 1)

    def create_presigned_upload_url(
        self, key: str, content_type: str, expires_in: int = 3600
    ) -> str:
        """Create a presigned upload URL for uploading to S3."""
        try:
            return self.client.generate_presigned_url(
                "put_object",
                Params={
                    "Bucket": settings.s3_bucket_name,
                    "Key": key,
                    "ContentType": content_type,
                },
                ExpiresIn=expires_in,
            )
        except ClientError as e:
            raise RuntimeError(f"Failed to create presigned upload URL: {e}")

    def create_presigned_download_url(
        self, key: str, expires_in: int = 3600, filename: str | None = None
    ) -> str:
        """Create a presigned download URL for downloading from S3."""
        params = {
            "Bucket": settings.s3_bucket_name,
            "Key": key,
        }

        if filename:
            params["ResponseContentDisposition"] = f"attachment; filename={filename}"

        try:
            return self.client.generate_presigned_url(
                "get_object",
                Params=params,
                ExpiresIn=expires_in,
            )
        except ClientError as e:
            raise RuntimeError(f"Failed to create presigned download URL: {e}")

    def delete_object(self, key: str) -> bool:
        """Delete an object from S3."""
        try:
            self.client.delete_object(Bucket=settings.s3_bucket_name, Key=key)
            return True
        except ClientError:
            return False

    def delete_objects(self, keys: list[str]) -> bool:
        """Delete multiple objects from S3."""
        if not keys:
            return True

        try:
            self.client.delete_objects(
                Bucket=settings.s3_bucket_name,
                Delete={"Objects": [{"Key": key} for key in keys]},
            )
            return True
        except ClientError:
            return False

    def head_object(self, key: str) -> Optional[dict]:
        """Get object metadata without downloading."""
        try:
            response = self.client.head_object(Bucket=settings.s3_bucket_name, Key=key)
            return {
                "content_type": response.get("ContentType"),
                "content_length": response.get("ContentLength"),
                "last_modified": response.get("LastModified"),
                "etag": response.get("ETag"),
            }
        except ClientError:
            return None


s3_service = S3Service()
