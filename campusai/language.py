"""Language detection for English, Hindi and Marathi.

Script tells English (Latin) from Devanagari. Hindi and Marathi share the
Devanagari script, so they are separated by function words and a few
characters that mark one language. Hindi or Marathi typed in Latin letters is
not supported and is treated as English.
"""

from __future__ import annotations

from campusai.text import split_words

SUPPORTED = ("en", "hi", "mr")

# Function words that are common in one language and rare or absent in the other.
_HI_WORDS = frozenset(
    """
    है हैं था थी थे क्या कौन कब कहाँ कहां कैसे कितना कितनी कितने मुझे में नहीं और चाहिए करें सकता
    सकते सकती होगा होगी होता होती बताइए बताएं बताएँ बताओ लिए यह वह क्यों तक इस कोई का की के
    """.split()
)
_MR_WORDS = frozenset(
    """
    आहे आहेत काय कोण कधी कुठे कसे किती मला मध्ये आणि नाही पाहिजे करावे शकतो शकते सांगा मिळेल मिळते
    असते असतो कोणते कोणती कोणता कुठल्या लागते लागतात चा ची चे च्या होतात यांना त्यांना आम्ही
    """.split()
)
# Inflectional endings that attach to Marathi words.
_MR_SUFFIXES = ("साठी", "च्या", "ाचा", "ाची", "ाचे", "ांचा", "ांची", "ांचे", "ांसाठी", "ाला", "ाकडे", "ांकडे")
_MR_LETTERS = "ळ"


def _is_devanagari(ch: str) -> bool:
    return "ऀ" <= ch <= "ॿ"


def detect_language(text: str) -> str:
    """Return ``"en"``, ``"hi"`` or ``"mr"`` for ``text``."""
    words = split_words(text.lower())
    indic = [w for w in words if any(_is_devanagari(c) for c in w)]
    latin = [w for w in words if w.isascii() and any(c.isalpha() for c in w)]
    if not indic or len(latin) > len(indic):
        return "en"

    hindi = marathi = 0
    for word in indic:
        if word in _HI_WORDS:
            hindi += 1
        if word in _MR_WORDS or word.endswith(_MR_SUFFIXES):
            marathi += 1
        if _MR_LETTERS in word:
            marathi += 2
    return "mr" if marathi > hindi else "hi"
