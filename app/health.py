# SPDX-License-Identifier: MIT
"""GET /healthz (App-Standard A2): 200 und {"status": "ok"}, prüft die Datenbank."""

from __future__ import annotations

from fastapi import APIRouter
from fastapi.responses import JSONResponse

from app import db, mariadb
from app.config import load

router = APIRouter()


@router.get("/healthz", include_in_schema=False)
def healthz() -> JSONResponse:
    config = load()
    if not db.healthy(config.data_dir):
        return JSONResponse({"status": "fehler"}, status_code=503)
    if mariadb.configured(config) and not mariadb.healthy(config):
        return JSONResponse({"status": "fehler", "failed": ["mariadb"]}, status_code=503)
    return JSONResponse({"status": "ok"})
