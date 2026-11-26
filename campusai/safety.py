"""Basic safety checks for user messages and for document text.

These are pattern checks, not a classifier. They catch the common, obvious
cases in English, Hindi and Marathi and fail open (the message is then handled
by the normal retrieval path, which only ever returns document text). See
"Known limitations" in the README.
"""

from __future__ import annotations

import re
import unicodedata

INJECTION = "injection"
HARMFUL = "harmful"
SELF_HARM = "self_harm"

_FLAGS = re.IGNORECASE | re.UNICODE
# Python's \w does not match Devanagari vowel signs, so spell the range out.
_D = "[ऀ-ॿ]*"


def _compile(patterns: list[str]) -> list[re.Pattern[str]]:
    return [re.compile(p.replace("{D}", _D), _FLAGS) for p in patterns]


_INJECTION = _compile(
    [
        # English
        r"\b(ignore|disregard|forget|override)\s+(all\s+|any\s+|your\s+|the\s+|my\s+)*"
        r"(previous|prior|above|earlier|preceding|original|system)\s+"
        r"(instructions?|rules?|prompts?|messages?|commands?)",
        r"\b(ignore|disregard|forget)\s+(all|everything|your)\s+"
        r"(instructions?|rules?|guidelines?|programming|training)",
        r"\bignore\s+everything\s+(above|before)",
        r"\b(reveal|show|print|repeat|display|leak|tell\s+me)\b.{0,30}"
        r"\b(system|hidden|initial|original|secret)\s+(prompt|instructions?|message|rules)",
        r"\bsystem\s+prompt\b",
        r"\byou\s+are\s+(now|no\s+longer)\b",
        r"\bpretend\s+(that\s+)?(you\s+are|you're|to\s+be)\b",
        r"\b(developer\s+mode|jailbreak|dan\s+mode|do\s+anything\s+now)\b",
        r"\bnew\s+instructions?\s*:",
        # Hindi
        r"(पिछले|पिछली|पहले\s+के|ऊपर\s+के|सभी)\s+(निर्देश|आदेश){D}\s+(को\s+)?"
        r"(अनदेखा|नज़रअंदाज़|नजरअंदाज|नज़रअंदाज|भूल|मत\s+मानो)",
        r"सिस्टम\s*प्रॉम्प्ट",
        r"(अपने|आपके|तुम्हारे)\s+(गुप्त\s+|आंतरिक\s+|मूल\s+)?निर्देश{D}\s+(बताओ|बताइए|दिखाओ|दिखाइए)",
        r"अब\s+से\s+(तुम|आप)\b",
        # Marathi
        r"(मागील|मागच्या|आधीच्या|वरील|सर्व)\s+सूचना{D}\s+(दुर्लक्ष|विसर)",
        r"सूचनांकडे\s+दुर्लक्ष",
        r"(तुझ्या|तुमच्या|आपल्या)\s+(गुप्त\s+|अंतर्गत\s+)?सूचना{D}\s+(सांग|दाखव|सांगा|दाखवा)",
        r"आतापासून\s+(तू|तुम्ही)\b",
    ]
)

_HARMFUL = _compile(
    [
        r"\b(make|build|create|assemble)\b.{0,20}\b(bomb|explosive|weapon|poison)",
        r"\bhow\s+to\s+(hack|break\s+into|steal|crack)\b",
        r"\b(hack|breach)\b.{0,25}\b(portal|server|website|account|wi-?fi|database)",
        r"\b(leak|steal)\b.{0,20}\b(question\s+paper|exam\s+paper|paper)\b",
        r"\b(cheat|cheating)\b.{0,25}\b(exam|test|paper)",
        r"\b(fake|forge|forged|fraudulent)\b.{0,20}"
        r"\b(certificate|marksheet|mark\s+sheet|document|degree)",
        r"\bkill\s+(someone|him|her|them|people)\b",
        r"बम\s*बनाने?",
        r"हैक\s*(कर|करना|कैसे)",
        r"पेपर\s*लीक",
        r"(नकली|फर्जी)\s*(मार्कशीट|अंकतालिका|प्रमाणपत्र|डिग्री)",
        r"परीक्षा\s*में\s*नकल",
        r"बॉम्ब\s*(कसा\s*)?बनव",
        r"हॅक\s*(कर|कसे)",
        r"पेपर\s*फोड",
        r"बनावट\s*(गुणपत्रिका|प्रमाणपत्र|पदवी)",
        r"परीक्षेत\s*कॉपी",
    ]
)

_SELF_HARM = _compile(
    [
        r"\b(kill(ing)?\s+myself|suicide|suicidal|end\s+my\s+life|want\s+to\s+die|"
        r"hurt\s+myself|harm\s+myself|self[-\s]?harm|don'?t\s+want\s+to\s+live)\b",
        r"आत्महत्या",
        r"मरना\s+चाहत[ाी]",
        r"जान\s+दे",
        r"जीना\s+नहीं\s+चाहत[ाी]",
        r"मरावेसे\s+वाटते",
        r"जीव\s+द्यावा",
        r"जगावेसे\s+वाटत\s+नाही",
    ]
)


def _clean(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("‍", "").replace("‌", "")
    return re.sub(r"\s+", " ", text)


def check_message(text: str) -> str | None:
    """Return the safety category of a user message, or None when it looks fine."""
    text = _clean(text)
    for category, patterns in (
        (SELF_HARM, _SELF_HARM),
        (HARMFUL, _HARMFUL),
        (INJECTION, _INJECTION),
    ):
        if any(p.search(text) for p in patterns):
            return category
    return None


def looks_like_injection(text: str) -> bool:
    """True when a piece of document text tries to give the assistant instructions."""
    text = _clean(text)
    return any(p.search(text) for p in _INJECTION)
