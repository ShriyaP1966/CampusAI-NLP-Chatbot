import pytest


@pytest.mark.parametrize(
    ("question", "source", "phrase"),
    [
        ("What is the last date for admission?", "admissions#dates", "July 31, 2027"),
        ("How much is the BCA tuition fee?", "fees#tuition", "70,000"),
        ("Who are the top recruiters?", "placements#recruiters", "Infosys"),
        ("What documents are required for admission?", "admissions#documents", "Aadhaar"),
        ("When are the semester exams?", "exams#schedule", "December 1"),
        ("What attendance do I need to sit the exams?", "exams#hall-ticket", "75%"),
        ("When is the tech fest?", "events#techfest", "February 18"),
        ("Does the campus have Wi-Fi?", "facilities#wifi-labs", "Wi-Fi"),
        ("Is there a scholarship for girls?", "scholarships#girls", "10,000"),
    ],
)
def test_answers_come_from_the_right_section(bot, question, source, phrase):
    answer = bot.ask(question)
    assert answer.found
    assert answer.sources[0].chunk_id == source
    assert phrase in answer.text


def test_every_answer_names_its_source(bot):
    answer = bot.ask("Is hostel available?")
    assert answer.found
    src = answer.sources[0]
    assert (src.title, src.section_title) == ("Campus facilities", "Hostel")
    assert src.text


@pytest.mark.parametrize(
    "question",
    ["What is the capital of France?", "Who is the vice chancellor?", "write me a poem"],
)
def test_out_of_scope_questions_are_not_guessed(bot, question):
    answer = bot.ask(question)
    assert not answer.found
    assert answer.status == "not_found"
    assert answer.sources == []
    assert "will not guess" in answer.text


@pytest.mark.parametrize("question", ["", "   ", None])
def test_empty_question(bot, question):
    answer = bot.ask(question)
    assert not answer.found
    assert "question" in answer.text.lower()


def test_answer_keeps_only_matching_sentences(bot):
    answer = bot.ask("When do the classes begin?")
    assert "September 1, 2027" in answer.text
    assert "Aadhaar" not in answer.text


def test_unsupported_language_falls_back_to_english(bot):
    assert bot.ask("Is hostel available?", lang="xx").found
