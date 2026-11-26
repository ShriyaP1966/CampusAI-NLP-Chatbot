"""User-facing fixed messages, keyed by language."""

NOT_FOUND = {
    "en": (
        "I could not find that in the campus documents, so I will not guess. "
        "Try asking about admissions, courses, fees, exams, scholarships, "
        "facilities, events, placements or contact details."
    ),
    "hi": (
        "यह जानकारी मुझे कैंपस के दस्तावेज़ों में नहीं मिली, इसलिए मैं अनुमान नहीं लगाऊँगा। "
        "प्रवेश, पाठ्यक्रम, शुल्क, परीक्षा, छात्रवृत्ति, सुविधाओं, कार्यक्रमों, प्लेसमेंट या "
        "संपर्क के बारे में पूछकर देखें।"
    ),
    "mr": (
        "ही माहिती मला कॅम्पसच्या कागदपत्रांमध्ये सापडली नाही, म्हणून मी अंदाज लावणार नाही. "
        "प्रवेश, अभ्यासक्रम, शुल्क, परीक्षा, शिष्यवृत्ती, सुविधा, कार्यक्रम, प्लेसमेंट किंवा "
        "संपर्काबद्दल विचारून पाहा."
    ),
}

EMPTY_QUESTION = {
    "en": "Please type a question about the campus.",
    "hi": "कृपया कैंपस के बारे में कोई प्रश्न लिखें।",
    "mr": "कृपया कॅम्पसबद्दल एखादा प्रश्न लिहा.",
}


def get(table: dict[str, str], lang: str) -> str:
    return table.get(lang) or table["en"]
