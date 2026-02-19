#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
from pathlib import Path

from pca.execute import execute_certified
from pca.schemas import validate
from pca.testsuite import run_vectors


ROOT = Path(__file__).resolve().parents[2]
VECTOR_DIR = ROOT / "test-vectors" / "vectors-v1"
SCHEMAS = (
    "pc.schema.json",
    "constraints.schema.json",
    "action_ir.schema.json",
    "evidence_capsule.schema.json",
)


def cmd_execute(pc_path: Path, runtime_path: Path) -> int:
    pc = json.loads(pc_path.read_text(encoding="utf-8"))
    runtime = json.loads(runtime_path.read_text(encoding="utf-8"))
    print(json.dumps(execute_certified(pc, runtime), indent=2))
    return 0


def cmd_validate_schemas() -> int:
    for vec_path in sorted(VECTOR_DIR.glob("T*.json")):
        vec = json.loads(vec_path.read_text(encoding="utf-8"))
        validate(vec["pc"], "pc.schema.json")
        validate(
            {
                "version_id": vec["pc"]["constraints_version_id"],
                "effective_time": vec["pc"]["effective_time"],
                "payload": {"allow": ["transfer"]},
                "digest": vec["pc"]["constraints_digest"],
            },
            "constraints.schema.json",
        )
        validate(vec["pc"]["steps"][0], "action_ir.schema.json")
        validate(
            {
                "capsule_version": "1.0",
                "proofs": [{"type": "test", "digest": vec["expected_pc_digest"]}],
            },
            "evidence_capsule.schema.json",
        )

    print(f"validated schemas: {', '.join(SCHEMAS)}")
    print(f"vectors checked: {len(list(VECTOR_DIR.glob('T*.json')))}")
    return 0


def cmd_run_vectors() -> int:
    print(json.dumps(run_vectors(VECTOR_DIR), indent=2))
    return 0


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="PCA CLI verifier/executor")
    subparsers = parser.add_subparsers(dest="command")

    execute_parser = subparsers.add_parser("execute", help="execute a single PC/runtime pair")
    execute_parser.add_argument("pc", type=Path)
    execute_parser.add_argument("runtime", type=Path)

    subparsers.add_parser("validate-schemas", help="validate schemas against test vectors")
    subparsers.add_parser("run-vectors", help="run all test vectors")

    parser.add_argument("legacy_pc", type=Path, nargs="?")
    parser.add_argument("legacy_runtime", type=Path, nargs="?")
    return parser


def main() -> int:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "execute":
        return cmd_execute(args.pc, args.runtime)
    if args.command == "validate-schemas":
        return cmd_validate_schemas()
    if args.command == "run-vectors":
        return cmd_run_vectors()

    if args.legacy_pc and args.legacy_runtime:
        return cmd_execute(args.legacy_pc, args.legacy_runtime)

    parser.print_help()
    return 2


if __name__ == "__main__":
    raise SystemExit(main())
