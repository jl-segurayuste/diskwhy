from __future__ import annotations

import os
from pathlib import Path

from diskwhy.fs import dir_size, human_size
from diskwhy.patterns import PROJECT_MARKER_FILES, PROJECT_MARKER_GLOBS, VENV_DIR_NAMES
from diskwhy.plugin import CheckResult, Finding


def _find_venv_dirs(root: Path):
    for dirpath, dirnames, _filenames in os.walk(root, followlinks=False):
        keep = []
        for name in dirnames:
            if name in VENV_DIR_NAMES:
                yield Path(dirpath) / name
            else:
                keep.append(name)
        dirnames[:] = keep


def _has_project_markers(parent: Path) -> bool:
    # Antes solo los nombres fijos: un proyecto con requirements-dev.txt, uv.lock o solo scripts
    # salía como huérfano con gravedad alta.
    if any((parent / marker).exists() for marker in PROJECT_MARKER_FILES):
        return True
    return any(next(parent.glob(pattern), None) is not None for pattern in PROJECT_MARKER_GLOBS)


class OrphanedEnvsCheck:
    """Entornos virtuales (.venv/venv) cuyo proyecto ya no tiene ningún fichero de dependencias al lado -- probablemente el proyecto se borró y el venv se quedó atrás."""

    name = "orphaned_envs"

    def run(self, root: Path) -> CheckResult:
        findings: list[Finding] = []
        scanned = 0
        for venv_dir in _find_venv_dirs(root):
            scanned += 1
            if not _has_project_markers(venv_dir.parent):
                size = dir_size(venv_dir)
                findings.append(
                    Finding(
                        severity="high",
                        title=f"Entorno huérfano: {venv_dir} ({human_size(size)})",
                        detail="No hay pyproject.toml/requirements.txt/setup.py junto a este venv -- el proyecto probablemente ya no existe.",
                        path=str(venv_dir),
                        size_bytes=size,
                    )
                )

        findings.sort(key=lambda f: f.size_bytes or 0, reverse=True)
        return CheckResult(
            check_name=self.name,
            summary=f"{scanned} entorno(s) virtual(es) revisado(s), {len(findings)} huérfano(s).",
            findings=findings,
        )
