import sys
import uuid
from loguru import logger
from contextvars import ContextVar
from src.core.config import settings

correlation_id_var: ContextVar[str] = ContextVar("correlation_id", default="")
file_processing_id_var: ContextVar[str] = ContextVar("file_processing_id", default="")

def configure_logging():
    logger.remove()
    fmt = (
        "<green>{time:YYYY-MM-DD HH:mm:ss.SSS}</green> | "
        "<level>{level: <8}</level> | "
        "cid=<cyan>{extra[correlation_id]}</cyan> | "
        "fid=<magenta>{extra[file_processing_id]}</magenta> | "
        "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
        "<level>{message}</level>"
    )
    logger.add(sys.stderr, format=fmt, level=settings.log_level, colorize=True)
    logger.add(
        settings.log_file_path,
        rotation="10 MB",
        retention="30 days",
        compression="zip",
        format=fmt,
        level="DEBUG",
    )
    logger.configure(extra={"correlation_id": "", "file_processing_id": ""})

def set_correlation_id():
    cid = str(uuid.uuid4())
    correlation_id_var.set(cid)
    logger.configure(extra={"correlation_id": cid, "file_processing_id": ""})

def set_file_processing_id(fid: str):
    file_processing_id_var.set(fid)
    logger.configure(extra={"correlation_id": correlation_id_var.get(), "file_processing_id": fid})