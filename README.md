# Orders API

API de catálogo, estoque, pedidos e pagamentos, com foco em consistência
de estoque sob concorrência, idempotência e processamento assíncrono.

## Requisitos

- Python 3.12+
- [uv](https://docs.astral.sh/uv/)

## Instalação

    git clone https://github.com/Guip7/orders-api.git
    cd orders-api
    uv sync

## Como rodar

    uv run uvicorn app.main:app --app-dir src --reload

A documentação interativa fica em http://localhost:8000/docs

## Documentação do projeto

- [PRD](docs/prd.md)
- [ADR 001: Stack base](docs/adr/001-stack.md)