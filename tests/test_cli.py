from conftest import make_dir_with_size

from diskwhy.cli import main


def test_scan_arbol_limpio_exit_0(tree, capsys):
    rc = main(["scan", str(tree), "--fail-on", "high"])
    assert rc == 0


def test_scan_con_venv_huerfano_exit_1_con_fail_on_high(tree, capsys):
    make_dir_with_size(tree / "old" / ".venv", 100)
    rc = main(["scan", str(tree), "--fail-on", "high"])
    assert rc == 1


def test_scan_json_produce_json_valido(tree, capsys):
    main(["scan", str(tree), "--json"])
    out = capsys.readouterr().out
    assert '"check_name"' in out


def test_scan_only_reclaimable_dirs(tree, capsys):
    make_dir_with_size(tree / "a" / "node_modules", 100)
    main(["scan", str(tree), "--only", "reclaimable_dirs"])
    out = capsys.readouterr().out
    assert "reclaimable_dirs" in out
    assert "orphaned_envs" not in out


def test_list_checks_incluye_los_cuatro(capsys):
    main(["list-checks"])
    out = capsys.readouterr().out
    assert "reclaimable_dirs" in out
    assert "orphaned_envs" in out
    assert "duplicate_lockfiles" in out
    assert "docker_reclaimable" in out


def test_check_que_revienta_sale_2(tmp_path, monkeypatch, capsys):
    from diskwhy import cli
    from diskwhy.plugin import CheckResult

    monkeypatch.setattr(cli, "run_checks", lambda *a, **k: [
        CheckResult(check_name="roto", summary="El check falló", error="Traceback..."),
    ])
    assert cli.main(["scan", str(tmp_path)]) == 2
    assert "roto" in capsys.readouterr().err
