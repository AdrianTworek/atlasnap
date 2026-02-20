import secrets
from fastapi import APIRouter, Depends, Query
from fastapi.responses import RedirectResponse
from fastapi.routing import APIRoute
from fastapi_users.password import PasswordHelper
from fastapi_users_db_sqlalchemy import SQLAlchemyUserDatabase
from sqlalchemy.ext.asyncio import AsyncSession

from .models import User, OAuthAccount
from .schemas import UserRead, UserCreate, UserUpdate
from .dependencies import fastapi_users
from .services import (
    auth_backend,
    fetch_google_profile,
    get_jwt_strategy,
    google_oauth_client,
)

from app.core.settings import settings
from app.core.database import get_async_session
from app.core.limiter import limiter

SECRET = settings.jwt_secret.get_secret_value()


def apply_rate_limit(router, path: str, method: str, limit_str: str):
    """Apply rate limit to fastapi-users auth routes."""
    for route in router.routes:
        if (
            isinstance(route, APIRoute)
            and route.path == path
            and method.upper() in route.methods
        ):
            route.endpoint = limiter.limit(limit_str)(route.endpoint)


router = APIRouter()

# Login
login_router = fastapi_users.get_auth_router(auth_backend)
apply_rate_limit(login_router, "/login", "POST", "5/minute")
router.include_router(
    login_router,
    prefix="/jwt",
    tags=["auth"],
)

# Register
register_router = fastapi_users.get_register_router(UserRead, UserCreate)
apply_rate_limit(register_router, "/register", "POST", "5/day")
router.include_router(
    register_router,
    tags=["auth"],
)

# Reset password
reset_password_router = fastapi_users.get_reset_password_router()
apply_rate_limit(reset_password_router, "/reset-password", "POST", "5/hour")
apply_rate_limit(reset_password_router, "/forgot-password", "POST", "5/hour")
router.include_router(
    reset_password_router,
    tags=["auth"],
)

# Verify
verify_router = fastapi_users.get_verify_router(UserRead)
apply_rate_limit(verify_router, "/request-verify-token", "POST", "5/hour")
apply_rate_limit(verify_router, "/verify", "POST", "5/hour")
router.include_router(
    verify_router,
    tags=["auth"],
)

# Users
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
    tags=["auth"],
)

# Google OAuth
router.include_router(
    fastapi_users.get_oauth_router(
        google_oauth_client,
        auth_backend,
        SECRET,
        associate_by_email=True,
        is_verified_by_default=True,
        redirect_url=settings.google_redirect_url,
    ),
    prefix="/google",
    tags=["oauth"],
)


@router.get("/google/callback/redirect")
async def google_callback_redirect(
    code: str = Query(...),
    state: str | None = Query(None),
    error: str | None = Query(None),
    session: AsyncSession = Depends(get_async_session),
):
    if error:
        return RedirectResponse(
            url=f"{settings.google_frontend_redirect_url}?error={error}",
            status_code=302,
        )

    # Exchange code for Google access token
    access_token_response = await google_oauth_client.get_access_token(
        code, settings.google_redirect_url
    )
    google_access_token = access_token_response["access_token"]

    # Fetch Google user
    google_id, email = await google_oauth_client.get_id_email(google_access_token)

    # Fetch Google profile
    google_profile = await fetch_google_profile(google_access_token)
    avatar_url = google_profile.get("picture", None)

    if not email:
        return RedirectResponse(
            url=f"{settings.google_frontend_redirect_url}?error=missing_email",
            status_code=302,
        )

    # Get or create user
    user_db = SQLAlchemyUserDatabase(session, User, OAuthAccount)
    user = await user_db.get_by_oauth_account("google", google_id)

    if user:
        if avatar_url and user.avatar_url != avatar_url:
            user.avatar_url = avatar_url
            session.add(user)
            await session.commit()
            await session.refresh(user)
    else:
        user = await user_db.get_by_email(email)
        if user:
            user.is_verified = True
            if avatar_url and user.avatar_url != avatar_url:
                user.avatar_url = avatar_url
                session.add(user)
            await session.commit()
            await session.refresh(user)

            await user_db.add_oauth_account(
                user,
                {
                    "oauth_name": "google",
                    "access_token": google_access_token,
                    "expires_at": None,
                    "account_id": google_id,
                    "account_email": email,
                },
            )

        else:
            password_helper = PasswordHelper()
            random_hash = password_helper.hash(secrets.token_urlsafe(32))
            user = User(
                email=email,
                hashed_password=random_hash,
                is_verified=True,
                has_password=False,
                avatar_url=avatar_url,
            )
            session.add(user)
            await session.flush()

            await user_db.add_oauth_account(
                user,
                {
                    "oauth_name": "google",
                    "access_token": google_access_token,
                    "expires_at": None,
                    "account_id": google_id,
                    "account_email": email,
                },
            )
            await session.refresh(user)

    jwt_strategy = get_jwt_strategy()
    jwt_token = await jwt_strategy.write_token(user)

    return RedirectResponse(
        url=f"{settings.google_frontend_redirect_url}?access_token={jwt_token}&token_type=bearer",
        status_code=302,
    )
