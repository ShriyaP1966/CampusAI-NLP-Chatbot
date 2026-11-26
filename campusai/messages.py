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

REFUSED_INJECTION = {
    "en": (
        "I only answer questions about the campus, using its documents, so I can't follow "
        "instructions that change how I work or ask for my internal settings. Ask me about "
        "admissions, courses, fees, exams, scholarships, facilities, events, placements or "
        "contacts."
    ),
    "hi": (
        "यह सहायक केवल कैंपस के दस्तावेज़ों के आधार पर कैंपस से जुड़े प्रश्नों के उत्तर देता है, "
        "इसलिए अपने काम करने का तरीका बदलने या आंतरिक सेटिंग माँगने वाले निर्देशों का पालन नहीं "
        "किया जा सकता। प्रवेश, पाठ्यक्रम, शुल्क, परीक्षा, छात्रवृत्ति, सुविधाओं, कार्यक्रमों, "
        "प्लेसमेंट या संपर्क के बारे में पूछें।"
    ),
    "mr": (
        "हा सहायक फक्त कॅम्पसच्या कागदपत्रांच्या आधारे कॅम्पसशी संबंधित प्रश्नांची उत्तरे देतो, "
        "त्यामुळे कामाची पद्धत बदलणाऱ्या किंवा अंतर्गत सेटिंग्ज मागणाऱ्या सूचनांचे पालन करता "
        "येत नाही. प्रवेश, अभ्यासक्रम, शुल्क, परीक्षा, शिष्यवृत्ती, सुविधा, कार्यक्रम, प्लेसमेंट "
        "किंवा संपर्काबद्दल विचारा."
    ),
}

REFUSED_HARMFUL = {
    "en": (
        "I can't help with that. I can answer questions about admissions, courses, fees, exams, "
        "scholarships, facilities, events, placements and contacts. If you have a concern about "
        "exams or conduct, please contact the Exam Cell or the Admission Office."
    ),
    "hi": (
        "इसमें मदद नहीं की जा सकती। प्रवेश, पाठ्यक्रम, शुल्क, परीक्षा, छात्रवृत्ति, सुविधाओं, "
        "कार्यक्रमों, प्लेसमेंट और संपर्क के बारे में पूछा जा सकता है। परीक्षा या आचरण से जुड़ी किसी "
        "चिंता के लिए कृपया परीक्षा प्रकोष्ठ या प्रवेश कार्यालय से संपर्क करें।"
    ),
    "mr": (
        "यात मदत करता येत नाही. प्रवेश, अभ्यासक्रम, शुल्क, परीक्षा, शिष्यवृत्ती, सुविधा, कार्यक्रम, "
        "प्लेसमेंट आणि संपर्काबद्दल विचारता येते. परीक्षा किंवा वर्तनाबद्दल काही चिंता असल्यास "
        "कृपया परीक्षा कक्ष किंवा प्रवेश कार्यालयाशी संपर्क साधा."
    ),
}

SELF_HARM_SUPPORT = {
    "en": (
        "I'm sorry you're going through this. You don't have to handle it alone. Please talk to "
        "someone you trust or contact the university counselling service. In India you can call "
        "Tele-MANAS on 14416 (free, 24x7). If you are in immediate danger, call 112."
    ),
    "hi": (
        "आप जिस स्थिति से गुज़र रहे हैं उसके लिए मुझे खेद है। आपको इसे अकेले नहीं झेलना है। कृपया किसी "
        "भरोसेमंद व्यक्ति से बात करें या विश्वविद्यालय की परामर्श सेवा से संपर्क करें। भारत में आप "
        "टेली-मानस (Tele-MANAS) को 14416 पर कॉल कर सकते हैं (निःशुल्क, 24x7)। तत्काल खतरे की "
        "स्थिति में 112 पर कॉल करें।"
    ),
    "mr": (
        "तुम्ही ज्या परिस्थितीतून जात आहात त्याबद्दल मला खेद वाटतो. तुम्हाला हे एकट्याने सहन करावे "
        "लागणार नाही. कृपया एखाद्या विश्वासू व्यक्तीशी बोला किंवा विद्यापीठाच्या समुपदेशन सेवेशी "
        "संपर्क साधा. भारतात तुम्ही टेली-मानस (Tele-MANAS) ला 14416 वर कॉल करू शकता (मोफत, "
        "24x7). तात्काळ धोका असल्यास 112 वर कॉल करा."
    ),
}


def get(table: dict[str, str], lang: str) -> str:
    return table.get(lang) or table["en"]
