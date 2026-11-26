# SPDX-License-Identifier: MIT
"""Einstieg der App: ASGI-Objekt ``app`` (App-Standard A1).

Deploy startet ``uvicorn app.main:app`` auf einem Unix-Socket; die App legt selbst keinen Port fest.
"""

from __future__ import annotations

import json
import logging
import sys
from pathlib import Path

from fastapi import FastAPI, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates

from app import db, health
from app.config import load

HERE = Path(__file__).resolve().parent
templates = Jinja2Templates(directory=HERE / "templates")


class JsonLines(logging.Formatter):
    def format(self, record: logging.LogRecord) -> str:
        return json.dumps({"level": record.levelname.lower(), "msg": record.getMessage()})


handler = logging.StreamHandler(sys.stdout)
handler.setFormatter(JsonLines())
logging.basicConfig(level=load().log_level.upper(), handlers=[handler])

app = FastAPI(title="meine-app", docs_url=None, redoc_url=None, openapi_url=None)
app.include_router(health.router)
app.mount("/static", StaticFiles(directory=HERE / "static"), name="static")


@app.middleware("http")
async def security_headers(request: Request, call_next):  # type: ignore[no-untyped-def]
    response = await call_next(request)
    response.headers["Content-Security-Policy"] = (
        "default-src 'self'; script-src 'self'; object-src 'none'; "
        "frame-ancestors 'none'; base-uri 'none'"
    )
    response.headers["X-Content-Type-Options"] = "nosniff"
    response.headers["Referrer-Policy"] = "same-origin"
    return response


@app.get("/", response_class=HTMLResponse)
def index(request: Request) -> HTMLResponse:
    count = db.read(load().data_dir, "besuche")
    return templates.TemplateResponse(request, "index.html", {"count": count})


@app.post("/zaehlen", response_class=HTMLResponse)
def count_up(request: Request) -> HTMLResponse:
    origin = request.headers.get("origin")
    if origin is not None and origin.split("://", 1)[-1] != request.headers.get("host"):
        raise HTTPException(403)
    count = db.increment(load().data_dir, "besuche")
    return templates.TemplateResponse(request, "_zahl.html", {"count": count})
