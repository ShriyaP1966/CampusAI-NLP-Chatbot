"""The question-answering engine: retrieve, then answer only from what was found."""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

from campusai import messages
from campusai.documents import Chunk, load_chunks
from campusai.language import detect_language
from campusai.retriever import Retriever
from campusai.safety import HARMFUL, INJECTION, SELF_HARM, check_message
from campusai.text import split_sentences, tokenize

DEFAULT_DOCS_DIR = Path(__file__).resolve().parent.parent / "data" / "documents"
MAX_SOURCES = 3
# Extra sources must score at least this fraction of the best hit.
RELATED_SCORE_RATIO = 0.8


_REFUSALS = {
    INJECTION: messages.REFUSED_INJECTION,
    HARMFUL: messages.REFUSED_HARMFUL,
    SELF_HARM: messages.SELF_HARM_SUPPORT,
}


@dataclass(frozen=True)
class Source:
    """A document section an answer is based on."""

    chunk_id: str
    doc_id: str
    section_id: str
    title: str
    section_title: str
    lang: str
    text: str

    @classmethod
    def from_chunk(cls, chunk: Chunk) -> Source:
        return cls(
            chunk.chunk_id,
            chunk.doc_id,
            chunk.section_id,
            chunk.title,
            chunk.section_title,
            chunk.lang,
            chunk.text,
        )


@dataclass(frozen=True)
class Answer:
    """The result of asking a question."""

    text: str
    status: str  # "answered", "not_found" or "refused"
    lang: str = "en"
    confidence: float = 0.0
    sources: list[Source] = field(default_factory=list)
    reason: str | None = None  # why a request was refused: injection, harmful or self_harm

    @property
    def found(self) -> bool:
        return self.status == "answered"


class CampusAI:
    """Answers questions from a set of campus documents."""

    def __init__(self, chunks: list[Chunk], min_coverage: float | None = None):
        kwargs = {} if min_coverage is None else {"min_coverage": min_coverage}
        self.retriever = Retriever(chunks, **kwargs)

    @classmethod
    def from_directory(cls, directory: str | Path | None = None) -> CampusAI:
        directory = directory or os.environ.get("CAMPUSAI_DOCS_DIR") or DEFAULT_DOCS_DIR
        return cls(load_chunks(directory))

    @property
    def section_count(self) -> int:
        return self.retriever.size

    @property
    def languages(self) -> list[str]:
        return self.retriever.languages

    def ask(self, question: str, lang: str | None = None) -> Answer:
        """Answer ``question``. When ``lang`` is None the language is detected."""
        question = (question or "").strip()
        lang = lang or detect_language(question)
        if not question:
            return Answer(messages.get(messages.EMPTY_QUESTION, lang), "not_found", lang)

        category = check_message(question)
        if category:
            return Answer(messages.get(_REFUSALS[category], lang), "refused", lang, reason=category)

        hits = self.retriever.search(question, lang, k=MAX_SOURCES)
        if not hits or not self.retriever.is_confident(hits[0]):
            return Answer(messages.get(messages.NOT_FOUND, lang), "not_found", lang)

        best = hits[0]
        related = [
            h
            for h in hits
            if h is best
            or (self.retriever.is_confident(h) and h.score >= RELATED_SCORE_RATIO * best.score)
        ]
        return Answer(
            text=self._extract(best.chunk, question),
            status="answered",
            lang=best.chunk.lang,
            confidence=round(best.coverage, 3),
            sources=[Source.from_chunk(h.chunk) for h in related],
        )

    def _extract(self, chunk: Chunk, question: str) -> str:
        """Keep the sentences of the best section that match the question."""
        sentences = split_sentences(chunk.text)
        if len(sentences) <= 2:
            return chunk.text
        terms = set(tokenize(question, chunk.lang))
        scored = [(len(terms & set(tokenize(s, chunk.lang))), s) for s in sentences]
        top = max(score for score, _ in scored)
        if top == 0:
            return chunk.text
        keep = [s for score, s in scored if score >= max(1, top * 0.5)]
        return " ".join(keep)
