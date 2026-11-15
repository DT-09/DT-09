"""Unit tests for the portfolio integrity validator."""

from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_portfolio.py"
SPEC = importlib.util.spec_from_file_location("validate_portfolio", MODULE_PATH)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(validator)


class AnchorTests(unittest.TestCase):
    def test_heading_slug(self) -> None:
        self.assertEqual(
            validator.heading_slug("A mind for questions & systems"),
            "a-mind-for-questions-systems",
        )

    def test_duplicate_headings_get_github_suffixes(self) -> None:
        anchors, duplicates = validator.document_anchors("# Overview\n\n## Overview\n")
        self.assertIn("overview", anchors)
        self.assertIn("overview-1", anchors)
        self.assertEqual(duplicates, [])

    def test_fenced_code_is_not_indexed(self) -> None:
        fence = chr(96) * 3
        anchors, _ = validator.document_anchors(
            "# Real heading\n\n" + fence + "md\n## Fake heading\n" + fence + "\n"
        )
        self.assertIn("real-heading", anchors)
        self.assertNotIn("fake-heading", anchors)


class DocumentTests(unittest.TestCase):
    def test_checks_fragments_in_other_documents(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("[Research](RESEARCH.md#method)\n", encoding="utf-8")
            (root / "RESEARCH.md").write_text("# Method\n", encoding="utf-8")
            errors = validator.validate_document(root / "README.md", root, {})
            self.assertEqual(errors, [])

    def test_reports_missing_cross_document_fragment(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            (root / "README.md").write_text("[Research](RESEARCH.md#missing)\n", encoding="utf-8")
            (root / "RESEARCH.md").write_text("# Method\n", encoding="utf-8")
            errors = validator.validate_document(root / "README.md", root, {})
            self.assertTrue(any("missing anchor" in error for error in errors))

    def test_reports_broken_local_link(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            readme = root / "README.md"
            readme.write_text("[Missing](missing.md)\n", encoding="utf-8")
            errors = validator.validate_document(readme, root, {})
            self.assertTrue(any("broken local link" in error for error in errors))


class SvgTests(unittest.TestCase):
    def test_valid_accessible_svg(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "valid.svg"
            path.write_text(
                '<svg xmlns="http://www.w3.org/2000/svg" role="img" aria-labelledby="t d" viewBox="0 0 10 10">'
                '<title id="t">Title</title><desc id="d">Description</desc></svg>',
                encoding="utf-8",
            )
            self.assertEqual(validator.validate_svg(path), [])

    def test_rejects_script_and_missing_accessibility(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            path = Path(temp) / "unsafe.svg"
            path.write_text('<svg viewBox="0 0 1 1"><script/></svg>', encoding="utf-8")
            errors = validator.validate_svg(path)
            self.assertTrue(any("disallowed SVG element" in error for error in errors))
            self.assertTrue(any("aria-labelledby" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
