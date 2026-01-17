from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware


app = FastAPI(
    title="Atlasnap API",
    description="Travel memory storage and organization SaaS",
    version="0.1.0",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def root():
    """Root endpoint."""
    return {"message": "Welcome to Atlasnap API!"}


@app.get("/health")
def health_check():
    """Health check endpoint."""
    return {"status": "ok"}
