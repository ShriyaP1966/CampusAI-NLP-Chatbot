"""Tokenization and normalization.

Everything here is plain Python so the retrieval core has no runtime
dependencies and starts instantly on small hosts.
"""

from __future__ import annotations

import re
import unicodedata

# Words that carry no retrieval signal in questions about campus life.
STOPWORDS_EN = frozenset(
    """
    a an the and or of to in on at for from by with about into over as is are was were be been
    am do does did can could will would shall should may might must have has had having i me my
    we our you your he she it its they them their this that these those there here what which who
    whom whose how when where why tell please give want need know like any some much many also
    just if then than so such not no yes get let us ok hi hello
    """.split()
)

# Variants that should match the same document words. Applied before stemming
# to both documents and queries, so retrieval stays symmetric.
SYNONYMS_EN = {
    "cost": "fee",
    "costs": "fee",
    "price": "fee",
    "charges": "fee",
    "charge": "fee",
    "deadline": "close",
    "closing": "close",
    "ends": "close",
    "end": "close",
    "begin": "start",
    "begins": "start",
    "starts": "start",
    "timetable": "schedule",
    "dorm": "hostel",
    "dormitory": "hostel",
    "accommodation": "hostel",
    "internet": "wifi",
    "recruiters": "recruiter",
    "companies": "recruiter",
    "package": "salary",
    "salary": "salary",
    "bus": "transport",
    "buses": "transport",
    "doctor": "medical",
    "ambulance": "medical",
    "marksheet": "document",
    "certificate": "document",
    "papers": "paper",
    "retotal": "revaluation",
    "recheck": "revaluation",
    "reevaluation": "revaluation",
    "timing": "open",
    "timings": "open",
    "hours": "open",
}

_DOTTED = re.compile(r"(?<=[^\W\d_])\.(?=[^\W\d_])")
_JOINERS = (
    ("wi-fi", "wifi"),
    ("e-mail", "email"),
    ("b.tech", "btech"),
    ("last date", "deadline"),
    ("tech fest", "techfest"),
    ("tech-fest", "techfest"),
)
_SENTENCE_END = re.compile(r"(?<=[.!?।])\s+")


def normalize(text: str) -> str:
    """Unicode-normalize, lowercase and glue dotted abbreviations (B.Sc -> bsc)."""
    text = unicodedata.normalize("NFKC", text).lower()
    for src, dst in _JOINERS:
        text = text.replace(src, dst)
    return _DOTTED.sub("", text)


def split_words(text: str) -> list[str]:
    """Split on anything that is not a letter, combining mark or digit.

    Python's ``\\w`` drops Devanagari vowel signs, so the split is done on
    Unicode categories instead. That keeps Hindi and Marathi words intact.
    """
    words: list[str] = []
    current: list[str] = []
    for ch in text:
        if unicodedata.category(ch)[0] in ("L", "M", "N"):
            current.append(ch)
        elif current:
            words.append("".join(current))
            current = []
    if current:
        words.append("".join(current))
    return words


def stem_en(word: str) -> str:
    """A deliberately small suffix stripper (fees -> fee, studies -> study)."""
    if len(word) <= 3 or not word.isalpha():
        return word
    if word.endswith("ies") and len(word) > 4:
        return word[:-3] + "y"
    for suffix in ("ing", "ed", "es", "s"):
        if word.endswith(suffix) and not word.endswith("ss") and len(word) - len(suffix) >= 3:
            return word[: -len(suffix)]
    return word


def tokenize(text: str, lang: str = "en") -> list[str]:
    """Return index terms for ``text`` in ``lang``."""
    if lang != "en":
        raise ValueError(f"Unsupported language: {lang!r}")
    terms = []
    for word in split_words(normalize(text)):
        if word in STOPWORDS_EN:
            continue
        terms.append(stem_en(SYNONYMS_EN.get(word, word)))
    return terms


def split_sentences(text: str) -> list[str]:
    """Split a passage into sentences (handles the Devanagari danda)."""
    parts = [p.strip() for p in _SENTENCE_END.split(text.strip())]
    return [p for p in parts if p]
