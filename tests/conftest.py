# SPDX-License-Identifier: MIT
"""Jeder Test bekommt einen eigenen DATA_DIR; ohne Netz."""

from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture(autouse=True)
def data_dir(tmp_path: Path, monkeypatch: pytest.MonkeyPatch) -> Path:
    monkeypatch.setenv("DATA_DIR", str(tmp_path / "data"))
    return tmp_path / "data"
