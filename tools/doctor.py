#!/usr/bin/env python3
"""Run project health checks with a clear PASS/FAIL summary."""

from __future__ import annotations

import os
import shutil
import subprocess
import sys
from dataclasses import dataclass, field
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


@dataclass
class Step:
    name: str
    cmd: list[str]
    cwd: Path = ROOT
    env: dict[str, str] = field(default_factory=dict)
    optional: bool = False
    skip_reason: str = ""


@dataclass
class StepResult:
    step: Step
    status: str
    returncode: int


def run_step(step: Step) -> StepResult:
    if step.optional and step.skip_reason:
        print(f"\n--- {step.name} ---")
        print(f"SKIP: {step.skip_reason}")
        return StepResult(step=step, status="SKIP", returncode=0)

    print(f"\n--- {step.name} ---")
    print(f"$ {' '.join(step.cmd)}")
    env = os.environ.copy()
    env.update(step.env)
    completed = subprocess.run(step.cmd, cwd=step.cwd, env=env)
    status = "PASS" if completed.returncode == 0 else "FAIL"
    return StepResult(step=step, status=status, returncode=completed.returncode)


def main() -> int:
    pythonpath = str(ROOT / "reference/python")
    node_available = shutil.which("node") is not None
    node_script = ROOT / "reference/js/run_t13.mjs"

    steps = [
        Step(
            name="Validate schemas",
            cmd=["python", "reference/cli/pca_cli.py", "validate-schemas"],
            env={"PYTHONPATH": pythonpath},
        ),
        Step(
            name="Run vectors",
            cmd=["python", "reference/cli/pca_cli.py", "run-vectors"],
            env={"PYTHONPATH": pythonpath},
        ),
        Step(
            name="Python tests",
            cmd=["python", "-m", "pytest", "-q"],
            cwd=ROOT / "reference/python",
        ),
        Step(
            name="Ruff lint",
            cmd=["ruff", "check", "."],
            cwd=ROOT / "reference/python",
        ),
    ]

    node_skip_reason = ""
    if not node_available:
        node_skip_reason = "node is not available on PATH"
    elif not node_script.exists():
        node_skip_reason = f"{node_script.relative_to(ROOT)} not found"

    steps.append(
        Step(
            name="Node T13 runner",
            cmd=["node", "reference/js/run_t13.mjs"],
            optional=True,
            skip_reason=node_skip_reason,
        )
    )

    results = [run_step(step) for step in steps]

    print("\n=== doctor summary ===")
    for result in results:
        print(f"{result.status:>4} | {result.step.name}")

    has_failures = any(result.status == "FAIL" for result in results)
    return 1 if has_failures else 0


if __name__ == "__main__":
    sys.exit(main())
