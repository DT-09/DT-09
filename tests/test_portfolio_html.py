"""Tests for the profile website's structural and accessibility checks."""

from __future__ import annotations

import tempfile
import unittest
from pathlib import Path

import importlib.util

MODULE_PATH = Path(__file__).resolve().parents[1] / "scripts" / "validate_portfolio.py"
SPEC = importlib.util.spec_from_file_location("validate_portfolio_html", MODULE_PATH)
validator = importlib.util.module_from_spec(SPEC)
assert SPEC and SPEC.loader
SPEC.loader.exec_module(validator)


class PortfolioHTMLTests(unittest.TestCase):
    def write_page(self, root: Path, body: str) -> Path:
        path = root / "index.html"
        path.write_text(
            '<!doctype html><html lang="en"><head><title>Portfolio</title>'
            '<meta name="description" content="A portfolio">'
            '<meta name="viewport" content="width=device-width,initial-scale=1">'
            '<style>@media(prefers-reduced-motion:reduce){}</style>'
            '<noscript>Enable JavaScript</noscript></head><body>'
            '<a class="skip-link" href="#main">Skip</a><nav aria-label="Primary"></nav>'
            '<main id="main"><h1>Portfolio</h1>' + body + '</main>'
            '<script>const ready = true;</script></body></html>',
            encoding="utf-8",
        )
        return path

    def test_valid_page_passes(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = self.write_page(root, '<a href="#main">Top</a>')
            self.assertEqual(validator.validate_html(path, root), [])

    def test_missing_anchor_is_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = self.write_page(root, '<a href="#missing">Broken</a>')
            errors = validator.validate_html(path, root)
            self.assertTrue(any("missing HTML anchor" in error for error in errors))

    def test_duplicate_ids_are_reported(self) -> None:
        with tempfile.TemporaryDirectory() as temp:
            root = Path(temp)
            path = self.write_page(root, '<span id="duplicate"></span><span id="duplicate"></span>')
            errors = validator.validate_html(path, root)
            self.assertTrue(any("duplicate HTML id" in error for error in errors))


if __name__ == "__main__":
    unittest.main()
