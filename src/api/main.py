from fastapi import FastAPI, Request
from src.api.routes.project_upload import router as upload_router
from src.core.logging_config import configure_logging, set_correlation_id

configure_logging()

app = FastAPI(title="Project Health AI - Phase 1")

@app.middleware("http")
async def add_correlation_middleware(request: Request, call_next):
    set_correlation_id()
    response = await call_next(request)
    return response

app.include_router(upload_router, prefix="/api/v1")