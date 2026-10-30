"""Behavior and privacy checks for the standalone CSV profiler."""

import contextlib
import importlib.util
import io
import json
import tempfile
import unittest
from pathlib import Path
from unittest.mock import patch


SCRIPT = Path(__file__).resolve().parents[1] / ".agents/skills/data-check/profile_csv.py"
SPEC = importlib.util.spec_from_file_location("profile_csv", SCRIPT)
profile_csv = importlib.util.module_from_spec(SPEC)
SPEC.loader.exec_module(profile_csv)


class CsvProfileTests(unittest.TestCase):
    def setUp(self):
        self.workspace = tempfile.TemporaryDirectory()
        self.addCleanup(self.workspace.cleanup)
        self.folder = Path(self.workspace.name)
        self.source = self.folder / "source.csv"
        self.output = self.folder / "profile.json"

    def run_profile(self):
        errors = io.StringIO()
        with contextlib.redirect_stderr(errors):
            code = profile_csv.main(["--input", str(self.source), "--output", str(self.output)])
        return code, errors.getvalue()

    def test_bom_multiline_quoted_fields_and_missing_cells(self):
        self.source.write_bytes(
            '\ufeffname,notes,optional\r\n"secret, name","private\nline",\r\n'
            'other,"escaped ""quote""",present\r\n'.encode("utf-8")
        )
        code, errors = self.run_profile()
        self.assertEqual((code, errors), (0, ""))
        report = json.loads(self.output.read_text(encoding="utf-8"))
        self.assertEqual(report, {
            "columns": [
                {"name": "name", "missing_count": 0},
                {"name": "notes", "missing_count": 0},
                {"name": "optional", "missing_count": 1},
            ],
            "row_count": 2,
            "valid_row_count": 2,
            "invalid_width_row_count": 0,
        })
        serialized = self.output.read_text(encoding="utf-8")
        for secret in ("secret, name", "private", "escaped", "present", str(self.source)):
            self.assertNotIn(secret, serialized)

    def test_malformed_widths_are_counted_and_reported_with_nonzero_exit(self):
        self.source.write_text("a,b\n1,\nsecret\nx,y,z\n", encoding="utf-8")
        code, errors = self.run_profile()
        self.assertEqual((code, errors), (1, ""))
        report = json.loads(self.output.read_text(encoding="utf-8"))
        self.assertEqual(report["row_count"], 3)
        self.assertEqual(report["valid_row_count"], 1)
        self.assertEqual(report["invalid_width_row_count"], 2)
        self.assertEqual(report["columns"][1]["missing_count"], 1)
        self.assertNotIn("secret", self.output.read_text(encoding="utf-8"))

    def test_empty_and_duplicate_headers_reject_without_output(self):
        for contents in ("a,,b\n1,2,3\n", "a,a\n1,2\n", "\n"):
            with self.subTest(contents=contents):
                self.source.write_text(contents, encoding="utf-8")
                code, errors = self.run_profile()
                self.assertEqual(code, 2)
                self.assertIn("header", errors)
                self.assertFalse(self.output.exists())

    def test_byte_and_row_limits_reject_without_output(self):
        self.source.write_text("a\n123456\n", encoding="utf-8")
        with patch.object(profile_csv, "MAX_INPUT_BYTES", 5):
            code, errors = self.run_profile()
        self.assertEqual(code, 2)
        self.assertIn("byte limit", errors)
        self.assertFalse(self.output.exists())
        self.source.write_text("a\n1\n2\n", encoding="utf-8")
        with patch.object(profile_csv, "MAX_DATA_ROWS", 1):
            code, errors = self.run_profile()
        self.assertEqual(code, 2)
        self.assertIn("row limit", errors)
        self.assertFalse(self.output.exists())

    def test_invalid_utf8_and_csv_syntax_reject_without_leaking_values(self):
        for contents, expected in (
            (b"a\n\xff\n", "UTF-8"),
            (b'a\n"private unclosed\n', "CSV syntax"),
        ):
            with self.subTest(expected=expected):
                self.source.write_bytes(contents)
                code, errors = self.run_profile()
                self.assertEqual(code, 2)
                self.assertIn(expected, errors)
                self.assertNotIn("private", errors)
                self.assertNotIn(str(self.source), errors)
                self.assertFalse(self.output.exists())

    def test_preexisting_output_and_symlink_are_not_overwritten(self):
        self.source.write_text("a\n1\n", encoding="utf-8")
        self.output.write_text("keep", encoding="utf-8")
        code, _ = self.run_profile()
        self.assertEqual(code, 2)
        self.assertEqual(self.output.read_text(encoding="utf-8"), "keep")
        self.output.unlink()
        target = self.folder / "target.json"
        target.write_text("keep target", encoding="utf-8")
        self.output.symlink_to(target)
        code, _ = self.run_profile()
        self.assertEqual(code, 2)
        self.assertTrue(self.output.is_symlink())
        self.assertEqual(target.read_text(encoding="utf-8"), "keep target")

    def test_input_path_cannot_be_output_path(self):
        self.source.write_text("a\n1\n", encoding="utf-8")
        before = self.source.read_bytes()
        with contextlib.redirect_stderr(io.StringIO()):
            code = profile_csv.main(["--input", str(self.source), "--output", str(self.source)])
        self.assertEqual(code, 2)
        self.assertEqual(self.source.read_bytes(), before)


if __name__ == "__main__":
    unittest.main()
