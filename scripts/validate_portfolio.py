#!/usr/bin/env python3
"""Validate portfolio documents, local links, heading anchors and referenced SVGs."""

from __future__ import annotations

import re
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = ("README.md", "RESEARCH.md", "PORTFOLIO_STANDARD.md")
SVG_PATTERN = re.compile(r"""assets/[^/"']+\.svg""", re.I)
MARKDOWN_LINK = re.compile(r"""!?(?:\[[^\]]*\])\((<[^>]+>|[^)\s]+)(?:\s+[^)]*)?\)""")
HTML_LINK = re.compile(r"""(?:href|src)\s*=\s*["']([^"']+)["']""", re.I)
HTML_ID = re.compile(r"""(?:^|\s)id\s*=\s*["']([^"']+)["']""", re.I)
HEADING = re.compile(r"^ {0,3}(#{1,6})\s+(.+?)\s*#*\s*$", re.M)


def strip_code_fences(content: str) -> str:
    """Remove fenced code blocks so examples are not treated as live links."""
    output: list[str] = []
    fence_char: str | None = None
    fence_size = 0
    for line in content.splitlines():
        stripped = line.lstrip()
        marker = stripped[:1]
        if len(line) - len(stripped) <= 3 and marker in {chr(96), "~"}:
            count = len(stripped) - len(stripped.lstrip(marker))
            if count >= 3:
                if fence_char is None:
                    fence_char, fence_size = marker, count
                elif marker == fence_char and count >= fence_size:
                    fence_char, fence_size = None, 0
                continue
        if fence_char is None:
            output.append(line)
    return "\n".join(output)


def heading_slug(text: str) -> str:
    tick = chr(96)
    text = re.sub(tick + r"([^" + tick + r"]*)" + tick, r"\1", text)
    text = re.sub(r"<[^>]+>", "", text)
    text = text.lower().strip()
    text = re.sub(r"[^\w\- ]", "", text, flags=re.UNICODE)
    return re.sub(r"\s+", "-", text)


def document_anchors(content: str) -> tuple[set[str], list[str]]:
    content = strip_code_fences(content)
    ids = HTML_ID.findall(content)
    duplicates = [item for item, count in Counter(ids).items() if count > 1]
    anchors = set(ids)
    seen: Counter[str] = Counter()
    for match in HEADING.finditer(content):
        base = heading_slug(match.group(2))
        suffix = seen[base]
        anchors.add(base if suffix == 0 else f"{base}-{suffix}")
        seen[base] += 1
    return anchors, duplicates


def link_targets(content: str) -> list[str]:
    content = strip_code_fences(content)
    targets = [match.group(1).strip("<>") for match in MARKDOWN_LINK.finditer(content)]
    targets.extend(match.group(1).strip() for match in HTML_LINK.finditer(content))
    return targets


def validate_document(path: Path, root: Path, anchor_cache: dict[Path, set[str]]) -> list[str]:
    errors: list[str] = []
    content = path.read_text(encoding="utf-8")
    anchors, duplicate_ids = document_anchors(content)
    for duplicate in duplicate_ids:
        errors.append(f"{path.relative_to(root)}: duplicate HTML id: {duplicate}")
    anchor_cache[path.resolve()] = anchors

    for target in link_targets(content):
        if not target or target.startswith(("http://", "https://", "mailto:", "data:", "sediment:")):
            continue
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            continue
        destination = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path.resolve()
        if not destination.exists():
            errors.append(f"{path.relative_to(root)}: broken local link: {target}")
            continue
        if parsed.fragment and destination.suffix.lower() in {".md", ".markdown"}:
            if destination not in anchor_cache:
                try:
                    target_anchors, target_duplicates = document_anchors(destination.read_text(encoding="utf-8"))
                    anchor_cache[destination] = target_anchors
                    for duplicate in target_duplicates:
                        errors.append(f"{destination.relative_to(root)}: duplicate HTML id: {duplicate}")
                except (OSError, UnicodeError):
                    errors.append(f"{path.relative_to(root)}: cannot read link target: {target}")
                    continue
            if unquote(parsed.fragment) not in anchor_cache[destination]:
                errors.append(f"{path.relative_to(root)}: missing anchor: {target}")
    return errors


def validate_svg(path: Path) -> list[str]:
    errors: list[str] = []
    try:
        root = ET.parse(path).getroot()
    except (ET.ParseError, OSError) as exc:
        return [f"{path}: invalid or unreadable SVG: {exc}"]

    if root.tag.split("}")[-1] != "svg":
        return [f"{path}: root element is not svg"]

    ids = {element.attrib["id"] for element in root.iter() if "id" in element.attrib}
    labelled_by = root.attrib.get("aria-labelledby", "").split()
    if root.attrib.get("role") != "img":
        errors.append(f"{path}: root must declare role=\"img\"")
    direct_children = {element.tag.split("}")[-1] for element in root}
    if not {"title", "desc"}.issubset(direct_children):
        errors.append(f"{path}: root must contain title and desc elements")
    if len(labelled_by) < 2 or not set(labelled_by).issubset(ids):
        errors.append(f"{path}: aria-labelledby must reference existing title and desc IDs")
    if not root.attrib.get("viewBox"):
        errors.append(f"{path}: missing viewBox")

    for element in root.iter():
        tag = element.tag.split("}")[-1].lower()
        if tag in {"script", "foreignobject"}:
            errors.append(f"{path}: disallowed SVG element: {tag}")
        for attribute in element.attrib:
            if attribute.lower().startswith("on"):
                errors.append(f"{path}: event-handler attribute is not allowed: {attribute}")
    return errors


def validate(root: Path = ROOT) -> list[str]:
    errors: list[str] = []
    anchor_cache: dict[Path, set[str]] = {}
    documents = [root / name for name in DOCUMENTS]

    for document in documents:
        if not document.is_file():
            errors.append(f"missing required document: {document.relative_to(root)}")
    for document in documents:
        if document.is_file():
            errors.extend(validate_document(document, root, anchor_cache))

    assets_dir = root / "assets"
    if not assets_dir.is_dir():
        errors.append("missing assets directory")
        return errors

    readme = root / "README.md"
    referenced = sorted(set(SVG_PATTERN.findall(readme.read_text(encoding="utf-8")))) if readme.is_file() else []
    if not referenced:
        errors.append("README.md does not reference any portfolio SVG assets")
    for relative in referenced:
        path = root / relative
        if not path.is_file():
            errors.append(f"README.md: referenced SVG is missing: {relative}")
        else:
            errors.extend(validate_svg(path))
    return errors


def main() -> int:
    errors = validate()
    if errors:
        print("Portfolio validation failed:")
        for error in errors:
            print(f" - {error}")
        return 1
    print(f"Portfolio validation passed: {len(DOCUMENTS)} documents and all README-linked SVG assets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
