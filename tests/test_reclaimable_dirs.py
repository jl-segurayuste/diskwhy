from conftest import make_dir_with_size, write

from diskwhy.checks.reclaimable_dirs import ReclaimableDirsCheck


def test_detecta_node_modules(tree):
    make_dir_with_size(tree / "proj" / "node_modules", 1000)
    write(tree / "proj", "package.json", "{}")
    result = ReclaimableDirsCheck().run(tree)
    assert len(result.findings) == 1
    assert "node_modules" in result.findings[0].title


def test_detecta_varios_tipos(tree):
    make_dir_with_size(tree / "a" / "node_modules", 100)
    make_dir_with_size(tree / "b" / ".venv", 200)
    make_dir_with_size(tree / "c" / "__pycache__", 50)
    result = ReclaimableDirsCheck().run(tree)
    assert len(result.findings) == 3
    assert "350 B" in result.summary


def test_no_desciende_dentro_de_una_carpeta_regenerable(tree):
    # un __pycache__ anidado DENTRO de node_modules no debe contarse aparte
    make_dir_with_size(tree / "proj" / "node_modules" / "pkg" / "__pycache__", 30)
    result = ReclaimableDirsCheck().run(tree)
    assert len(result.findings) == 1
    assert result.findings[0].title.startswith("node_modules")


def test_ordena_por_tamano_descendente(tree):
    make_dir_with_size(tree / "small" / ".venv", 10)
    make_dir_with_size(tree / "big" / "node_modules", 1000)
    result = ReclaimableDirsCheck().run(tree)
    assert result.findings[0].size_bytes == 1000
    assert result.findings[1].size_bytes == 10


def test_arbol_limpio_sin_hallazgos(tree):
    write(tree, "src/main.py", "x = 1\n")
    result = ReclaimableDirsCheck().run(tree)
    assert result.findings == []
