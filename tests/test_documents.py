from pathlib import Path

import pytest

from campusai.documents import DocumentError, load_chunks, parse_document

SAMPLE = """---
doc_id: fees
title: Fees
lang: en
---
## Tuition {#tuition}
Pay online.

## Late fee
A fine applies.
"""


def test_parse_document_splits_sections_with_ids():
    chunks = parse_document(SAMPLE, Path("fees.en.md"))
    assert [c.chunk_id for c in chunks] == ["fees#tuition", "fees#late-fee"]
    assert chunks[0].text == "Pay online."
    assert chunks[0].title == "Fees"


def test_plain_file_without_front_matter_uses_file_name():
    chunks = parse_document("Library opens at 8.\n", Path("campus_rules.md"))
    assert len(chunks) == 1
    assert chunks[0].doc_id == "campus_rules"
    assert chunks[0].lang == "en"


def test_language_comes_from_file_suffix():
    chunks = parse_document("## A {#a}\ntext", Path("notes.hi.md"))
    assert chunks[0].lang == "hi"


def test_unclosed_front_matter_is_an_error():
    with pytest.raises(DocumentError):
        parse_document("---\ntitle: x\n## A\ntext", Path("x.md"))


def test_duplicate_section_ids_are_an_error():
    with pytest.raises(DocumentError):
        parse_document("## A {#a}\none\n## B {#a}\ntwo", Path("x.md"))


def test_load_chunks_reads_folder_and_skips_readme(tmp_path):
    (tmp_path / "README.md").write_text("# Notes\nnot a document", encoding="utf-8")
    (tmp_path / "fees.en.md").write_text(SAMPLE, encoding="utf-8")
    assert len(load_chunks(tmp_path)) == 2


def test_load_chunks_missing_folder(tmp_path):
    with pytest.raises(DocumentError):
        load_chunks(tmp_path / "missing")


def test_load_chunks_empty_folder(tmp_path):
    with pytest.raises(DocumentError):
        load_chunks(tmp_path)


def test_sample_documents_cover_every_topic(bot):
    docs = {c.doc_id for c in bot.retriever._chunks["en"]}
    assert {
        "admissions",
        "courses",
        "fees",
        "exams",
        "scholarships",
        "facilities",
        "events",
        "placements",
        "contact",
    } <= docs
