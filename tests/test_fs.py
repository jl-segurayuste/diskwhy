from conftest import make_dir_with_size

from diskwhy.fs import dir_size, human_size


def test_dir_size_suma_ficheros(tree):
    make_dir_with_size(tree / "a", 8192)
    (tree / "a" / "b.bin").write_bytes(b"\1" * 4096)
    assert dir_size(tree / "a") == 12288


def test_dir_size_directorio_vacio(tree):
    (tree / "empty").mkdir()
    assert dir_size(tree / "empty") == 0


def test_dir_size_ignora_symlinks(tree):
    real = make_dir_with_size(tree / "real", 8192)
    link = tree / "link"
    link.symlink_to(real / "data.bin")
    assert dir_size(tree) == 8192  # el symlink no debe contarse aparte


def test_human_size_bytes():
    assert human_size(500) == "500 B"


def test_human_size_kb():
    assert human_size(2048) == "2.0 KB"


def test_human_size_mb():
    assert human_size(5 * 1024 * 1024) == "5.0 MB"


def test_human_size_gb():
    assert human_size(3 * 1024**3) == "3.0 GB"


def test_dir_size_fichero_disperso_cuenta_lo_ocupado(tree):
    (tree / "vm").mkdir()
    with open(tree / "vm" / "disk.img", "wb") as f:
        f.truncate(1024**3)  # 1 GB aparente, casi nada en disco
    assert dir_size(tree / "vm") < 1024**2


def test_dir_size_enlaces_duros_cuentan_una_vez(tree):
    real = make_dir_with_size(tree / "store", 8192)
    for i in range(3):
        (real / f"link{i}").hardlink_to(real / "data.bin")
    assert dir_size(real) == 8192
