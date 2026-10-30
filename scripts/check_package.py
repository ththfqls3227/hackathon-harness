#!/usr/bin/env python3
"""Validate the explicit public file list, local links and skill metadata."""

import re
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def check():
    problems = []
    entries = (ROOT / "RELEASE_FILES.txt").read_text(encoding="utf-8").splitlines()
    files = [line for line in entries if line and not line.startswith("#")]
    if len(files) != len(set(files)):
        problems.append("duplicate release paths")
    for name in files:
        relative = Path(name)
        if relative.is_absolute() or ".." in relative.parts:
            problems.append("invalid release path")
            continue
        path = ROOT / relative
        if path.is_symlink() or not path.is_file():
            problems.append(f"missing file or symlink: {name}")
            continue
        if not path.resolve().is_relative_to(ROOT):
            problems.append(f"path escapes package: {name}")
            continue
        try:
            body = path.read_text(encoding="utf-8")
        except UnicodeError:
            problems.append(f"non-UTF-8 release file: {name}")
            continue
        for number, line in enumerate(body.splitlines(), 1):
            if line != line.rstrip():
                problems.append(f"trailing whitespace: {name}:{number}")
        if path.suffix == ".md":
            for link in re.findall(r"\[[^\]]*\]\(([^)]+)\)", body):
                if link.startswith(("https://", "http://", "#")):
                    continue
                target = (path.parent / link.split("#")[0]).resolve()
                if not target.is_relative_to(ROOT) or not target.is_file():
                    problems.append(f"broken or external local link: {name}")
        if path.name == "SKILL.md":
            parts = body.split("---", 2)
            if len(parts) != 3 or parts[0].strip():
                problems.append(f"missing frontmatter: {name}")
                continue
            fields = dict(re.findall(r"^(name|description):\s*(.+)$", parts[1], re.M))
            if fields.get("name") != path.parent.name or not fields.get("description"):
                problems.append(f"invalid skill metadata: {name}")
    for directory in (".agents", "roles", "templates", "scripts", "tests", "docs"):
        for path in (ROOT / directory).rglob("*"):
            if path.is_file() and "__pycache__" not in path.parts:
                if path.relative_to(ROOT).as_posix() not in files:
                    problems.append(f"unlisted package file: {path.relative_to(ROOT)}")
    return files, problems


if __name__ == "__main__":
    release_files, errors = check()
    for error in errors:
        print(error, file=sys.stderr)
    if errors:
        raise SystemExit(1)
    print(f"PASS: {len(release_files)} release files, local links and skill metadata")
