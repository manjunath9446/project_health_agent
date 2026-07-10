from contextlib import asynccontextmanager

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware

from src.api.routes.project_upload import router as upload_router
from src.core.logging_config import configure_logging, set_correlation_id

# ----------------------------------------------------
# Configure Logging
# ----------------------------------------------------

configure_logging()


# ----------------------------------------------------
# Application Lifespan
# ----------------------------------------------------

@asynccontextmanager
async def lifespan(app: FastAPI):

    print("🚀 AI Project Health Backend Started")

    yield

    print("🛑 AI Project Health Backend Stopped")


# ----------------------------------------------------
# FastAPI App
# ----------------------------------------------------

app = FastAPI(
    title="AI Project Health Intelligence API",
    description="AI-powered Project Health Assessment using Multi-Agent Intelligence",
    version="1.0.0",
    lifespan=lifespan,
)


# ----------------------------------------------------
# Middleware
# ----------------------------------------------------

app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://project-health-agent-1.onrender.com"],      # Replace with your frontend URL later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.middleware("http")
async def correlation_id_middleware(
    request: Request,
    call_next,
):

    set_correlation_id()

    response = await call_next(request)

    return response


# ----------------------------------------------------
# Health Endpoints
# ----------------------------------------------------

@app.get("/", tags=["Health"])
async def root():

    return {
        "message": "AI Project Health Backend Running",
        "status": "healthy",
    }


@app.get("/health", tags=["Health"])
async def health():

    return {
        "status": "healthy",
        "service": "AI Project Health Intelligence",
        "version": "1.0.0",
    }


# ----------------------------------------------------
# Routers
# ----------------------------------------------------

app.include_router(
    upload_router,
    prefix="/api/v1",
    tags=["Project Upload"],
)