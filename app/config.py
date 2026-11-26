# SPDX-License-Identifier: MIT
"""Konfiguration nur aus der Umgebung (App-Standard §4.1). Nur hier wird die Umgebung gelesen."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path


@dataclass(frozen=True)
class Config:
    app_env: str
    app_url: str
    data_dir: Path
    secret_key: str = field(repr=False)
    log_level: str
    #: Zugewiesene MariaDB (LayerNX Deploy, Paket 2.1): Socket, Name, Benutzer, Passwort.
    db_socket: str = ""
    db_name: str = ""
    db_user: str = ""
    db_password: str = field(default="", repr=False)


def load() -> Config:
    return Config(
        app_env=os.environ.get("APP_ENV", "development"),
        app_url=os.environ.get("APP_URL", ""),
        data_dir=Path(os.environ.get("DATA_DIR") or ".data"),
        secret_key=os.environ.get("SECRET_KEY", ""),
        log_level=os.environ.get("LOG_LEVEL", "info"),
        db_socket=os.environ.get("DB_SOCKET", ""),
        db_name=os.environ.get("DB_NAME", ""),
        db_user=os.environ.get("DB_USER", ""),
        db_password=os.environ.get("DB_PASSWORD", ""),
    )
