#!/usr/bin/env python3
"""Validate local portfolio links, heading anchors, and SVG accessibility metadata."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = (ROOT / "README.md", ROOT / "RESEARCH.md")
SVG_DIR = ROOT / "assets"


def heading_slug(text: str) -> str:
    text = re.sub(r"`([^\`]*)`", r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.lower().strip()
    text = re.sub(r"[^\w\- ]", "", text)
    return re.sub(r"[\s]+", "-", text)


def validate_document(path: Path) -> list[str]:
    errors: list[str] = []
    content = path.read_text(encoding="utf-8")
    anchors = set(re.findall(r'\bid=["\']([^"\']+)["\']', content))
    anchors.update(heading_slug(match.group(1)) for match in re.finditer(r"^#{1,6}\s+(.+?)\s*#*\s*$", content, re.M))

    # Markdown and HTML links. External links are intentionally not fetched in CI.
    patterns = (
        re.compile(r"!?\[[^\]]*\]\(([^)]+)\)"),
        re.compile(r"""\bhref=["']([^"']+)["']""", re.I),
        re.compile(r"""\bsrc=["']([^"']+)["']""", re.I),
    )
    targets: list[str] = []
    for pattern in patterns:
        targets.extend(match.group(1).strip().split()[0] for match in pattern.finditer(content))

    for target in targets:
        if not target or target.startswith(("http://", "https://", "mailto:", "data:", "sediment:")):
            continue
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            continue
        if parsed.path:
            candidate = (path.parent / unquote(parsed.path)).resolve()
            if not candidate.exists():
                errors.append(f"{path.relative_to(ROOT)}: broken local link: {target}")
        elif parsed.fragment and unquote(parsed.fragment) not in anchors:
            errors.append(f"{path.relative_to(ROOT)}: missing anchor: #{parsed.fragment}")

    for fragment in re.findall(r"\]\(#([^)]*)\)", content):
        if unquote(fragment) not in anchors:
            errors.append(f"{path.relative_to(ROOT)}: missing anchor: #{fragment}")
    return errors


def validate_svgs() -> list[str]:
    errors: list[str] = []
    for path in sorted(SVG_DIR.glob("*.svg")):
        try:
            root = ET.parse(path).getroot()
        except ET.ParseError as exc:
            errors.append(f"{path.relative_to(ROOT)}: invalid SVG XML: {exc}")
            continue
        if root.tag.split("}")[-1] != "svg":
            errors.append(f"{path.relative_to(ROOT)}: root element is not svg")
        children = {child.tag.split("}")[-1] for child in root}
        if "title" not in children or "desc" not in children:
            errors.append(f"{path.relative_to(ROOT)}: SVG must include title and desc")
        if not root.attrib.get("viewBox"):
            errors.append(f"{path.relative_to(ROOT)}: SVG must define viewBox")
    return errors


def main() -> int:
    errors: list[str] = []
    for document in DOCUMENTS:
        if not document.is_file():
            errors.append(f"missing required document: {document.relative_to(ROOT)}")
        else:
            errors.extend(validate_document(document))
    if not SVG_DIR.is_dir():
        errors.append("missing assets directory")
    else:
        errors.extend(validate_svgs())

    if errors:
        print("Portfolio validation failed:")
        for error in errors:
            print(f" - {error}")
        return 1

    print(f"Portfolio validation passed: {len(DOCUMENTS)} documents and {len(list(SVG_DIR.glob('*.svg')))} SVG assets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
