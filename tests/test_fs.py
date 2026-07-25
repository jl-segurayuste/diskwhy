from conftest import make_dir_with_size

from diskwhy.fs import dir_size, human_size


def test_dir_size_suma_ficheros(tree):
    make_dir_with_size(tree / "a", 100)
    (tree / "a" / "b.bin").write_bytes(b"\0" * 50)
    assert dir_size(tree / "a") == 150


def test_dir_size_directorio_vacio(tree):
    (tree / "empty").mkdir()
    assert dir_size(tree / "empty") == 0


def test_dir_size_ignora_symlinks(tree):
    real = make_dir_with_size(tree / "real", 100)
    link = tree / "link"
    link.symlink_to(real / "data.bin")
    assert dir_size(tree) == 100  # el symlink no debe contarse aparte


def test_human_size_bytes():
    assert human_size(500) == "500 B"


def test_human_size_kb():
    assert human_size(2048) == "2.0 KB"


def test_human_size_mb():
    assert human_size(5 * 1024 * 1024) == "5.0 MB"


def test_human_size_gb():
    assert human_size(3 * 1024**3) == "3.0 GB"
