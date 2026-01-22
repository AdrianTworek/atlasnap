from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.settings import settings
from app.auth.router import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Lifespan context manager for startup/shutdown events."""
    yield


app = FastAPI(
    title=settings.app_name,
    description="Travel memory storage and organization SaaS",
    version=settings.version,
    lifespan=lifespan,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/api/v1/auth")


@app.get("/", tags=["root"])
def root():
    """Root endpoint."""
    return {"message": "Welcome to Atlasnap API!"}


@app.get("/health", tags=["health"])
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
