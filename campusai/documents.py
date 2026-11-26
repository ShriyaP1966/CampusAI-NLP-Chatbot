"""Loading campus documents and splitting them into citable sections."""

from __future__ import annotations

import logging
import re
from dataclasses import dataclass
from pathlib import Path

from campusai.safety import looks_like_injection

logger = logging.getLogger(__name__)

SUPPORTED_SUFFIXES = {".md", ".txt"}
_HEADING = re.compile(r"^##\s+(?P<title>.+?)(?:\s+\{#(?P<id>[\w-]+)\})?\s*$")
_FILE_LANG = re.compile(r"^(?P<stem>.+)\.(?P<lang>[a-z]{2})$")


class DocumentError(ValueError):
    """Raised when a document file cannot be used."""


@dataclass(frozen=True)
class Chunk:
    """One section of one document in one language: the unit that is retrieved and cited."""

    doc_id: str
    section_id: str
    title: str
    section_title: str
    lang: str
    text: str

    @property
    def chunk_id(self) -> str:
        return f"{self.doc_id}#{self.section_id}"


def _slug(text: str) -> str:
    slug = re.sub(r"[^\w]+", "-", text.lower(), flags=re.UNICODE).strip("-")
    return slug or "section"


def _split_front_matter(raw: str) -> tuple[dict[str, str], str]:
    lines = raw.lstrip("﻿").splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, "\n".join(lines)
    meta: dict[str, str] = {}
    for end, line in enumerate(lines[1:], start=1):
        if line.strip() == "---":
            return meta, "\n".join(lines[end + 1 :])
        key, sep, value = line.partition(":")
        if sep:
            meta[key.strip().lower()] = value.strip()
    raise DocumentError("front matter is not closed with '---'")


def parse_document(raw: str, path: Path) -> list[Chunk]:
    """Parse one document file into chunks."""
    meta, body = _split_front_matter(raw)

    stem, lang = path.stem, "en"
    match = _FILE_LANG.match(stem)
    if match:
        stem, lang = match["stem"], match["lang"]
    doc_id = meta.get("doc_id") or _slug(stem)
    lang = meta.get("lang", lang)
    title = meta.get("title") or stem.replace("_", " ").replace("-", " ").title()

    sections: list[tuple[str, str, list[str]]] = []
    for line in body.splitlines():
        heading = _HEADING.match(line)
        if heading:
            section_title = heading["title"].strip()
            sections.append((heading["id"] or _slug(section_title), section_title, []))
        elif sections:
            sections[-1][2].append(line)
        elif line.strip() and not line.startswith("#"):
            sections.append(("main", title, [line]))

    chunks: list[Chunk] = []
    seen: set[str] = set()
    for section_id, section_title, lines in sections:
        text = " ".join(part.strip() for part in "\n".join(lines).split("\n\n") if part.strip())
        text = re.sub(r"\s+", " ", text).strip()
        if not text:
            continue
        if section_id in seen:
            raise DocumentError(f"duplicate section id {section_id!r} in {path.name}")
        seen.add(section_id)
        chunks.append(Chunk(doc_id, section_id, title, section_title, lang, text))
    return chunks


def _is_injected(chunk: Chunk) -> bool:
    """Documents are untrusted input: skip sections that try to instruct the assistant."""
    if looks_like_injection(f"{chunk.section_title}. {chunk.text}"):
        logger.warning(
            "Skipping %s [%s]: it contains instructions aimed at the assistant",
            chunk.chunk_id,
            chunk.lang,
        )
        return True
    return False


def load_chunks(directory: str | Path) -> list[Chunk]:
    """Load every ``.md`` / ``.txt`` document in ``directory`` (README files are skipped)."""
    root = Path(directory)
    if not root.is_dir():
        raise DocumentError(f"Document folder not found: {root}")

    chunks: list[Chunk] = []
    for path in sorted(root.iterdir()):
        if path.suffix.lower() not in SUPPORTED_SUFFIXES or path.stem.lower() == "readme":
            continue
        try:
            chunks.extend(parse_document(path.read_text(encoding="utf-8"), path))
        except (DocumentError, UnicodeDecodeError) as exc:
            raise DocumentError(f"{path.name}: {exc}") from exc
    trusted = [c for c in chunks if not _is_injected(c)]
    if not trusted:
        raise DocumentError(f"No usable documents found in {root}")
    chunks = trusted
    logger.info("Loaded %d sections from %s", len(chunks), root)
    return chunks
