# SPDX-License-Identifier: MIT
"""Zugewiesene MariaDB (nur wenn LayerNX Deploy eine zugewiesen hat): Verbindung über den Socket."""

from __future__ import annotations

from app.config import Config


def configured(config: Config) -> bool:
    return bool(config.db_socket and config.db_user)


def healthy(config: Config) -> bool:
    import pymysql  # erst hier: ohne zugewiesene Datenbank wird der Treiber nie gebraucht

    try:
        conn = pymysql.connect(
            unix_socket=config.db_socket,
            user=config.db_user,
            password=config.db_password,
            database=config.db_name or None,
            connect_timeout=3,
        )
    except pymysql.MySQLError:
        return False
    try:
        with conn.cursor() as cursor:
            cursor.execute("SELECT 1")
            return cursor.fetchone() == (1,)
    finally:
        conn.close()
