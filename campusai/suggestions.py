"""Suggested starter questions shown in the chat UI, per language."""

SUGGESTIONS = {
    "en": [
        "What is the last date for admission?",
        "How much is the BCA tuition fee?",
        "When are the semester exams?",
        "Is there a scholarship for girls?",
        "Is hostel accommodation available?",
        "Who are the top recruiters?",
    ],
}


def get_suggestions(lang: str) -> list[str]:
    return list(SUGGESTIONS.get(lang) or SUGGESTIONS["en"])
