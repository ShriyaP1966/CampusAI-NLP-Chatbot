"""BM25 retrieval with an explicit confidence check."""

from __future__ import annotations

from dataclasses import dataclass

from campusai.bm25 import BM25
from campusai.documents import Chunk
from campusai.text import tokenize

# A hit must match at least this share of the (idf-weighted) question terms
# to be trusted. Chosen on the development split of the evaluation set.
DEFAULT_MIN_COVERAGE = 0.5


@dataclass(frozen=True)
class Hit:
    chunk: Chunk
    score: float
    coverage: float


class Retriever:
    """Ranks document sections for a question, one BM25 index per language."""

    def __init__(self, chunks: list[Chunk], min_coverage: float = DEFAULT_MIN_COVERAGE):
        self.min_coverage = min_coverage
        self._chunks: dict[str, list[Chunk]] = {}
        for chunk in chunks:
            self._chunks.setdefault(chunk.lang, []).append(chunk)

        self._terms: dict[str, list[set[str]]] = {}
        self._index: dict[str, BM25] = {}
        for lang, items in self._chunks.items():
            tokens = [tokenize(f"{c.title} {c.section_title} {c.text}", lang) for c in items]
            self._terms[lang] = [set(t) for t in tokens]
            self._index[lang] = BM25(tokens)

    @property
    def languages(self) -> list[str]:
        return sorted(self._chunks)

    def search(self, query: str, lang: str = "en", k: int = 3) -> list[Hit]:
        """Return up to ``k`` sections ranked by BM25, best first."""
        if lang not in self._index:
            lang = "en" if "en" in self._index else self.languages[0]
        terms = list(dict.fromkeys(tokenize(query, lang)))
        if not terms:
            return []

        index = self._index[lang]
        total_weight = sum(index.idf(t) for t in terms)
        ranked = []
        for i, score in enumerate(index.scores(terms)):
            if score <= 0:
                continue
            matched = sum(index.idf(t) for t in terms if t in self._terms[lang][i])
            ranked.append(Hit(self._chunks[lang][i], score, matched / total_weight))
        ranked.sort(key=lambda h: (h.score, h.coverage), reverse=True)
        return ranked[:k]

    def is_confident(self, hit: Hit) -> bool:
        return hit.coverage >= self.min_coverage
