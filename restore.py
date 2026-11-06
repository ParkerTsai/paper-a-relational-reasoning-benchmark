#!/usr/bin/env python3
"""Restore and hash-check the Paper A release. Python 3.10+, standard library only."""
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import tarfile
import tempfile
from pathlib import Path

from verify import HERE, CHUNK, load_json, safe_relative, verify_files


def restore(output: Path) -> dict:
    archive = load_json(HERE / "archive_manifest.json")
    files = load_json(HERE / "file_manifest.json")
    expected = {r["path"]: r for r in files["files"]}
    if len(expected) != len(files["files"]):
        raise ValueError("Duplicate paths in file manifest")
    output = output.resolve()
    if output.exists() and (not output.is_dir() or any(output.iterdir())):
        raise ValueError(f"Choose an empty output directory: {output}")
    combined = hashlib.sha256()
    total = 0
    with tempfile.TemporaryFile() as joined:
        for part in archive["parts"]:
            path = HERE / safe_relative(part["path"])
            if path.is_symlink() or not path.is_file():
                raise ValueError(f"Missing regular archive part: {part['path']}")
            part_digest = hashlib.sha256()
            size = 0
            with path.open("rb") as stream:
                for block in iter(lambda: stream.read(CHUNK), b""):
                    joined.write(block)
                    combined.update(block)
                    part_digest.update(block)
                    size += len(block)
            if size != part["size_bytes"] or part_digest.hexdigest() != part["sha256"]:
                raise ValueError(f"Archive part failed verification: {part['path']}")
            total += size
            print(f"Verified {part['path']}", flush=True)
        if total != archive["archive_size_bytes"] or combined.hexdigest() != archive["archive_sha256"]:
            raise ValueError("Combined archive failed verification")
        joined.seek(0)
        output.mkdir(parents=True, exist_ok=True)
        marker = output / ".restore-incomplete"
        marker.write_text("Restoration is not complete.\n", encoding="utf-8")
        seen = set()
        with tarfile.open(fileobj=joined, mode="r|gz") as tar:
            for member in tar:
                relative = safe_relative(member.name)
                target = output / relative
                if member.isdir():
                    target.mkdir(parents=True, exist_ok=True)
                    continue
                if not member.isfile():
                    raise ValueError(f"Links and special archive members are prohibited: {member.name}")
                if member.name not in expected or member.name in seen:
                    raise ValueError(f"Unexpected or duplicate member: {member.name}")
                if member.size != expected[member.name]["size_bytes"]:
                    raise ValueError(f"Unexpected archive member size: {member.name}")
                target.parent.mkdir(parents=True, exist_ok=True)
                stream = tar.extractfile(member)
                if stream is None:
                    raise ValueError(f"Cannot read member: {member.name}")
                with stream, target.open("xb") as destination:
                    shutil.copyfileobj(stream, destination, CHUNK)
                seen.add(member.name)
        if seen != set(expected):
            raise ValueError(f"Missing {len(set(expected) - seen)} archive members")
    result = verify_files(output, strict=True)
    marker.unlink()
    result.update({"archive_sha256": combined.hexdigest(), "network_calls": 0})
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", type=Path, default=HERE / "restored", help="Empty restoration directory")
    args = parser.parse_args()
    try:
        result = restore(args.output)
    except (OSError, ValueError, KeyError, tarfile.TarError) as error:
        print(f"FAIL: {error}")
        return 1
    print(json.dumps(result, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
