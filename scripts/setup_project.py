#!/usr/bin/env python3
"""Add a small, project-local entry point to this harness."""

import argparse
import os
import secrets
import stat
import sys
from pathlib import Path
from urllib.parse import quote


ROOT = Path(__file__).resolve().parents[1]
REQUIRED = (
    "START.md",
    "AGENTS.md",
    "docs/exam-contract.md",
    ".agents/skills/task-flow/SKILL.md",
)
DESTINATION = (".agents", "skills", "hackathon-harness")
POSIX_SUPPORTED = all(hasattr(os, name) for name in ("O_DIRECTORY", "O_NOFOLLOW", "supports_dir_fd")) and all(
    function in os.supports_dir_fd for function in (os.mkdir, os.open, os.link, os.unlink)
)


class SetupError(Exception):
    pass


def validate(project):
    if not project.is_dir() or project.is_symlink():
        raise SetupError("project must be an existing directory")
    raw_project, raw_source = project.absolute(), ROOT.absolute()
    project = project.resolve()
    source = ROOT.resolve()
    if project in (Path("/"), Path.home().resolve(), source):
        raise SetupError("unsafe project directory")
    if not source.is_relative_to(project) or source == project:
        raise SetupError("harness source must be strictly inside the project")
    if raw_source.is_relative_to(raw_project):
        current = raw_project
        for part in raw_source.relative_to(raw_project).parts:
            current = current / part
            if not stat.S_ISDIR(current.lstat().st_mode):
                raise SetupError("harness source contains a symlink or non-directory")
    for name in REQUIRED:
        current = source
        parts = Path(name).parts
        for part in parts[:-1]:
            current = current / part
            try:
                mode = current.lstat().st_mode
            except FileNotFoundError:
                raise SetupError("harness source is missing a required file") from None
            if not stat.S_ISDIR(mode):
                raise SetupError("harness source contains a symlink or non-directory")
        leaf = current / parts[-1]
        try:
            mode = leaf.lstat().st_mode
        except FileNotFoundError:
            raise SetupError("harness source is missing a required file") from None
        if not stat.S_ISREG(mode) or not leaf.resolve().is_relative_to(source):
            raise SetupError("harness source contains a symlink or non-file")
    return project, source


def skill_bytes(project, source):
    parent = project.joinpath(*DESTINATION)
    relative = Path(os.path.relpath(source / "START.md", parent))
    link = quote(relative.as_posix(), safe="/.")
    return (
        "---\n"
        "name: hackathon-harness\n"
        "description: 해커톤 과제를 시작하거나 재개할 때 응시 규정과 작업 흐름을 확인하고 필요한 스킬로 안내합니다.\n"
        "---\n\n"
        "# Hackathon harness\n\n"
        f"과제를 시작하거나 재개하기 전에 원본 하네스의 [START.md]({link})를 읽으세요.\n"
        "START.md에서 연결하는 파일의 상대경로는 각 원본 파일이 있는 폴더를 기준으로 해석하세요.\n"
    ).encode("utf-8")


def inspect_destination(project, expected):
    current = project
    for part in DESTINATION:
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            return False
        if not stat.S_ISDIR(mode):
            raise SetupError("destination contains a symlink or non-directory")
    skill = current / "SKILL.md"
    try:
        mode = skill.lstat().st_mode
    except FileNotFoundError:
        if any(current.iterdir()):
            raise SetupError("destination entry contains another file")
        return False
    if not stat.S_ISREG(mode):
        raise SetupError("destination skill is a symlink or non-file")
    if skill.read_bytes() != expected:
        raise SetupError("destination skill already differs")
    return True


def apply(project, expected):
    if not POSIX_SUPPORTED:
        raise SetupError("project setup needs POSIX directory operations; read START.md directly")
    flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    fd = os.open(project, flags)
    try:
        for part in DESTINATION:
            try:
                os.mkdir(part, dir_fd=fd)
            except FileExistsError:
                pass
            child_fd = os.open(part, flags, dir_fd=fd)
            os.close(fd)
            fd = child_fd
        names = os.listdir(fd)
        if any(name != "SKILL.md" for name in names):
            raise SetupError("destination entry contains another file")
        temporary = f".setup-{secrets.token_hex(16)}"
        temp_fd = os.open(
            temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o644, dir_fd=fd,
        )
        try:
            with os.fdopen(temp_fd, "wb") as output:
                output.write(expected)
                output.flush()
                os.fsync(output.fileno())
            try:
                os.link(temporary, "SKILL.md", src_dir_fd=fd, dst_dir_fd=fd, follow_symlinks=False)
            except FileExistsError:
                raise SetupError("destination skill appeared during setup") from None
            return "created"
        finally:
            os.unlink(temporary, dir_fd=fd)
    finally:
        os.close(fd)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--apply", action="store_true", help="create the project-local entry skill")
    args = parser.parse_args(argv)
    try:
        project, source = validate(args.project)
        expected = skill_bytes(project, source)
        present = inspect_destination(project, expected)
        if present:
            result = "already present"
        elif args.apply:
            result = apply(project, expected)
        else:
            result = "would create"
        print(f"{result}: {project.joinpath(*DESTINATION, 'SKILL.md')}")
        return 0
    except (SetupError, OSError) as error:
        message = str(error) if isinstance(error, SetupError) else (
            f"filesystem operation failed: {os.strerror(error.errno)}" if error.errno else "filesystem operation failed"
        )
        print(f"setup error: {message}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
