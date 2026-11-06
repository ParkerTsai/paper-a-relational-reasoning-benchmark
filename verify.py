#!/usr/bin/env python3
"""Verify the downloaded archive parts or restored Paper A files, offline."""
from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
CHUNK = 1024 * 1024


def digest(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as stream:
        for block in iter(lambda: stream.read(CHUNK), b""):
            h.update(block)
    return h.hexdigest()


def load_json(path: Path) -> dict:
    with path.open(encoding="utf-8") as stream:
        value = json.load(stream)
    if not isinstance(value, dict):
        raise ValueError(f"Expected a JSON object: {path}")
    return value


def safe_relative(name: str) -> Path:
    value = PurePosixPath(name)
    if (not name or not value.parts or value.is_absolute() or "\\" in name
            or any(part in (".", "..") or ":" in part for part in value.parts)):
        raise ValueError(f"Unsafe archive path: {name!r}")
    return Path(*value.parts)


def verify_parts(directory: Path = HERE) -> dict:
    manifest = load_json(directory / "archive_manifest.json")
    combined = hashlib.sha256()
    total = 0
    errors = []
    for record in manifest["parts"]:
        path = directory / safe_relative(record["path"])
        if not path.is_file() or path.is_symlink():
            errors.append(f"Missing regular file: {record['path']}")
            continue
        actual = hashlib.sha256()
        size = 0
        with path.open("rb") as stream:
            for block in iter(lambda: stream.read(CHUNK), b""):
                actual.update(block)
                combined.update(block)
                size += len(block)
        total += size
        if size != record["size_bytes"] or actual.hexdigest() != record["sha256"]:
            errors.append(f"Size or SHA256 mismatch: {record['path']}")
    if total != manifest["archive_size_bytes"]:
        errors.append("Combined archive size does not match")
    if combined.hexdigest() != manifest["archive_sha256"]:
        errors.append("Combined archive SHA256 does not match")
    if errors:
        raise ValueError("\n".join(errors))
    return {"status": "PASS", "parts": len(manifest["parts"]),
            "bytes": total, "sha256": combined.hexdigest()}


def verify_files(root: Path, directory: Path = HERE, strict: bool = False) -> dict:
    manifest = load_json(directory / "file_manifest.json")
    errors = []
    expected = set()
    total = 0
    root = root.resolve()
    for record in manifest["files"]:
        relative = safe_relative(record["path"])
        expected.add(relative.as_posix())
        path = root / relative
        if path.is_symlink() or not path.is_file():
            errors.append(f"Missing regular file: {relative.as_posix()}")
            continue
        if root not in path.resolve().parents:
            errors.append(f"Path escapes data directory: {relative.as_posix()}")
            continue
        size = path.stat().st_size
        total += size
        if size != record["size_bytes"] or digest(path) != record["sha256"]:
            errors.append(f"Size or SHA256 mismatch: {relative.as_posix()}")
    if strict:
        actual = {p.relative_to(root).as_posix() for p in root.rglob("*") if p.is_file()}
        extras = sorted(actual - expected - {".restore-incomplete"})
        errors.extend(f"Unexpected file: {name}" for name in extras)
    if errors:
        raise ValueError("\n".join(errors[:100]) +
                         (f"\n... {len(errors)} total errors" if len(errors) > 100 else ""))
    return {"status": "PASS", "files": len(expected), "bytes": total,
            "root": str(root), "strict": strict}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--parts", action="store_true", help="Check archive parts without restoring")
    parser.add_argument("--data", type=Path, default=HERE / "restored", help="Restored data directory")
    parser.add_argument("--strict", action="store_true", help="Also reject unexpected restored files")
    args = parser.parse_args()
    try:
        result = verify_parts() if args.parts else verify_files(args.data, strict=args.strict)
    except (OSError, ValueError, KeyError) as error:
        print(f"FAIL: {error}")
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
