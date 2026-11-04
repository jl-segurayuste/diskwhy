from conftest import make_dir_with_size, write

from diskwhy.checks.reclaimable_dirs import ReclaimableDirsCheck


def test_detecta_node_modules(tree):
    make_dir_with_size(tree / "proj" / "node_modules", 1000)
    write(tree / "proj", "package.json", "{}")
    result = ReclaimableDirsCheck().run(tree)
    assert len(result.findings) == 1
    assert "node_modules" in result.findings[0].title


def test_detecta_varios_tipos(tree):
    make_dir_with_size(tree / "a" / "node_modules", 40960)
    make_dir_with_size(tree / "b" / ".venv", 81920)
    make_dir_with_size(tree / "c" / "__pycache__", 20480)
    result = ReclaimableDirsCheck().run(tree)
    assert len(result.findings) == 3
    assert "140.0 KB" in result.summary


def test_no_desciende_dentro_de_una_carpeta_regenerable(tree):
    # un __pycache__ anidado DENTRO de node_modules no debe contarse aparte
    make_dir_with_size(tree / "proj" / "node_modules" / "pkg" / "__pycache__", 30)
    result = ReclaimableDirsCheck().run(tree)
    assert len(result.findings) == 1
    assert result.findings[0].title.startswith("node_modules")


def test_ordena_por_tamano_descendente(tree):
    make_dir_with_size(tree / "small" / ".venv", 4096)
    make_dir_with_size(tree / "big" / "node_modules", 409600)
    result = ReclaimableDirsCheck().run(tree)
    assert result.findings[0].size_bytes == 409600
    assert result.findings[1].size_bytes == 4096


def test_arbol_limpio_sin_hallazgos(tree):
    write(tree, "src/main.py", "x = 1\n")
    result = ReclaimableDirsCheck().run(tree)
    assert result.findings == []


def test_build_con_codigo_versionado_no_es_regenerable(tree):
    import subprocess

    write(tree / "goapp", "build/package/Dockerfile", "FROM x\n")
    make_dir_with_size(tree / "goapp" / "build" / "node_modules", 100)
    subprocess.run(["git", "init", "-q"], cwd=tree / "goapp", check=True)
    subprocess.run(["git", "add", "build/package/Dockerfile"], cwd=tree / "goapp", check=True)
    titles = [f.title for f in ReclaimableDirsCheck().run(tree).findings]
    assert not any(t.startswith("build ") for t in titles)
    assert any(t.startswith("node_modules") for t in titles)      # se sigue mirando dentro


def test_build_sin_versionar_si_es_regenerable(tree):
    make_dir_with_size(tree / "p" / "build", 100)
    assert [f.title.split()[0] for f in ReclaimableDirsCheck().run(tree).findings] == ["build"]
