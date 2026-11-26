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
    "hi": [
        "प्रवेश की अंतिम तिथि क्या है?",
        "बीसीए की ट्यूशन फीस कितनी है?",
        "सेमेस्टर परीक्षाएँ कब होती हैं?",
        "क्या छात्राओं के लिए कोई छात्रवृत्ति है?",
        "क्या छात्रावास की सुविधा उपलब्ध है?",
        "प्रमुख भर्तीकर्ता कंपनियाँ कौन सी हैं?",
    ],
    "mr": [
        "प्रवेशाची शेवटची तारीख कोणती आहे?",
        "बीसीएचे शिक्षण शुल्क किती आहे?",
        "सत्र परीक्षा कधी होतात?",
        "मुलींसाठी काही शिष्यवृत्ती आहे का?",
        "वसतिगृहाची सोय उपलब्ध आहे का?",
        "प्रमुख भरती करणाऱ्या कंपन्या कोणत्या आहेत?",
    ],
}


def get_suggestions(lang: str) -> list[str]:
    return list(SUGGESTIONS.get(lang) or SUGGESTIONS["en"])
