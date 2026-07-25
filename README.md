# diskwhy

Un `du` que explica *por qué* una carpeta pesa tanto y qué es seguro borrar —
en vez de solo mostrarte números y dejarte adivinar.

```
$ diskwhy scan ~/projects

diskwhy — /home/jose/projects

── reclaimable_dirs ─────────────────────
  4 carpeta(s) regenerables, 3.2 GB recuperables en total.
  [INFO  ] node_modules (1.8 GB) (/home/jose/projects/app/node_modules)
           Regenerable -- seguro borrar y reinstalar/reconstruir cuando haga falta.
  [INFO  ] .venv (900 MB) (/home/jose/projects/api/.venv)
           Regenerable -- seguro borrar y reinstalar/reconstruir cuando haga falta.

── orphaned_envs ────────────────────────
  3 entorno(s) virtual(es) revisado(s), 1 huérfano(s).
  [HIGH  ] Entorno huérfano: /home/jose/projects/old-script/.venv (400 MB)
           No hay pyproject.toml/requirements.txt/setup.py junto a este venv --
           el proyecto probablemente ya no existe.

Total: 6 hallazgo(s).
```

## Por qué existe

`du -sh */` te dice qué carpeta pesa más, pero no te dice si es seguro
borrarla. `diskwhy` sí: distingue entre "esto es regenerable" (node_modules,
venvs, cachés de build), "esto es un venv sin proyecto detrás" (candidato de
alta confianza para borrar del todo) y "esto son dependencias duplicadas
entre proyectos" — sin borrar nada por su cuenta, solo diagnostica.

## Instalación

Todavía no está en PyPI:

```bash
pip install git+https://github.com/jl-segurayuste/diskwhy.git
```

## Uso

```bash
diskwhy scan .                          # informe en consola
diskwhy scan . --only reclaimable_dirs  # solo un check
diskwhy scan . --json
diskwhy scan . --fail-on high           # código de salida 1 si hay algo "high"
diskwhy list-checks
```

## Checks incluidos

| Check | Qué detecta |
|---|---|
| `reclaimable_dirs` | `node_modules`, `__pycache__`, `.venv`/`venv`, cachés de build (`dist`, `.next`, `.tox`...) — regenerables, seguro borrar |
| `orphaned_envs` | Un `.venv`/`venv` sin ningún fichero de dependencias al lado — el proyecto probablemente ya no existe |
| `duplicate_lockfiles` | Lockfiles idénticos en proyectos distintos — candidatos a compartir cache de paquetes en vez de duplicar `node_modules` |
| `docker_reclaimable` | Espacio reclamable de Docker (`docker system df`) — solo lee, nunca ejecuta `docker system prune` |

Ningún check borra nada ni ejecuta código de lo que analiza — solo lee el
árbol de ficheros e introspecciona tamaños. Cada check es un plugin
independiente (`importlib.metadata.entry_points`, grupo `diskwhy.checks`).

## Desarrollo

```bash
pip install -e ".[dev]"
ruff check .
pytest
```
