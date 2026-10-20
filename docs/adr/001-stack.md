# ADR 001: Stack base do projeto
## Status
Aceito

## Contexto

A Orders API precisa de transações ACID e controle de concorrência para reservar estoque sem overselling. Os dados são relacionais (usuários, produtos, pedidos, itens do pedido). A API deve atender muitas requisições I/O-bound (banco, Redis, chamadas ao gateway de pagamento), ter documentação automática e boa testabilidade. O projeto também serve como portfólio e aprendizado, então a stack deve ser moderna e amplamente usada no mercado.

## Decisão

Linguagem: Python 3.12+
Framework web: FastAPI
ORM: SQLAlchemy 2.0 (modo async)
Migrations: Alembic
Banco de dados: PostgreSQL 16
Gerenciador de pacotes: uv

## Alternativas consideradas

Django REST Framework (em vez de FastAPI): ecossistema maduro e admin pronto, mas suporte async é menos natural, é mais opinativo e o projeto não precisa de templates nem do admin do Django. FastAPI dá validação com Pydantic e OpenAPI de graça.
Flask (em vez de FastAPI): simples e flexível, porém exige montar manualmente validação, documentação e suporte async.
Django ORM / SQLModel / Tortoise (em vez de SQLAlchemy): SQLAlchemy 2.0 é o padrão de fato fora do Django, dá controle fino sobre queries e locks (SELECT ... FOR UPDATE) e tem integração direta com Alembic.
MySQL (em vez de PostgreSQL): atenderia, mas o Postgres tem recursos úteis para o projeto (FOR UPDATE SKIP LOCKED, índices parciais, JSONB) e é a escolha mais comum no ecossistema Python.
MongoDB (em vez de PostgreSQL): modelo de documentos não combina com dados fortemente relacionais e transações multi-entidade.
Poetry ou pip + venv (em vez de uv): Poetry é consolidado, porém mais lento e não gerencia versões do Python. pip + venv é o mais básico, sem lockfile nativo. uv é muito mais rápido, gera lockfile, gerencia versões do Python e tem adoção crescente.
## Consequências

(+) Transações, locks e integridade referencial robustos
(+) Documentação OpenAPI e validação automáticas
(+) Instalação de dependências rápida local e no CI
(+) Tipagem de ponta a ponta (Pydantic + mypy)
(-) SQLAlchemy async tem curva de aprendizado maior (sessões, lazy loading não funciona em async)
(-) Escalar escrita horizontalmente no Postgres é mais difícil
(-) uv é mais novo que Poetry; parte do mercado ainda usa Poetry, então o time precisa conhecer ambos
(-) Migrations exigem cuidado (revisar o SQL gerado pelo autogenerate)