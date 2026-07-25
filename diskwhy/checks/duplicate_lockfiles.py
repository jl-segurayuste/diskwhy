from __future__ import annotations

import hashlib
import os
from collections import defaultdict
from pathlib import Path

from diskwhy.patterns import LOCKFILE_NAMES
from diskwhy.plugin import CheckResult, Finding


def _find_lockfiles(root: Path):
    for dirpath, dirnames, filenames in os.walk(root, followlinks=False):
        if "node_modules" in dirnames:
            dirnames.remove("node_modules")  # nunca hay lockfiles utiles ahi dentro
        for name in filenames:
            if name in LOCKFILE_NAMES:
                yield Path(dirpath) / name


def _hash_file(path: Path) -> str | None:
    try:
        return hashlib.sha256(path.read_bytes()).hexdigest()
    except OSError:
        return None


class DuplicateLockfilesCheck:
    """Lockfiles (package-lock.json/yarn.lock/pnpm-lock.yaml) con contenido idéntico en proyectos distintos -- candidatos a compartir un cache global del gestor de paquetes en vez de duplicar node_modules por completo."""

    name = "duplicate_lockfiles"

    def run(self, root: Path) -> CheckResult:
        by_hash: dict[str, list[Path]] = defaultdict(list)
        scanned = 0
        for lockfile in _find_lockfiles(root):
            digest = _hash_file(lockfile)
            if digest is None:
                continue
            scanned += 1
            by_hash[digest].append(lockfile)

        findings: list[Finding] = []
        for digest, paths in by_hash.items():
            if len(paths) < 2:
                continue
            paths_str = ", ".join(str(p) for p in paths)
            findings.append(
                Finding(
                    severity="info",
                    title=f"{len(paths)} lockfiles idénticos ({paths[0].name})",
                    detail=(
                        f"Mismas dependencias exactas en: {paths_str}. "
                        "Considera un gestor de paquetes con cache global (pnpm) "
                        "para no duplicar node_modules por completo."
                    ),
                )
            )

        return CheckResult(
            check_name=self.name,
            summary=f"{scanned} lockfile(s) analizados, {len(findings)} grupo(s) duplicado(s).",
            findings=findings,
        )
