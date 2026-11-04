from __future__ import annotations

import argparse
import sys
from pathlib import Path

from diskwhy.plugin import SEVERITIES
from diskwhy.report import build_report, write_json
from diskwhy.runner import discover_checks, run_checks

_SEVERITY_ORDER = {sev: idx for idx, sev in enumerate(SEVERITIES)}


def _cmd_scan(args: argparse.Namespace) -> int:
    root = Path(args.path).resolve()
    only = set(args.only) if args.only else None
    skip = set(args.skip) if args.skip else None

    results = run_checks(root, only=only, skip=skip)
    report = build_report(root, results)

    if args.json:
        print(write_json(report))
    else:
        print(report.to_console())

    # Un check que revienta deja el análisis incompleto: antes solo se avisaba y salía 0 (o 1 según
    # --fail-on), y en un CI pasaba por verde sin haber mirado lo que ese check mira.
    failed = [r.check_name for r in results if r.error]
    if failed:
        print(f"error: no se pudieron ejecutar: {', '.join(failed)} (análisis incompleto)", file=sys.stderr)
        return 2

    if args.fail_on:
        worst = report.worst_severity()
        if worst is not None and _SEVERITY_ORDER[worst] >= _SEVERITY_ORDER[args.fail_on]:
            return 1
    return 0


def _cmd_list_checks(args: argparse.Namespace) -> int:
    for name, cls in sorted(discover_checks().items()):
        doc = (cls.__doc__ or "").strip().splitlines()[0] if cls.__doc__ else ""
        print(f"{name}: {doc}")
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="diskwhy")
    sub = parser.add_subparsers(dest="command", required=True)

    p_scan = sub.add_parser("scan", help="Analiza una carpeta en busca de espacio recuperable")
    p_scan.add_argument("path", nargs="?", default=".")
    p_scan.add_argument("--only", action="append", help="Ejecutar solo este check (repetible)")
    p_scan.add_argument("--skip", action="append", help="Saltar este check (repetible)")
    p_scan.add_argument("--json", action="store_true")
    p_scan.add_argument("--fail-on", choices=SEVERITIES, default=None)
    p_scan.set_defaults(func=_cmd_scan)

    p_list = sub.add_parser("list-checks", help="Lista los checks instalados")
    p_list.set_defaults(func=_cmd_list_checks)

    return parser


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
