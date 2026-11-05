#!/usr/bin/env python3
"""Fetch a pinned public source repository into the task project, without installing it."""

import argparse
import os
from pathlib import Path
import subprocess
import sys

from setup_project import SetupError, validate


SOURCES = {
    "omx": ("Yeachan-Heo/oh-my-codex", "a60b9435a8e6d894ba69d1540ecf20afaac63a7a"),
    "codexclaw": ("lidge-jun/codexclaw", "a7ff3b6b1e8221dc9be4f665f26b50270854b951"),
    "anatomy": ("wheresryan22/anatomy", "1482e8469b0a9e0d8cc18ea2740a01423d29ae80"),
    "superpowers": ("obra/superpowers", "2ce8aa15d05bd57213e6f746f953aafb7ded7a8b"),
    "ui-ux-pro-max": ("nextlevelbuilder/ui-ux-pro-max-skill", "28b3b8dee8c976df4fa3e94aed4e092ad43fcb03"),
    "mattpocock": ("mattpocock/skills", "a496f5513d4a4cf889bc48e189e579f4b0bdf6aa"),
    "scientific": ("K-Dense-AI/scientific-agent-skills", "5f2bc0341354fd5590aef76a533ada1e1e5b4e62"),
}


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--project", required=True, type=Path)
    parser.add_argument("--name", required=True, choices=SOURCES)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args(argv)
    target = None
    try:
        project, _ = validate(args.project)
        parent = project / "tools" / "upstream"
        for path in (project / "tools", parent):
            if path.is_symlink() or (path.exists() and not path.is_dir()):
                raise SetupError("source parent is a symlink or non-directory")
        target = parent / args.name
        if target.exists() or target.is_symlink():
            raise SetupError("destination already exists; preserve and inspect it")
        repo, revision = SOURCES[args.name]
        print(f"Source: https://github.com/{repo} @ {revision}")
        print(f"Destination: {target}")
        if not args.apply:
            print("Preview only; no download or filesystem changes. Use --apply to fetch.")
            return 0
        parent.mkdir(parents=True, exist_ok=True)
        target.mkdir()  # Exclusive creation: never overwrite an existing checkout.
        env = os.environ.copy()
        for key in list(env):
            if key.startswith("GIT_") or key in {"GH_TOKEN", "GITHUB_TOKEN", "SSH_ASKPASS"}:
                env.pop(key, None)
        env.update(GIT_CONFIG_NOSYSTEM="1", GIT_CONFIG_GLOBAL=os.devnull, GIT_TERMINAL_PROMPT="0")
        git = ["git", "-c", f"core.hooksPath={os.devnull}", "-c", "credential.helper="]

        def run(*command):
            return subprocess.run(git + list(command), cwd=target, env=env, check=True,
                                  capture_output=True, text=True, timeout=120).stdout.strip()

        run("init", "--quiet", "--template=")
        run("fetch", "--quiet", "--depth=1", f"https://github.com/{repo}.git", revision)
        if run("rev-parse", "FETCH_HEAD") != revision:
            raise SetupError("fetched revision does not match the pinned source")
        run("checkout", "--quiet", "--detach", revision)
        print("Fetched original source and license files. No plugin, hook, or dependency was installed.")
        return 0
    except (SetupError, OSError, subprocess.SubprocessError) as error:
        detail = str(error) if isinstance(error, SetupError) else type(error).__name__
        print(f"Fetch stopped: {detail}. Any created source directory is preserved; inspect before retrying.",
              file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
