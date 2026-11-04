RECLAIMABLE_DIR_NAMES: frozenset[str] = frozenset(
    {
        "node_modules",
        "__pycache__",
        ".venv",
        "venv",
        ".pytest_cache",
        ".ruff_cache",
        ".mypy_cache",
        "dist",
        "build",
        ".tox",
        "target",
        ".next",
        ".nuxt",
        ".cache",
        ".parcel-cache",
        "coverage",
        "htmlcov",
        ".gradle",
        ".terraform",
    }
)

# Ficheros que, si están junto a un .venv/venv, indican que el proyecto
# sigue existiendo (el venv no está huérfano).
PROJECT_MARKER_FILES: frozenset[str] = frozenset(
    {
        "pyproject.toml",
        "requirements.txt",
        "setup.py",
        "setup.cfg",
        "Pipfile",
        "Pipfile.lock",
        "poetry.lock",
        "uv.lock",
        "pdm.lock",
        "pixi.toml",
        "environment.yml",
        "environment.yaml",
        "tox.ini",
        "hatch.toml",
        "requirements",   # directorio requirements/base.txt, dev.txt...
    }
)
# Además de los anteriores: requirements-dev.txt, código o notebooks sueltos junto al venv.
PROJECT_MARKER_GLOBS: tuple[str, ...] = ("requirements*.txt", "*.py", "*.ipynb")

# Nombres que también se usan para carpetas de código (el build/ de un proyecto Go, un dist/ que
# se publica...): solo son regenerables si git no tiene ficheros dentro.
AMBIGUOUS_DIR_NAMES: frozenset[str] = frozenset({"build", "dist", "target", "coverage", ".cache"})

VENV_DIR_NAMES: frozenset[str] = frozenset({".venv", "venv"})

LOCKFILE_NAMES: frozenset[str] = frozenset(
    {
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
    }
)
