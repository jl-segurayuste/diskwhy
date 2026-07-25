# Contribuir

## Añadir un check nuevo

Cada check implementa el protocolo `Check` (`diskwhy/plugin.py`):

```python
class MiCheck:
    name = "mi_check"

    def run(self, root: Path) -> CheckResult:
        ...
```

Se registra vía entry point en tu propio `pyproject.toml`:

```toml
[project.entry-points."diskwhy.checks"]
mi_check = "mi_paquete.check:MiCheck"
```

## Antes de un PR

- `ruff check .` y `pytest` en verde.
- Ningún check borra nada ni ejecuta comandos destructivos (`docker system
  prune`, `rm -rf`...) — solo diagnostica y sugiere.
- Si tu check usa una herramienta externa (como `docker`), debe fallar de
  forma silenciosa y clara ("no aplica") si no está disponible, no romper
  el resto del informe.
