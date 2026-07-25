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
        "poetry.lock",
    }
)

VENV_DIR_NAMES: frozenset[str] = frozenset({".venv", "venv"})

LOCKFILE_NAMES: frozenset[str] = frozenset(
    {
        "package-lock.json",
        "yarn.lock",
        "pnpm-lock.yaml",
    }
)
