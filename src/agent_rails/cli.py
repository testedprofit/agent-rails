"""Command line interface for Agent Rails."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

from .checks import render_report, run_checks
from .templates import TEMPLATES


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)

    if args.command == "init":
        return init_command(Path(args.path), force=args.force)
    if args.command == "check":
        try:
            changed_files = load_changed_files(args.changed_files, args.changed_files_list)
        except OSError as error:
            print(f"error: could not read changed files list: {error}", file=sys.stderr)
            return 2
        return check_command(Path(args.path), report_path=args.report, strict=args.strict, changed_files=changed_files)

    parser.print_help()
    return 2


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="agent-rails",
        description="Portable guardrails for AI-assisted repositories.",
    )
    subparsers = parser.add_subparsers(dest="command")

    init_parser = subparsers.add_parser("init", help="Install Agent Rails markdown files into a project.")
    init_parser.add_argument("path", nargs="?", default=".", help="Project path to initialize.")
    init_parser.add_argument("--force", action="store_true", help="Overwrite existing rail files.")

    check_parser = subparsers.add_parser("check", help="Run Agent Rails checks.")
    check_parser.add_argument("path", nargs="?", default=".", help="Project path to check.")
    check_parser.add_argument("--report", help="Write a markdown report to this path.")
    check_parser.add_argument("--strict", action="store_true", help="Treat warnings as failures.")
    check_parser.add_argument(
        "--changed-files",
        nargs="*",
        help="Limit gate, sensitive-value, and risk scans to these changed files while keeping required-doc checks global.",
    )
    check_parser.add_argument(
        "--changed-files-list",
        help="Read newline-delimited changed files from this path.",
    )

    return parser


def init_command(path: Path, *, force: bool) -> int:
    target = path.resolve()
    target.mkdir(parents=True, exist_ok=True)

    created = 0
    skipped = 0

    for relative_name, content in TEMPLATES.items():
        output_path = target / relative_name
        if output_path.exists() and not force:
            skipped += 1
            print(f"skip {relative_name} (already exists)")
            continue

        output_path.write_text(content.rstrip() + "\n", encoding="utf-8")
        created += 1
        print(f"write {relative_name}")

    print(f"Agent Rails init complete: {created} written, {skipped} skipped.")
    return 0


def check_command(
    path: Path,
    *,
    report_path: str | None,
    strict: bool,
    changed_files: tuple[str, ...] | None = None,
) -> int:
    root = path.resolve()
    if not root.exists():
        print(f"error: path does not exist: {root}", file=sys.stderr)
        return 2

    results = run_checks(root, changed_files=changed_files)
    report = render_report(results)
    failures = [result for result in results if result.is_failure]
    warnings = [result for result in results if result.is_warning]

    if report_path:
        Path(report_path).write_text(report, encoding="utf-8")

    print(f"Agent Rails checked {root}")
    print(f"failures={len(failures)} warnings={len(warnings)}")

    for result in failures[:10]:
        location = f" {result.path}:{result.line}" if result.path and result.line else ""
        print(f"FAIL {result.name}{location} - {result.message}")

    for result in warnings[:10]:
        location = f" {result.path}:{result.line}" if result.path and result.line else ""
        print(f"WARN {result.name}{location} - {result.message}")

    if failures or (strict and warnings):
        return 1
    return 0


def load_changed_files(changed_files: list[str] | None, changed_files_list: str | None) -> tuple[str, ...] | None:
    if changed_files is None and changed_files_list is None:
        return None

    loaded: list[str] = list(changed_files or [])
    if changed_files_list:
        lines = Path(changed_files_list).read_text(encoding="utf-8").splitlines()
        loaded.extend(line.strip() for line in lines if line.strip())

    return tuple(loaded)


if __name__ == "__main__":
    raise SystemExit(main())
