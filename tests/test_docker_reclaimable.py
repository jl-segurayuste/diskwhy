import subprocess

import diskwhy.checks.docker_reclaimable as docker_module
from diskwhy.checks.docker_reclaimable import DockerReclaimableCheck


def test_docker_no_instalado(tmp_path, monkeypatch):
    monkeypatch.setattr(docker_module.shutil, "which", lambda cmd: None)
    result = DockerReclaimableCheck().run(tmp_path)
    assert result.findings == []
    assert "no aplica" in result.summary.lower()


def test_docker_con_espacio_reclamable(tmp_path, monkeypatch):
    monkeypatch.setattr(docker_module.shutil, "which", lambda cmd: "/usr/bin/docker")
    fake_output = (
        '{"Type":"Images","Size":"2GB","Reclaimable":"1.5GB (75%)"}\n'
        '{"Type":"Containers","Size":"0B","Reclaimable":"0B (0%)"}\n'
    )

    def fake_run(*a, **k):
        return subprocess.CompletedProcess(a, 0, stdout=fake_output, stderr="")

    monkeypatch.setattr(docker_module.subprocess, "run", fake_run)
    result = DockerReclaimableCheck().run(tmp_path)
    assert len(result.findings) == 1
    assert "Images" in result.findings[0].title


def test_docker_comando_falla(tmp_path, monkeypatch):
    monkeypatch.setattr(docker_module.shutil, "which", lambda cmd: "/usr/bin/docker")

    def fake_run(*a, **k):
        return subprocess.CompletedProcess(a, 1, stdout="", stderr="daemon not running")

    monkeypatch.setattr(docker_module.subprocess, "run", fake_run)
    result = DockerReclaimableCheck().run(tmp_path)
    assert result.findings == []
    assert "no aplica" in result.summary.lower()


def test_docker_timeout(tmp_path, monkeypatch):
    monkeypatch.setattr(docker_module.shutil, "which", lambda cmd: "/usr/bin/docker")

    def fake_run(*a, **k):
        raise subprocess.TimeoutExpired(cmd="docker", timeout=15)

    monkeypatch.setattr(docker_module.subprocess, "run", fake_run)
    result = DockerReclaimableCheck().run(tmp_path)
    assert result.findings == []
