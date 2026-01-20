from fastapi import APIRouter

from .schemas import UserRead, UserCreate, UserUpdate
from .dependencies import fastapi_users
from .services import auth_backend

router = APIRouter()

router.include_router(
    fastapi_users.get_auth_router(auth_backend),
    prefix="/jwt",
)
router.include_router(
    fastapi_users.get_register_router(UserRead, UserCreate),
)
router.include_router(
    fastapi_users.get_reset_password_router(),
)
router.include_router(
    fastapi_users.get_verify_router(UserRead),
)
router.include_router(
    fastapi_users.get_users_router(UserRead, UserUpdate),
)
