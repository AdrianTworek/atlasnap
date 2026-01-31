from fastapi import FastAPI, Request, status
from fastapi.responses import JSONResponse


def register_exception_handlers(app: FastAPI) -> None:
    """Register exception handlers."""
    from app.media.exceptions import MediaNotFound, UnsupportedMediaType, FileTooLarge

    @app.exception_handler(MediaNotFound)
    async def _(req: Request, exc: MediaNotFound):
        return JSONResponse(
            status_code=status.HTTP_404_NOT_FOUND,
            content={"detail": str(exc)},
        )

    @app.exception_handler(UnsupportedMediaType)
    async def _(req: Request, exc: UnsupportedMediaType):
        return JSONResponse(
            status_code=status.HTTP_400_BAD_REQUEST,
            content={"detail": str(exc)},
        )

    @app.exception_handler(FileTooLarge)
    async def _(req: Request, exc: FileTooLarge):
        return JSONResponse(
            status_code=status.HTTP_413_REQUEST_ENTITY_TOO_LARGE,
            content={"detail": str(exc)},
        )
