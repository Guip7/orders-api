from collections.abc import Iterator
from typing import Any

import pytest
from fastapi.testclient import TestClient
from sqlalchemy.exc import OperationalError

from app.core.db import get_session
from app.main import app

client = TestClient(app)


class FakeSession:
    """Sessão falsa: permite testar a rota sem um banco de verdade."""

    def __init__(self, error: Exception | None = None) -> None:
        self.error = error

    async def execute(self, *args: Any, **kwargs: Any) -> None:
        if self.error:
            raise self.error


@pytest.fixture
def override_session() -> Iterator[Any]:
    def _set(session: FakeSession) -> None:
        async def _fake() -> FakeSession:
            return session

        app.dependency_overrides[get_session] = _fake

    yield _set
    app.dependency_overrides.clear()


def test_health_returns_ok() -> None:
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_returns_ok_when_database_responds(override_session: Any) -> None:
    override_session(FakeSession())

    response = client.get("/health/ready")

    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_ready_returns_503_when_database_is_down(override_session: Any) -> None:
    override_session(FakeSession(OperationalError("SELECT 1", {}, Exception("down"))))

    response = client.get("/health/ready")

    assert response.status_code == 503
