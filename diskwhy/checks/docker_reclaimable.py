from __future__ import annotations

import json
import shutil
import subprocess
from pathlib import Path

from diskwhy.plugin import CheckResult, Finding


class DockerReclaimableCheck:
    """Espacio reclamable de Docker (imágenes sin usar, cache de build, contenedores parados) vía `docker system df` -- solo lee, nunca ejecuta `docker system prune` por su cuenta."""

    name = "docker_reclaimable"

    def run(self, root: Path) -> CheckResult:
        del root  # no depende del árbol de ficheros, solo consulta al daemon de Docker
        if shutil.which("docker") is None:
            return CheckResult(
                check_name=self.name,
                summary="No aplica: docker no está instalado o no está en el PATH.",
            )

        try:
            result = subprocess.run(
                ["docker", "system", "df", "--format", "{{json .}}"],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
        except (OSError, subprocess.TimeoutExpired):
            return CheckResult(
                check_name=self.name,
                summary="No aplica: no se pudo ejecutar 'docker system df'.",
            )

        if result.returncode != 0:
            return CheckResult(
                check_name=self.name,
                summary="No aplica: 'docker system df' falló (¿el daemon de Docker está corriendo?).",
            )

        findings: list[Finding] = []
        for line in result.stdout.splitlines():
            line = line.strip()
            if not line:
                continue
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            reclaimable = row.get("Reclaimable", "")
            # OJO: no usar `.startswith("0")` -- un valor real como "0.5GB (10%)"
            # también empieza por "0" y se descartaría como si fuera cero. Docker
            # solo representa el cero exacto como "0B" (no hay unidad más pequeña
            # que el byte, así que nunca hay un "0.xxx B"), con o sin porcentaje
            # detrás -- ese es el único prefijo que de verdad significa "nada".
            if not reclaimable or reclaimable.strip().startswith("0B"):
                continue
            findings.append(
                Finding(
                    severity="info",
                    title=f"{row.get('Type', '?')}: {reclaimable} reclamable",
                    detail=(
                        f"Total: {row.get('Size', '?')}. "
                        "Revisar con 'docker system df -v' antes de un 'docker system prune'."
                    ),
                )
            )

        return CheckResult(
            check_name=self.name,
            summary=f"{len(findings)} categoría(s) de Docker con espacio reclamable.",
            findings=findings,
        )
