from conftest import make_dir_with_size, write

from diskwhy.checks.orphaned_envs import OrphanedEnvsCheck


def test_venv_sin_proyecto_es_huerfano(tree):
    make_dir_with_size(tree / "old-project" / ".venv", 500)
    result = OrphanedEnvsCheck().run(tree)
    assert len(result.findings) == 1
    assert "huérfano" in result.findings[0].title.lower() or "huerfano" in result.findings[0].detail.lower()
    assert result.findings[0].severity == "high"


def test_venv_con_pyproject_no_es_huerfano(tree):
    make_dir_with_size(tree / "proj" / ".venv", 500)
    write(tree / "proj", "pyproject.toml", "[project]\nname='x'\n")
    result = OrphanedEnvsCheck().run(tree)
    assert result.findings == []


def test_venv_con_requirements_txt_no_es_huerfano(tree):
    make_dir_with_size(tree / "proj" / "venv", 500)
    write(tree / "proj", "requirements.txt", "click\n")
    result = OrphanedEnvsCheck().run(tree)
    assert result.findings == []


def test_sin_venvs_no_hay_hallazgos(tree):
    write(tree, "src/main.py", "x=1\n")
    result = OrphanedEnvsCheck().run(tree)
    assert result.findings == []
    assert "0 entorno" in result.summary
