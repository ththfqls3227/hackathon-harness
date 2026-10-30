#!/usr/bin/env python3
"""Produce a small, value-free profile of an explicitly named CSV file."""

import argparse
import csv
import io
import json
import os
import sys
from pathlib import Path


MAX_INPUT_BYTES = 8 * 1024 * 1024
MAX_DATA_ROWS = 100_000


class ProfileError(Exception):
    """An input or output error whose details must not expose data."""


def profile(input_path: Path) -> dict:
    try:
        with input_path.open("rb") as source:
            raw = source.read(MAX_INPUT_BYTES + 1)
    except OSError as exc:
        raise ProfileError("cannot read input") from exc
    if len(raw) > MAX_INPUT_BYTES:
        raise ProfileError("input exceeds byte limit")
    try:
        content = raw.decode("utf-8-sig")
    except UnicodeError as exc:
        raise ProfileError("input is not UTF-8") from exc

    try:
        rows = csv.reader(io.StringIO(content, newline=""), strict=True)
        header = next(rows, None)
        if not header or any(not label.strip() for label in header):
            raise ProfileError("header is missing or empty")
        if len(set(header)) != len(header):
            raise ProfileError("header contains duplicates")

        missing = [0] * len(header)
        row_count = 0
        invalid_rows = 0
        for row in rows:
            row_count += 1
            if row_count > MAX_DATA_ROWS:
                raise ProfileError("input exceeds row limit")
            if len(row) != len(header):
                invalid_rows += 1
                continue
            for index, value in enumerate(row):
                if value == "":
                    missing[index] += 1
    except csv.Error as exc:
        raise ProfileError("CSV syntax is invalid") from exc

    return {
        "columns": [{"name": label, "missing_count": count}
                    for label, count in zip(header, missing)],
        "row_count": row_count,
        "valid_row_count": row_count - invalid_rows,
        "invalid_width_row_count": invalid_rows,
    }


def write_new_json(output_path: Path, report: dict) -> None:
    payload = json.dumps(report, ensure_ascii=False, sort_keys=True, indent=2) + "\n"
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    try:
        descriptor = os.open(output_path, flags, 0o600)
    except OSError as exc:
        raise ProfileError("cannot create new output") from exc
    with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as target:
        target.write(payload)


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--input", required=True, type=Path, help="explicit CSV input path")
    parser.add_argument("--output", required=True, type=Path, help="new JSON output path")
    args = parser.parse_args(argv)
    try:
        report = profile(args.input)
        write_new_json(args.output, report)
    except ProfileError as exc:
        print(f"data-check: {exc}", file=sys.stderr)
        return 2
    except OSError:
        print("data-check: cannot write output", file=sys.stderr)
        return 2
    return 1 if report["invalid_width_row_count"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
