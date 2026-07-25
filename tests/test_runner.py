from conftest import make_dir_with_size

from diskwhy.runner import discover_checks, run_checks


def test_discover_checks_incluye_los_builtin():
    checks = discover_checks()
    expected = {"reclaimable_dirs", "orphaned_envs", "duplicate_lockfiles", "docker_reclaimable"}
    assert expected <= set(checks)


def test_run_checks_devuelve_un_resultado_por_check(tree):
    make_dir_with_size(tree / "a" / "node_modules", 100)
    results = run_checks(tree, only={"reclaimable_dirs", "orphaned_envs"})
    names = {r.check_name for r in results}
    assert names == {"reclaimable_dirs", "orphaned_envs"}


def test_run_checks_skip_excluye(tree):
    results = run_checks(tree, only={"reclaimable_dirs", "orphaned_envs"}, skip={"orphaned_envs"})
    names = {r.check_name for r in results}
    assert "orphaned_envs" not in names
    assert "reclaimable_dirs" in names


def test_run_checks_captura_excepcion_de_un_check_roto(tree, monkeypatch):
    import diskwhy.runner as runner_module

    class BrokenCheck:
        name = "broken"

        def run(self, root):
            raise RuntimeError("boom")

    monkeypatch.setattr(runner_module, "discover_checks", lambda: {"broken": BrokenCheck})
    results = run_checks(tree)
    assert len(results) == 1
    assert results[0].error is not None
    assert "boom" in results[0].summary
