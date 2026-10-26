from fastapi import APIRouter

from app.schemas.health import HealthResponse

router = APIRouter(tags=["health"])


@router.get("/health")
async def health() -> HealthResponse:
    """Liveness:
    indica que o processo da API está de pé.
    """
    return HealthResponse(status="ok")
