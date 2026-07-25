from diskwhy.plugin import CheckResult, Finding
from diskwhy.report import build_report, write_json


def test_worst_severity_ninguno_si_no_hay_findings():
    report = build_report(".", [CheckResult(check_name="x", summary="ok")])
    assert report.worst_severity() is None


def test_worst_severity_toma_el_mas_grave():
    results = [
        CheckResult(
            check_name="x",
            summary="ok",
            findings=[Finding(severity="info", title="a"), Finding(severity="high", title="b")],
        )
    ]
    report = build_report(".", results)
    assert report.worst_severity() == "high"


def test_total_reclaimable_bytes_suma_todos_los_findings():
    results = [
        CheckResult(
            check_name="reclaimable_dirs",
            summary="ok",
            findings=[
                Finding(severity="info", title="a", size_bytes=100),
                Finding(severity="info", title="b", size_bytes=250),
            ],
        )
    ]
    report = build_report(".", results)
    assert report.total_reclaimable_bytes() == 350


def test_to_console_sin_emojis():
    results = [
        CheckResult(
            check_name="reclaimable_dirs",
            summary="1 hallazgo",
            findings=[Finding(severity="info", title="node_modules (1.0 GB)", path="/a/node_modules")],
        )
    ]
    report = build_report("/repo", results)
    out = report.to_console()
    assert "[INFO  ]" in out
    assert "🗑" not in out and "⚠" not in out


def test_to_json_valido():
    results = [CheckResult(check_name="x", summary="ok")]
    report = build_report("/repo", results)
    out = write_json(report)
    assert '"check_name": "x"' in out
