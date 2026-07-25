from __future__ import annotations

import os
from pathlib import Path

from diskwhy.fs import dir_size, human_size
from diskwhy.patterns import RECLAIMABLE_DIR_NAMES
from diskwhy.plugin import CheckResult, Finding


def _find_junk_dirs(root: Path):
    for dirpath, dirnames, _filenames in os.walk(root, followlinks=False):
        keep = []
        for name in dirnames:
            if name in RECLAIMABLE_DIR_NAMES:
                yield Path(dirpath) / name
                # no descender dentro -- evita contar cachés anidadas dos veces
            else:
                keep.append(name)
        dirnames[:] = keep


class ReclaimableDirsCheck:
    """Carpetas regenerables (node_modules, __pycache__, venvs, cachés de build...) -- seguro borrar y reinstalar/reconstruir cuando haga falta."""

    name = "reclaimable_dirs"

    def run(self, root: Path) -> CheckResult:
        findings: list[Finding] = []
        total = 0
        for junk_dir in _find_junk_dirs(root):
            size = dir_size(junk_dir)
            total += size
            findings.append(
                Finding(
                    severity="info",
                    title=f"{junk_dir.name} ({human_size(size)})",
                    detail="Regenerable -- seguro borrar y reinstalar/reconstruir cuando haga falta.",
                    path=str(junk_dir),
                    size_bytes=size,
                )
            )

        findings.sort(key=lambda f: f.size_bytes or 0, reverse=True)
        return CheckResult(
            check_name=self.name,
            summary=f"{len(findings)} carpeta(s) regenerables, {human_size(total)} recuperables en total.",
            findings=findings,
        )
