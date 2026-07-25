from __future__ import annotations

from pathlib import Path

import pytest


@pytest.fixture
def tree(tmp_path: Path) -> Path:
    return tmp_path


def make_dir_with_size(path: Path, size_bytes: int) -> Path:
    path.mkdir(parents=True, exist_ok=True)
    (path / "data.bin").write_bytes(b"\0" * size_bytes)
    return path


def write(path: Path, relpath: str, content: str = "") -> Path:
    p = path / relpath
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_text(content, encoding="utf-8")
    return p
