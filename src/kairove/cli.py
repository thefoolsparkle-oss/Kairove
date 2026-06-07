from __future__ import annotations

import argparse
import json
from pathlib import Path

from .core import ensure_project
from .p1 import run_p1_demo
from .p0b import build_manual_publish_package, import_candidate, run_basic_qa, run_p0b_demo


def _print_json(data: object) -> None:
    print(json.dumps(data, ensure_ascii=False, indent=2))


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="kairove", description="Kairove P0-B runtime tools")
    parser.add_argument("--root", default=".", help="Project root directory")
    sub = parser.add_subparsers(dest="command", required=True)

    init_cmd = sub.add_parser("init", help="Create folders, config JSON files, and SQLite schema")
    init_cmd.set_defaults(func=cmd_init)

    demo = sub.add_parser("p0b-demo", help="Run the complete offline P0-B production skeleton")
    demo.add_argument("--seed-text", required=True, help="Manual seed/source text")
    demo.add_argument("--title", required=True, help="Working title")
    demo.add_argument("--target-style", default="ordinary AI format adaptation", help="Target adaptation style")
    demo.set_defaults(func=cmd_p0b_demo)

    p1_demo = sub.add_parser("p1-demo", help="Run the P1 trend/source intelligence skeleton with honest live/fixture scout modes")
    p1_demo.add_argument("--goal", required=True, help="Research goal for autonomous query planning")
    p1_demo.add_argument("--manual-url", help="Optional auxiliary manual seed URL")
    p1_demo.add_argument("--scout-mode", choices=["auto", "fixture", "live"], default="auto", help="auto respects permissions, fixture is offline-only, live explicitly attempts metadata search")
    p1_demo.set_defaults(func=cmd_p1_demo)

    imp = sub.add_parser("import-candidate", help="Import a generated video candidate")
    imp.add_argument("--job-id", required=True)
    imp.add_argument("--file", required=True)
    imp.add_argument("--run-id")
    imp.set_defaults(func=cmd_import_candidate)

    qa = sub.add_parser("qa", help="Run basic P0-B QA for a candidate")
    qa.add_argument("--job-id", required=True)
    qa.add_argument("--candidate-id", required=True)
    qa.set_defaults(func=cmd_qa)

    package = sub.add_parser("package", help="Build manual publish package for a candidate")
    package.add_argument("--job-id", required=True)
    package.add_argument("--candidate-id", required=True)
    package.set_defaults(func=cmd_package)
    return parser


def cmd_init(args: argparse.Namespace) -> int:
    root = ensure_project(args.root)
    _print_json({"status": "initialized", "root": str(Path(root))})
    return 0


def cmd_p0b_demo(args: argparse.Namespace) -> int:
    _print_json(run_p0b_demo(args.root, args.seed_text, args.title, args.target_style))
    return 0


def cmd_p1_demo(args: argparse.Namespace) -> int:
    _print_json(run_p1_demo(args.root, args.goal, args.manual_url, scout_mode=args.scout_mode))
    return 0


def cmd_import_candidate(args: argparse.Namespace) -> int:
    candidate_id = import_candidate(args.root, args.job_id, args.file, run_id=args.run_id)
    _print_json({"candidate_id": candidate_id})
    return 0


def cmd_qa(args: argparse.Namespace) -> int:
    quality_report_id = run_basic_qa(args.root, args.job_id, args.candidate_id)
    _print_json({"quality_report_id": quality_report_id})
    return 0


def cmd_package(args: argparse.Namespace) -> int:
    package_id = build_manual_publish_package(args.root, args.job_id, args.candidate_id)
    _print_json({"publish_package_id": package_id})
    return 0


def main(argv: list[str] | None = None) -> int:
    parser = build_parser()
    args = parser.parse_args(argv)
    return args.func(args)
