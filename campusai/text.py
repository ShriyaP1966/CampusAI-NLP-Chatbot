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

_NGRAM = 3
_DEVANAGARI_DIGITS = str.maketrans("०१२३४५६७८९", "0123456789")

STOPWORDS_HI = frozenset(
    """
    है हैं था थी थे हो होगा होगी होंगे होता होती होते रहा रही रहे क्या कौन कब कहाँ कहां कैसे कैसी
    कैसा क्यों कितना कितनी कितने कोई कुछ का की के को से में पर और या भी तो ही यह वह ये वे इस उस
    इन उन मैं मुझे मेरा मेरी मेरे हम हमें हमारा आप आपका आपकी आपके तुम कर करना करें करता करती
    करते सकता सकती सकते चाहिए चाहता चाहती चाहते बताइए बताएं बताएँ बताओ बताइये बताये कृपया लिए
    मिलेगा मिलेगी मिलता मिलती मिलते द्वारा साथ तक जा जाता जाती जाते न नहीं जी सभी अपना अपनी
    अपने एक हर बहुत कि जो जब तब अगर
    """.split()
)

STOPWORDS_MR = frozenset(
    """
    आहे आहेत होते होता होती होतात असते असतो असतात असे असा अशी काय कोण कोणता कोणती कोणते कधी कुठे
    कुठल्या कुठली कुठला कसे कशी कसा का किती चा ची चे च्या चं ला ना ने नी ते तो ती हा ही हे या त्या
    त्याला त्यांना मला मी आम्ही आपण तुम्ही तुमचा तुमची तुमचे आणि व किंवा पण नाही नको करा करावे
    करू शकतो शकते शकता शकतात मध्ये साठी पासून पर्यंत वर कृपया सांगा सांगू द्या मिळेल मिळते मिळतो
    एक प्रत्येक सर्व काही कोणी की जर तर
    """.split()
)

# A few common spoken variants mapped to the word the sample documents use.
SYNONYMS_HI = {
    "होस्टल": "छात्रावास",
    "हॉस्टल": "छात्रावास",
    "फीस": "शुल्क",
    "फ़ीस": "शुल्क",
    "फी": "शुल्क",
    "स्कॉलरशिप": "छात्रवृत्ति",
    "छात्रवृत्तियाँ": "छात्रवृत्ति",
    "छात्रवृत्तियां": "छात्रवृत्ति",
    "लाइब्रेरी": "पुस्तकालय",
    "एग्जाम": "परीक्षा",
    "परीक्षाएँ": "परीक्षा",
    "परीक्षाएं": "परीक्षा",
    "समयसारणी": "सारणी",
    "किराया": "शुल्क",
    "भाड़ा": "शुल्क",
    "खाना": "भोजन",
}
SYNONYMS_MR = {
    "होस्टेल": "वसतिगृह",
    "हॉस्टेल": "वसतिगृह",
    "फी": "शुल्क",
    "फीस": "शुल्क",
    "स्कॉलरशिप": "शिष्यवृत्ती",
    "लायब्ररी": "ग्रंथालय",
    "एक्झाम": "परीक्षा",
    "भाडे": "शुल्क",
    "भाडं": "शुल्क",
    "परीक्षांचे": "परीक्षा",
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


def _tokenize_en(text: str) -> list[str]:
    terms = []
    for word in split_words(normalize(text)):
        if word in STOPWORDS_EN:
            continue
        terms.append(stem_en(SYNONYMS_EN.get(word, word)))
    return terms


def _normalize_indic(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).lower()
    text = text.translate(_DEVANAGARI_DIGITS)
    for src, dst in _JOINERS:
        text = text.replace(src, dst)
    text = _DOTTED.sub("", text)
    # Zero-width joiners and the chandrabindu are written inconsistently.
    return text.replace("‍", "").replace("‌", "").replace("ँ", "ं")


def _tokenize_indic(text: str, lang: str) -> list[str]:
    """Hindi and Marathi inflect heavily (शुल्क, शुल्कात, शुल्काचे), so longer
    Devanagari words are indexed as character trigrams. Latin words that appear
    inside Hindi or Marathi text (course names such as BCA) are handled as English."""
    stopwords = STOPWORDS_HI if lang == "hi" else STOPWORDS_MR
    synonyms = SYNONYMS_HI if lang == "hi" else SYNONYMS_MR
    terms: list[str] = []
    for word in split_words(_normalize_indic(text)):
        if word.isascii():
            if word not in STOPWORDS_EN:
                terms.append(stem_en(SYNONYMS_EN.get(word, word)))
            continue
        if word in stopwords:
            continue
        word = synonyms.get(word, word)
        if len(word) <= _NGRAM:
            terms.append(word)
        else:
            terms.extend(word[i : i + _NGRAM] for i in range(len(word) - _NGRAM + 1))
    return terms


def tokenize(text: str, lang: str = "en") -> list[str]:
    """Return index terms for ``text`` in ``lang`` (``en``, ``hi`` or ``mr``)."""
    if lang == "en":
        return _tokenize_en(text)
    if lang in ("hi", "mr"):
        return _tokenize_indic(text, lang)
    raise ValueError(f"Unsupported language: {lang!r}")


def split_sentences(text: str) -> list[str]:
    """Split a passage into sentences (handles the Devanagari danda)."""
    parts = [p.strip() for p in _SENTENCE_END.split(text.strip())]
    return [p for p in parts if p]
