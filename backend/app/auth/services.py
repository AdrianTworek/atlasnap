from typing import Optional

from fastapi import Depends, Request, status
from fastapi.exceptions import HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from fastapi_users import BaseUserManager, UUIDIDMixin
from fastapi_users.authentication import (
    AuthenticationBackend,
    BearerTransport,
    JWTStrategy,
)
from fastapi_users.db import SQLAlchemyUserDatabase
from fastapi_users import exceptions
from fastapi_users import models
from httpx_oauth.clients.google import GoogleOAuth2

from app.core.settings import settings
from app.core.database import get_user_db
from .models import User

SECRET = settings.jwt_secret.get_secret_value()


class UserManager(UUIDIDMixin, BaseUserManager):
    """User manager for fastapi-users."""

    reset_password_token_secret = SECRET
    verification_token_secret = SECRET

    async def authenticate(
        self, credentials: OAuth2PasswordRequestForm
    ) -> models.UP | None:
        """
        Authenticate and verify that the user is verified.
        """
        try:
            user = await self.get_by_email(credentials.username)
        except exceptions.UserNotExists:
            # Run the hasher to mitigate timing attack
            # Inspired from Django: https://code.djangoproject.com/ticket/20760
            self.password_helper.hash(credentials.password)
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="LOGIN_BAD_CREDENTIALS"
            )

        verified, updated_password_hash = self.password_helper.verify_and_update(
            credentials.password, user.hashed_password
        )
        if not verified:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED, detail="LOGIN_BAD_CREDENTIALS"
            )
        # Update password hash to a more robust one if needed
        if updated_password_hash is not None:
            await self.user_db.update(user, {"hashed_password": updated_password_hash})

        if not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="LOGIN_INACTIVE_USER"
            )

        if not user.is_verified:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN, detail="LOGIN_USER_NOT_VERIFIED"
            )

        return user

    async def on_after_register(self, user: User, request: Optional[Request] = None):
        """Called after user registration."""
        print(f"User {user.id} has registered.")

    async def on_after_forgot_password(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """Called after forgot password request."""
        print(f"User {user.id} has requested password reset. Token: {token}")

    async def on_after_request_verify(
        self, user: User, token: str, request: Optional[Request] = None
    ):
        """Called after request verification."""
        print(f"User {user.id} has requested verification. Token: {token}")

    async def on_after_update(
        self, user: User, update_dict: dict, request: Optional[Request] = None
    ):
        """Called after user update."""
        print(f"User {user.id} has been updated with {update_dict}.")


async def get_user_manager(user_db: SQLAlchemyUserDatabase = Depends(get_user_db)):
    """Get user manager."""
    yield UserManager(user_db)


bearer_transport = BearerTransport(tokenUrl="api/v1/auth/jwt/login")


def get_jwt_strategy() -> JWTStrategy:
    return JWTStrategy(
        secret=SECRET,
        lifetime_seconds=settings.jwt_lifetime_seconds,
    )


auth_backend = AuthenticationBackend(
    name="jwt", transport=bearer_transport, get_strategy=get_jwt_strategy
)

google_oauth_client = GoogleOAuth2(
    client_id=settings.google_client_id.get_secret_value(),
    client_secret=settings.google_client_secret.get_secret_value(),
    scopes=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
    ],
)
