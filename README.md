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
    uv run pre-commit install

## Como rodar

    uv run uvicorn app.main:app --app-dir src --reload

A documentação interativa fica em http://localhost:8000/docs

## Desenvolvimento

### Configurar o ambiente

    uv sync
    uv run pre-commit install

O `uv sync` instala as dependências, incluindo as de desenvolvimento.
O `pre-commit install` ativa as verificações automáticas a cada commit
(precisa ser feito uma vez em cada máquina).

### Qualidade de código

| Comando | O que faz |
|---|---|
| `uv run ruff check .` | Procura erros e problemas de estilo (lint) |
| `uv run ruff check --fix .` | Corrige automaticamente o que for possível |
| `uv run ruff format .` | Formata o código no padrão do projeto |
| `uv run mypy` | Verifica a tipagem |
| `uv run pre-commit run --all-files` | Roda todas as verificações em todos os arquivos |

O pre-commit executa Ruff e mypy automaticamente a cada `git commit`.
Se alguma verificação falhar, o commit é barrado até o problema ser corrigido.

## Documentação do projeto

- [PRD](docs/prd.md)
- [ADR 001: Stack base](docs/adr/001-stack.md)

