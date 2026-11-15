#!/usr/bin/env python3
"""Validate portfolio documents, local links, heading anchors and referenced SVGs."""

from __future__ import annotations

import re
import shutil
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET
from html.parser import HTMLParser
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[1]
DOCUMENTS = ("README.md", "RESEARCH.md", "PORTFOLIO_STANDARD.md")
HTML_DOCUMENT = "index.html"
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




class PortfolioHTMLParser(HTMLParser):
    """Collect structural metadata, identifiers, local links and inline scripts."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.ids: list[str] = []
        self.links: list[str] = []
        self.html_lang = ""
        self.title_count = 0
        self.description = False
        self.viewport = False
        self.h1_count = 0
        self.main_count = 0
        self.nav_count = 0
        self.skip_link = False
        self.in_script = False
        self.current_script: list[str] = []
        self.scripts: list[str] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        values = dict(attrs)
        if tag == "html":
            self.html_lang = values.get("lang") or ""
        if "id" in values and values["id"]:
            self.ids.append(values["id"] or "")
        if tag == "a" and "skip-link" in (values.get("class") or "").split():
            self.skip_link = True
        if tag == "meta":
            name = (values.get("name") or "").lower()
            self.description = self.description or name == "description"
            self.viewport = self.viewport or name == "viewport"
        if tag == "title":
            self.title_count += 1
        if tag == "h1":
            self.h1_count += 1
        if tag == "main":
            self.main_count += 1
        if tag == "nav":
            self.nav_count += 1
        for key in ("href", "src"):
            if values.get(key):
                self.links.append(values[key] or "")
        if tag == "script":
            self.in_script = True
            self.current_script = []

    def handle_data(self, data: str) -> None:
        if self.in_script:
            self.current_script.append(data)

    def handle_endtag(self, tag: str) -> None:
        if tag == "script" and self.in_script:
            self.scripts.append("".join(self.current_script))
            self.current_script = []
            self.in_script = False


def validate_html(path: Path, root: Path) -> list[str]:
    errors: list[str] = []
    content = path.read_text(encoding="utf-8")
    parser = PortfolioHTMLParser()
    parser.feed(content)
    parser.close()

    duplicates = [item for item, count in Counter(parser.ids).items() if count > 1]
    for duplicate in duplicates:
        errors.append(f"{path.relative_to(root)}: duplicate HTML id: {duplicate}")
    if parser.html_lang != "en":
        errors.append(f"{path.relative_to(root)}: html element must declare lang=\\"en\\"")
    if parser.title_count != 1:
        errors.append(f"{path.relative_to(root)}: expected exactly one title element")
    if not parser.description:
        errors.append(f"{path.relative_to(root)}: missing description meta tag")
    if not parser.viewport:
        errors.append(f"{path.relative_to(root)}: missing viewport meta tag")
    if parser.h1_count != 1:
        errors.append(f"{path.relative_to(root)}: expected exactly one h1")
    if parser.main_count != 1:
        errors.append(f"{path.relative_to(root)}: expected exactly one main landmark")
    if parser.nav_count < 1:
        errors.append(f"{path.relative_to(root)}: missing navigation landmark")
    if not parser.skip_link:
        errors.append(f"{path.relative_to(root)}: missing skip-to-content link")
    if "prefers-reduced-motion" not in content:
        errors.append(f"{path.relative_to(root)}: missing reduced-motion support")
    if "<noscript" not in content.lower():
        errors.append(f"{path.relative_to(root)}: missing no-JavaScript fallback")

    known_ids = set(parser.ids)
    for target in parser.links:
        if target.startswith(("http://", "https://", "mailto:", "tel:", "data:", "javascript:")):
            continue
        parsed = urlsplit(target)
        if parsed.scheme or parsed.netloc:
            continue
        destination = (path.parent / unquote(parsed.path)).resolve() if parsed.path else path.resolve()
        if not destination.exists():
            errors.append(f"{path.relative_to(root)}: broken local HTML link: {target}")
            continue
        if parsed.fragment and destination == path.resolve() and unquote(parsed.fragment) not in known_ids:
            errors.append(f"{path.relative_to(root)}: missing HTML anchor: {target}")

    node = shutil.which("node")
    if node and parser.scripts:
        with tempfile.TemporaryDirectory() as temp:
            script_path = Path(temp) / "inline.js"
            script_path.write_text("\n".join(parser.scripts), encoding="utf-8")
            result = subprocess.run(
                [node, "--check", str(script_path)],
                capture_output=True,
                text=True,
                timeout=15,
                check=False,
            )
            if result.returncode:
                detail = (result.stderr or result.stdout).strip().splitlines()
                errors.append(f"{path.relative_to(root)}: inline JavaScript syntax check failed: {detail[-1] if detail else 'unknown error'}")
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

    html_document = root / HTML_DOCUMENT
    if not html_document.is_file():
        errors.append(f"missing required document: {HTML_DOCUMENT}")
    else:
        errors.extend(validate_html(html_document, root))

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
    print(f"Portfolio validation passed: {len(DOCUMENTS)} Markdown documents, the HTML portfolio and all README-linked SVG assets.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
