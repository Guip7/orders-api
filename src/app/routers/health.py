from fastapi import APIRouter, HTTPException
from sqlalchemy import text
from sqlalchemy.exc import SQLAlchemyError

from app.core.db import SessionDep
from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> HealthResponse:
    """Liveness:
    indica que o processo da API está de pé.
    """
    return HealthResponse(status="ok")


@router.get("/health/ready")
async def ready(session: SessionDep) -> HealthResponse:
    """
    Readiness: a API consegue falar com o banco?"
    """
    try:
        await session.execute(text("SELECT 1"))
    except (SQLAlchemyError, OSError) as exc:
        raise HTTPException(status_code=503, detail="database unavailable") from exc
    return HealthResponse(status="ok")
