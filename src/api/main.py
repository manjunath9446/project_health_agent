from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.project_upload import router as upload_router
from src.core.database import init_db
from src.core.logging_config import configure_logging, set_correlation_id

# ----------------------------------------------------
# Configure Logging
# ----------------------------------------------------

configure_logging()


# ----------------------------------------------------
# Lifespan
# ----------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("🚀 Starting Backend...")

    await init_db()

    print("✅ Database initialized.")

    yield

    print("🛑 Backend Stopped")


# ----------------------------------------------------
# App
# ----------------------------------------------------

app = FastAPI(
    title="AI Project Health Intelligence API",
    description="AI-powered Project Health Assessment",
    version="1.0.0",
    lifespan=lifespan,
)


# ----------------------------------------------------
# CORS
# ----------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://project-health-agent-1.onrender.com",
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ----------------------------------------------------
# Correlation ID
# ----------------------------------------------------

@app.middleware("http")
async def correlation_id_middleware(
    request: Request,
    call_next,
):
    set_correlation_id()
    return await call_next(request)


# ----------------------------------------------------
# Health
# ----------------------------------------------------

@app.get("/")
async def root():
    return {
        "message": "AI Project Health Backend Running"
    }


@app.get("/health")
async def health():
    return {
        "status": "healthy"
    }


# ----------------------------------------------------
# Routes
# ----------------------------------------------------

app.include_router(
    upload_router,
    prefix="/api/v1",
    tags=["Project Upload"],
)