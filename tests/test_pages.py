# SPDX-License-Identifier: MIT
"""Startseite, Zähler in DATA_DIR, CSP und keine Inline-Skripte."""

from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app


def test_index_and_counter(data_dir: Path) -> None:
    client = TestClient(app)
    page = client.get("/")
    assert page.status_code == 200 and ">0<" in page.text
    assert "script-src 'self'" in page.headers["content-security-policy"]
    assert client.post("/zaehlen").text.strip().endswith(">1</p>")
    assert client.post("/zaehlen").text.strip().endswith(">2</p>")
    assert (data_dir / "app.db").exists()


def test_foreign_origin_rejected() -> None:
    response = TestClient(app).post("/zaehlen", headers={"Origin": "https://boese.example"})
    assert response.status_code == 403


def test_no_inline_scripts_or_styles() -> None:
    for template in (Path(__file__).parents[1] / "app" / "templates").glob("*.html"):
        text = template.read_text()
        assert "style=" not in text and "onclick" not in text
        assert "<script>" not in text
