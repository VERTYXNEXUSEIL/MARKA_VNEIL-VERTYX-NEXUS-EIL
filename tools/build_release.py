#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile, ZipInfo

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
INCLUDE_PATHS = [
    "spec",
    "schemas",
    "test-vectors",
    "reference",
    "README.md",
    "LICENSE-CODE",
    "LICENSE-SPEC",
    "NOTICE",
    "PATENT-NOTICE.md",
]


def _sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def _git_commit() -> str:
    return subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()


def _schema_version_ids() -> dict[str, str | None]:
    out: dict[str, str | None] = {}
    for schema in sorted((ROOT / "schemas").glob("*.schema.json")):
        payload = json.loads(schema.read_text(encoding="utf-8"))
        out[schema.name] = payload.get("$id")
    return out


def _iter_release_files() -> list[Path]:
    files: list[Path] = []
    for entry in INCLUDE_PATHS:
        target = ROOT / entry
        if target.is_file():
            files.append(target)
            continue
        for path in sorted(target.rglob("*")):
            if path.is_file() and ".git" not in path.parts and "__pycache__" not in path.parts:
                files.append(path)
    return sorted(files, key=lambda p: p.relative_to(ROOT).as_posix())


def build_release(tag: str) -> dict[str, Path]:
    DIST.mkdir(exist_ok=True)
    files = _iter_release_files()

    manifest = {
        "tag": tag,
        "generated_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        "files": [
            {
                "path": path.relative_to(ROOT).as_posix(),
                "sha256": _sha256_file(path),
                "size": path.stat().st_size,
            }
            for path in files
        ],
    }

    manifest_path = DIST / "MANIFEST.json"
    manifest_path.write_text(json.dumps(manifest, indent=2) + "\n", encoding="utf-8")

    buildinfo = {
        "commit_sha": _git_commit(),
        "tag": tag,
        "generated_utc": manifest["generated_utc"],
        "python_version": platform.python_version(),
        "schema_version_ids": _schema_version_ids(),
    }
    buildinfo_path = DIST / "BUILDINFO.json"
    buildinfo_path.write_text(json.dumps(buildinfo, indent=2) + "\n", encoding="utf-8")

    archive_name = f"pca-spec-{tag}.zip"
    archive_path = DIST / archive_name
    with ZipFile(archive_path, "w", compression=ZIP_DEFLATED) as archive:
        for path in files:
            rel = path.relative_to(ROOT).as_posix()
            info = ZipInfo(rel)
            info.date_time = (1980, 1, 1, 0, 0, 0)
            info.external_attr = (0o644 & 0xFFFF) << 16
            info.compress_type = ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())

    sums_path = DIST / "SHA256SUMS"
    sums_lines = [
        f"{_sha256_file(archive_path)}  {archive_name}",
        f"{_sha256_file(manifest_path)}  MANIFEST.json",
    ]
    sums_path.write_text("\n".join(sums_lines) + "\n", encoding="utf-8")

    return {
        "archive": archive_path,
        "sha256sums": sums_path,
        "manifest": manifest_path,
        "buildinfo": buildinfo_path,
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Build self-verifying PCA release artifacts")
    parser.add_argument("--tag", default=os.environ.get("GITHUB_REF_NAME", "v1.0.0"))
    args = parser.parse_args()
    artifacts = build_release(args.tag)
    print(json.dumps({k: str(v.relative_to(ROOT)) for k, v in artifacts.items()}, indent=2))


if __name__ == "__main__":
    main()
