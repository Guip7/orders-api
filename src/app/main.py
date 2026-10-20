from fastapi import FastAPI

app = FastAPI(
    title="Orders API",
    description=(
        """API de catálogo, estoque, pedidos e pagamentos.\n\n
        Garante consistência de estoque sob concorrência, 
        idempotência na criação de pedidos e processamento 
        assíncrono de pagamentos."""
    ),
    version="0.1.0",
)
@app.get("/")
async def root():
    return {"message": "Hello World"}
