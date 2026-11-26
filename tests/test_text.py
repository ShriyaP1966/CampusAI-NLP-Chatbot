import pytest

from campusai.text import normalize, split_sentences, split_words, stem_en, tokenize


def test_normalize_glues_dotted_abbreviations_and_hyphens():
    assert normalize("B.Sc AI and Wi-Fi") == "bsc ai and wifi"


def test_split_words_keeps_devanagari_words_whole():
    assert split_words("छात्रावास शुल्क, कितना?") == ["छात्रावास", "शुल्क", "कितना"]


@pytest.mark.parametrize(
    ("word", "stem"),
    [("fees", "fee"), ("studies", "study"), ("exams", "exam"), ("class", "class"), ("ai", "ai")],
)
def test_stem_en(word, stem):
    assert stem_en(word) == stem


def test_tokenize_drops_stopwords_and_applies_synonyms():
    assert tokenize("What is the cost of B.Sc AI?") == ["fee", "bsc", "ai"]


def test_tokenize_rejects_unknown_language():
    with pytest.raises(ValueError):
        tokenize("hello", "xx")


def test_split_sentences_handles_danda():
    assert split_sentences("One. Two। Three?") == ["One.", "Two।", "Three?"]
