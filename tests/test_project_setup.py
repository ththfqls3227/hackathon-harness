"""Project-local setup must preserve the project and its existing files."""

import contextlib
import hashlib
import importlib.util
import io
import os
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch
from urllib.parse import unquote


SCRIPT = Path(__file__).resolve().parents[1] / "scripts/setup_project.py"
SPEC = importlib.util.spec_from_file_location("setup_project", SCRIPT)
setup = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(setup)


class ProjectSetupTests(unittest.TestCase):
    def setUp(self):
        workspace = tempfile.TemporaryDirectory()
        self.addCleanup(workspace.cleanup)
        self.project = Path(workspace.name) / "project space 한글"
        self.project.mkdir()
        self.source = self.project / "harness source 한글"
        for name in setup.REQUIRED:
            path = self.source / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text("source kept", encoding="utf-8")
        self.entry = self.project / ".agents/skills/hackathon-harness/SKILL.md"
        self.root_patch = patch.object(setup, "ROOT", self.source)
        self.root_patch.start()
        self.addCleanup(self.root_patch.stop)

    def run_setup(self, *args):
        out, err = io.StringIO(), io.StringIO()
        with contextlib.redirect_stdout(out), contextlib.redirect_stderr(err):
            code = setup.main(["--project", str(self.project), *args])
        return code, out.getvalue(), err.getvalue()

    def test_preview_does_not_mutate_and_apply_links_to_source(self):
        before = sorted(str(p.relative_to(self.project)) for p in self.project.rglob("*"))
        code, out, err = self.run_setup()
        self.assertEqual((code, err), (0, ""))
        self.assertIn("would create", out)
        self.assertEqual(before, sorted(str(p.relative_to(self.project)) for p in self.project.rglob("*")))
        code, out, err = self.run_setup("--apply")
        self.assertEqual((code, err), (0, ""))
        self.assertIn("created", out)
        text = self.entry.read_text(encoding="utf-8")
        self.assertTrue(text.startswith("---\nname: hackathon-harness\ndescription: "))
        link = text.split("[START.md](", 1)[1].split(")", 1)[0]
        self.assertIn("%20", link)
        self.assertIn("%ED", link)
        self.assertEqual((self.entry.parent / unquote(link)).resolve(), (self.source / "START.md").resolve())
        self.assertIn("상대경로", text)
        self.assertEqual((self.source / "START.md").read_text(encoding="utf-8"), "source kept")

    def test_identical_repeat_is_noop_and_existing_project_files_survive(self):
        agents = self.project / "AGENTS.md"
        config = self.project / ".codex/config.toml"
        config.parent.mkdir()
        agents.write_text("project instructions", encoding="utf-8")
        config.write_text("project config", encoding="utf-8")
        self.assertEqual(self.run_setup("--apply")[0], 0)
        watched = (self.entry, agents, config)
        before = {path: (hashlib.sha256(path.read_bytes()).digest(), path.stat().st_mtime_ns) for path in watched}
        code, out, err = self.run_setup("--apply")
        self.assertEqual((code, err), (0, ""))
        self.assertIn("already present", out)
        self.assertEqual(
            {path: (hashlib.sha256(path.read_bytes()).digest(), path.stat().st_mtime_ns) for path in watched},
            before,
        )
        self.assertEqual(agents.read_text(), "project instructions")
        self.assertEqual(config.read_text(), "project config")

    def test_differing_skill_and_unrelated_file_are_collisions(self):
        self.entry.parent.mkdir(parents=True)
        self.entry.write_text("keep existing", encoding="utf-8")
        self.assertEqual(self.run_setup()[0], 2)
        self.assertEqual(self.run_setup("--apply")[0], 2)
        self.assertEqual(self.entry.read_text(), "keep existing")
        self.entry.unlink()
        other = self.entry.parent / "notes.txt"
        other.write_text("keep", encoding="utf-8")
        self.assertEqual(self.run_setup("--apply")[0], 2)
        self.assertEqual(other.read_text(), "keep")
        self.assertFalse(self.entry.exists())

    def test_symlink_chain_and_broken_skill_symlink_are_rejected(self):
        external = Path(tempfile.mkdtemp())
        self.addCleanup(lambda: external.rmdir())
        (self.project / ".agents").symlink_to(external, target_is_directory=True)
        self.assertEqual(self.run_setup("--apply")[0], 2)
        self.assertEqual(list(external.iterdir()), [])
        (self.project / ".agents").unlink()
        self.entry.parent.mkdir(parents=True)
        self.entry.symlink_to(external / "absent")
        self.assertEqual(self.run_setup("--apply")[0], 2)
        self.assertFalse((external / "absent").exists())

    def test_missing_source_and_wrong_project_rejected(self):
        (self.source / "START.md").unlink()
        self.assertEqual(self.run_setup("--apply")[0], 2)
        self.assertFalse(self.entry.exists())
        (self.source / "START.md").write_text("restored", encoding="utf-8")
        outside = self.project.parent / "other"
        outside.mkdir()
        with contextlib.redirect_stderr(io.StringIO()):
            self.assertEqual(setup.main(["--project", str(outside), "--apply"]), 2)
            self.assertEqual(setup.main(["--project", str(self.source), "--apply"]), 2)
            self.assertEqual(setup.main(["--project", "/", "--apply"]), 2)
        self.assertFalse((outside / ".agents").exists())

    def test_required_source_symlinks_and_symlinked_parent_rejected(self):
        external_workspace = tempfile.TemporaryDirectory()
        self.addCleanup(external_workspace.cleanup)
        external = Path(external_workspace.name)
        target = external / "target"
        target.write_text("external kept", encoding="utf-8")
        for name in setup.REQUIRED:
            with self.subTest(name=name):
                required = self.source / name
                required.unlink()
                required.symlink_to(target)
                self.assertEqual(self.run_setup("--apply")[0], 2)
                self.assertFalse(self.entry.exists())
                self.assertEqual(target.read_text(), "external kept")
                required.unlink()
                required.write_text("source kept", encoding="utf-8")
        docs = self.source / "docs"
        (docs / "exam-contract.md").unlink()
        docs.rmdir()
        (external / "exam-contract.md").write_text("external kept", encoding="utf-8")
        docs.symlink_to(external, target_is_directory=True)
        self.assertEqual(self.run_setup("--apply")[0], 2)
        self.assertFalse(self.entry.exists())
        self.assertEqual((external / "exam-contract.md").read_text(), "external kept")

    def test_source_directory_symlink_rejected(self):
        alias = self.project / "source alias"
        alias.symlink_to(self.source, target_is_directory=True)
        with patch.object(setup, "ROOT", alias):
            self.assertEqual(self.run_setup("--apply")[0], 2)
        self.assertFalse(self.entry.exists())

    def test_write_failure_leaves_no_final_or_temp_and_retry_succeeds(self):
        with patch.object(setup.os, "fsync", side_effect=OSError(5, "private details")):
            code, _, error = self.run_setup("--apply")
        self.assertEqual(code, 2)
        self.assertNotIn("private details", error)
        self.assertFalse(self.entry.exists())
        self.assertEqual(list(self.entry.parent.iterdir()), [])
        self.assertEqual(self.run_setup("--apply")[0], 0)
        self.assertTrue(self.entry.is_file())

    def test_concurrent_final_is_never_overwritten(self):
        real_link = os.link

        def concurrent_link(*args, **kwargs):
            self.entry.write_text("concurrent winner", encoding="utf-8")
            return real_link(*args, **kwargs)

        with patch.object(setup.os, "link", side_effect=concurrent_link):
            code, _, error = self.run_setup("--apply")
            self.assertEqual(code, 2, error)
        self.assertTrue(self.entry.exists(), error)
        self.assertEqual(self.entry.read_text(), "concurrent winner")
        self.assertEqual([p.name for p in self.entry.parent.iterdir()], ["SKILL.md"])
        self.assertEqual(self.run_setup("--apply")[0], 2)

    def test_cleanup_failure_after_publish_allows_noop_retry(self):
        with patch.object(setup.os, "unlink", side_effect=OSError(5, "private details")):
            code, _, error = self.run_setup("--apply")
        self.assertEqual(code, 2)
        self.assertNotIn("private details", error)
        self.assertTrue(self.entry.is_file())
        before = self.entry.read_bytes()
        siblings = sorted(path.name for path in self.entry.parent.iterdir())
        self.assertEqual(len(siblings), 2)
        self.assertEqual(siblings[1], "SKILL.md")
        self.assertTrue(siblings[0].startswith(".setup-"))
        code, out, error = self.run_setup("--apply")
        self.assertEqual((code, error), (0, ""))
        self.assertIn("already present", out)
        self.assertEqual(self.entry.read_bytes(), before)
        self.assertEqual(sorted(path.name for path in self.entry.parent.iterdir()), siblings)


if __name__ == "__main__":
    unittest.main()
