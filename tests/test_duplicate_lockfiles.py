from conftest import write

from diskwhy.checks.duplicate_lockfiles import DuplicateLockfilesCheck


def test_lockfiles_identicos_se_agrupan(tree):
    write(tree / "proj-a", "package-lock.json", '{"deps": "same"}')
    write(tree / "proj-b", "package-lock.json", '{"deps": "same"}')
    result = DuplicateLockfilesCheck().run(tree)
    assert len(result.findings) == 1
    assert "2 lockfiles" in result.findings[0].title


def test_lockfiles_distintos_no_se_agrupan(tree):
    write(tree / "proj-a", "package-lock.json", '{"deps": "one"}')
    write(tree / "proj-b", "package-lock.json", '{"deps": "other"}')
    result = DuplicateLockfilesCheck().run(tree)
    assert result.findings == []


def test_ignora_node_modules(tree):
    write(tree / "proj" / "node_modules" / "pkg", "package-lock.json", '{"nested": true}')
    write(tree / "proj", "package-lock.json", '{"nested": true}')
    result = DuplicateLockfilesCheck().run(tree)
    # solo el de fuera de node_modules cuenta, asi que no hay duplicado
    assert result.findings == []


def test_sin_lockfiles(tree):
    write(tree, "src/main.py", "x=1\n")
    result = DuplicateLockfilesCheck().run(tree)
    assert result.findings == []
    assert "0 lockfile" in result.summary
