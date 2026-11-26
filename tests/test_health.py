# SPDX-License-Identifier: MIT
"""App-Standard A2 und A12: /healthz antwortet 200 und {"status": "ok"}."""

from fastapi.testclient import TestClient

from app.main import app


def test_health() -> None:
    response = TestClient(app).get("/healthz")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_health_fails_without_reachable_mariadb(monkeypatch, tmp_path) -> None:  # type: ignore[no-untyped-def]
    """Ist eine Datenbank zugewiesen, prüft /healthz auch sie."""
    monkeypatch.setenv("DB_SOCKET", str(tmp_path / "fehlt.sock"))
    monkeypatch.setenv("DB_USER", "app1")
    monkeypatch.setenv("DB_PASSWORD", "x")
    response = TestClient(app).get("/healthz")
    assert response.status_code == 503
    assert response.json()["failed"] == ["mariadb"]
