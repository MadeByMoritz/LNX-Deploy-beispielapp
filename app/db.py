# SPDX-License-Identifier: MIT
"""SQLite in DATA_DIR, im WAL-Modus (App-Standard A3, A5). Kein Zustand im Arbeitsspeicher (A4)."""

from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from pathlib import Path

SCHEMA = "CREATE TABLE IF NOT EXISTS zaehler (name TEXT PRIMARY KEY, wert INTEGER NOT NULL)"


@contextmanager
def connect(data_dir: Path) -> Iterator[sqlite3.Connection]:
    data_dir.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(data_dir / "app.db", timeout=5)
    try:
        conn.execute("PRAGMA journal_mode=WAL")
        conn.execute("PRAGMA busy_timeout=5000")
        conn.execute(SCHEMA)
        with conn:
            yield conn
    finally:
        conn.close()


def read(data_dir: Path, name: str) -> int:
    with connect(data_dir) as conn:
        row = conn.execute("SELECT wert FROM zaehler WHERE name = ?", (name,)).fetchone()
        return int(row[0]) if row else 0


def increment(data_dir: Path, name: str) -> int:
    with connect(data_dir) as conn:
        conn.execute(
            "INSERT INTO zaehler (name, wert) VALUES (?, 1) "
            "ON CONFLICT(name) DO UPDATE SET wert = wert + 1",
            (name,),
        )
        row = conn.execute("SELECT wert FROM zaehler WHERE name = ?", (name,)).fetchone()
        return int(row[0])


def healthy(data_dir: Path) -> bool:
    try:
        with connect(data_dir) as conn:
            conn.execute("SELECT 1")
        return True
    except sqlite3.Error:
        return False
