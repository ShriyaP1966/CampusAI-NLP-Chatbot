"""A small Okapi BM25 implementation."""

from __future__ import annotations

import math
from collections import Counter


class BM25:
    """Okapi BM25 over pre-tokenized documents."""

    def __init__(self, documents: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1 = k1
        self.b = b
        self.size = len(documents)
        self.lengths = [len(d) for d in documents]
        self.avg_length = (sum(self.lengths) / self.size) if self.size else 0.0
        self.term_freqs = [Counter(d) for d in documents]
        self.doc_freq: Counter[str] = Counter()
        for tf in self.term_freqs:
            self.doc_freq.update(tf.keys())

    def idf(self, term: str) -> float:
        """Smoothed inverse document frequency. Unknown terms get the maximum value."""
        n = self.doc_freq.get(term, 0)
        return math.log(1.0 + (self.size - n + 0.5) / (n + 0.5))

    def score(self, query_terms: list[str], index: int) -> float:
        tf = self.term_freqs[index]
        relative_length = self.lengths[index] / self.avg_length if self.avg_length else 0.0
        norm = 1.0 - self.b + self.b * relative_length
        total = 0.0
        for term in set(query_terms):
            freq = tf.get(term, 0)
            if freq:
                total += self.idf(term) * (freq * (self.k1 + 1.0)) / (freq + self.k1 * norm)
        return total

    def scores(self, query_terms: list[str]) -> list[float]:
        return [self.score(query_terms, i) for i in range(self.size)]
