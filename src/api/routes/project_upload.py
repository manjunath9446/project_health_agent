import gc
import os
import tempfile
import time
import uuid

from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from loguru import logger

from src.agents.coordinator import CoordinatorAgent
from src.api.dependencies import get_coordinator
from src.core.config import settings
from src.core.logging_config import set_file_processing_id
from src.schemas.project import ProjectUploadResponse

router = APIRouter()


@router.post(
    "/projects/upload",
    response_model=ProjectUploadResponse,
)
async def upload_project(
    file: UploadFile = File(...),
    coordinator: CoordinatorAgent = Depends(get_coordinator),
):
    # -------------------------------------------------------
    # Validate file
    # -------------------------------------------------------
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is missing.",
        )

    if not file.filename.lower().endswith(".xlsx"):
        raise HTTPException(
            status_code=400,
            detail="Only .xlsx files are supported.",
        )

    contents = await file.read()

    if len(contents) > settings.max_upload_size_mb * 1024 * 1024:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum upload size is {settings.max_upload_size_mb} MB.",
        )

    # -------------------------------------------------------
    # Logging
    # -------------------------------------------------------
    processing_id = str(uuid.uuid4())
    set_file_processing_id(processing_id)

    logger.info(
        "Processing upload {} ({})",
        processing_id,
        file.filename,
    )

    # -------------------------------------------------------
    # Save temporary file
    # -------------------------------------------------------
    with tempfile.NamedTemporaryFile(
        delete=False,
        suffix=".xlsx",
    ) as tmp:
        tmp.write(contents)
        tmp_path = tmp.name

    try:
        project_name = os.path.splitext(file.filename)[0]

        project_id, project_context, quality_report = (
            await coordinator.process_upload(
                tmp_path,
                project_name,
            )
        )

        return ProjectUploadResponse(
            project_id=project_id,
            project_name=project_name,
            status="success",
            message="Project uploaded and processed successfully.",
            data_quality_report=quality_report,
        )

    except HTTPException:
        raise

    except Exception as e:
        logger.exception("Upload failed")

        raise HTTPException(
            status_code=500,
            detail=f"Processing failed: {str(e)}",
        )

    finally:
        gc.collect()
        time.sleep(0.2)

        try:
            if os.path.exists(tmp_path):
                os.unlink(tmp_path)
        except PermissionError:
            logger.warning(
                "Temporary file could not be deleted: {}",
                tmp_path,
            )