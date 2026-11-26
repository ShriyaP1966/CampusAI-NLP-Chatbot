import pytest

from campusai.language import detect_language
from campusai.suggestions import get_suggestions
from campusai.text import tokenize


@pytest.mark.parametrize(
    ("question", "lang"),
    [
        ("What is the last date for admission?", "en"),
        ("how much is the fee", "en"),
        ("प्रवेश की अंतिम तिथि क्या है?", "hi"),
        ("छात्रावास की फीस कितनी है", "hi"),
        ("क्या लड़कियों के लिए कोई छात्रवृत्ति है?", "hi"),
        ("प्रवेशाची शेवटची तारीख कोणती आहे?", "mr"),
        ("वसतिगृहाचे शुल्क किती आहे?", "mr"),
        ("मुलींसाठी शिष्यवृत्ती आहे का?", "mr"),
        ("BCA की फीस क्या है?", "hi"),
        ("BCA चे शुल्क किती आहे?", "mr"),
    ],
)
def test_detect_language(question, lang):
    assert detect_language(question) == lang


def test_detect_language_defaults_to_english_for_empty_or_numeric_text():
    assert detect_language("") == "en"
    assert detect_language("2027") == "en"


def test_indic_tokenizer_keeps_words_and_indexes_trigrams():
    terms = tokenize("छात्रावास की फीस", "hi")
    assert "छात" in terms
    assert "शुल" in terms  # फीस is normalised to the word the documents use
    assert "की" not in terms  # stop word


def test_latin_words_inside_hindi_text_are_kept():
    assert "bca" in tokenize("BCA की फीस", "hi")


@pytest.mark.parametrize(
    ("question", "source", "phrase"),
    [
        ("प्रवेश की अंतिम तिथि क्या है?", "admissions#dates", "31 जुलाई 2027"),
        ("बीसीए की फीस कितनी है?", "fees#tuition", "70,000"),
        ("परीक्षा कब होती है?", "exams#schedule", "1 दिसंबर"),
        ("प्रमुख कंपनियाँ कौन सी आती हैं?", "placements#recruiters", "इन्फोसिस"),
        ("टेकफेस्ट कब है?", "events#techfest", "18 फरवरी"),
        ("प्रवेशाची शेवटची तारीख कोणती आहे?", "admissions#dates", "31 जुलै 2027"),
        ("वसतिगृहाचे शुल्क किती आहे?", "fees#hostel", "45,000"),
        ("मुलींसाठी शिष्यवृत्ती आहे का?", "scholarships#girls", "10,000"),
        ("हॉल तिकीट कधी मिळते?", "exams#hall-ticket", "सात दिवस"),
        ("पदवीदान समारंभ कधी आहे?", "events#convocation", "25 मार्च 2028"),
    ],
)
def test_answers_come_back_in_the_questions_language(bot, question, source, phrase):
    answer = bot.ask(question)
    assert answer.found
    assert answer.lang == detect_language(question)
    assert answer.sources[0].chunk_id == source
    assert phrase in answer.text


@pytest.mark.parametrize(
    ("question", "marker"),
    [
        ("फ्रांस की राजधानी क्या है?", "अनुमान नहीं"),
        ("फ्रान्सची राजधानी कोणती आहे?", "अंदाज लावणार नाही"),
    ],
)
def test_out_of_scope_questions_are_declined_in_the_same_language(bot, question, marker):
    answer = bot.ask(question)
    assert not answer.found
    assert marker in answer.text


def test_explicit_language_overrides_detection(bot):
    answer = bot.ask("BCA fee", lang="hi")
    assert answer.lang == "hi"


def test_documents_exist_in_all_three_languages_with_the_same_sections(bot):
    by_lang: dict[str, set[str]] = {}
    for chunk in (
        bot.retriever._chunks["en"] + bot.retriever._chunks["hi"] + bot.retriever._chunks["mr"]
    ):
        by_lang.setdefault(chunk.lang, set()).add(chunk.chunk_id)
    assert by_lang["en"] == by_lang["hi"] == by_lang["mr"]


@pytest.mark.parametrize("lang", ["en", "hi", "mr"])
def test_suggestions_exist_for_every_language(lang):
    assert len(get_suggestions(lang)) == 6
