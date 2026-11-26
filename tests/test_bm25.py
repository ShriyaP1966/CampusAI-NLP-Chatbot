import pytest

from campusai.bm25 import BM25


@pytest.fixture
def index() -> BM25:
    return BM25([["fee", "bsc", "fee"], ["hostel", "wifi"], ["exam", "schedule"]])


def test_matching_document_ranks_first(index):
    scores = index.scores(["hostel"])
    assert scores[1] > 0
    assert scores[0] == scores[2] == 0


def test_rarer_terms_weigh_more():
    bm25 = BM25([["a", "x"], ["a", "y"], ["a", "z"], ["b"]])
    assert bm25.idf("b") > bm25.idf("a")


def test_unknown_term_scores_nothing(index):
    assert index.scores(["zzz"]) == [0.0, 0.0, 0.0]


def test_empty_index_does_not_crash():
    assert BM25([]).scores(["x"]) == []
