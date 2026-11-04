from __future__ import annotations

import os
import stat
from pathlib import Path


def dir_size(path: Path) -> int:
    """Espacio que ocupa de verdad en disco, como `du`.

    Se cuentan los bloques asignados (no `st_size`: un disco de VM disperso de 10 GB que ocupa
    4 KB salía como 10 GB) y cada inodo una sola vez (los enlaces duros de pnpm, ccache o
    `cp -al` se sumaban una vez por enlace).
    """
    total = 0
    seen: set[tuple[int, int]] = set()
    for dirpath, _dirnames, filenames in os.walk(path, followlinks=False):
        for name in filenames:
            try:
                st = os.lstat(os.path.join(dirpath, name))
            except OSError:
                continue
            if stat.S_ISLNK(st.st_mode):
                continue
            if st.st_nlink > 1:
                key = (st.st_dev, st.st_ino)
                if key in seen:
                    continue
                seen.add(key)
            blocks = getattr(st, "st_blocks", None)  # no existe en Windows
            total += blocks * 512 if blocks is not None else st.st_size
    return total


def human_size(num_bytes: int) -> str:
    size = float(num_bytes)
    for unit in ("B", "KB", "MB", "GB", "TB"):
        if size < 1024 or unit == "TB":
            return f"{size:.1f} {unit}" if unit != "B" else f"{int(size)} {unit}"
        size /= 1024
    return f"{size:.1f} TB"
