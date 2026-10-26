from fastapi import FastAPI

from app.core.config import get_settings
from app.routers import health

settings = get_settings()


app = FastAPI(
    title="Orders API",
    description=(
        "API de catálogo, estoque, pedidos e pagamentos.\n\n"
        "Garante consistência de estoque sob concorrência, "
        "idempotência na criação de pedidos e processamento "
        "assíncrono de pagamentos."
    ),
    version="0.1.0",
    debug=settings.debug,
)

app.include_router(health.router)
