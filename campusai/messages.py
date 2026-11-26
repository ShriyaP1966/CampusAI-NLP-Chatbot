"""User-facing fixed messages, keyed by language."""

NOT_FOUND = {
    "en": (
        "I could not find that in the campus documents, so I will not guess. "
        "Try asking about admissions, courses, fees, exams, scholarships, "
        "facilities, events, placements or contact details."
    ),
}

EMPTY_QUESTION = {
    "en": "Please type a question about the campus.",
}


def get(table: dict[str, str], lang: str) -> str:
    return table.get(lang) or table["en"]
