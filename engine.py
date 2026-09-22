"""Canonical intent classification and knowledge-base retrieval engine.

Shared by both entry points (chatbot.py CLI and app.py Streamlit UI) so their
behavior cannot drift the way it previously did: predict_intent() now always
returns the trained model's real predict_proba() confidence, with no
keyword-based shortcuts bypassing the classifier.
"""

import logging
import random
from pathlib import Path

import joblib
import pandas as pd

from preprocess import preprocess_text
from ner import extract_entity

logger = logging.getLogger(__name__)

MODELS_DIR = Path(__file__).parent / "models"
DATA_DIR = Path(__file__).parent / "data"

REQUIRED_KB_COLUMNS = {"intent", "entity", "response"}

_classifier = None
_vectorizer = None
_label_encoder = None
_kb = None


class EngineLoadError(RuntimeError):
    """Raised when required model or knowledge-base files can't be loaded."""


def load_engine() -> None:
    """Load the trained model and knowledge base once. Safe to call repeatedly."""
    global _classifier, _vectorizer, _label_encoder, _kb

    if _classifier is not None:
        return

    try:
        classifier = joblib.load(MODELS_DIR / "intent_classifier.pkl")
        vectorizer = joblib.load(MODELS_DIR / "tfidf_vectorizer.pkl")
        label_encoder = joblib.load(MODELS_DIR / "label_encoder.pkl")
    except FileNotFoundError as exc:
        raise EngineLoadError(
            f"Missing trained model file ({exc.filename}). "
            "Run `python train_model.py` to generate the models/ directory."
        ) from exc

    try:
        kb = pd.read_csv(DATA_DIR / "university_kb.csv")
    except FileNotFoundError as exc:
        raise EngineLoadError(
            f"Missing knowledge base file ({exc.filename})."
        ) from exc

    kb.columns = kb.columns.str.lower()
    missing = REQUIRED_KB_COLUMNS - set(kb.columns)
    if missing:
        raise EngineLoadError(
            f"Knowledge base is missing required column(s): {sorted(missing)}"
        )

    _classifier, _vectorizer, _label_encoder, _kb = (
        classifier, vectorizer, label_encoder, kb,
    )
    logger.info("Engine loaded: %d KB entries", len(kb))


def predict_intent(query: str) -> tuple[str | None, float]:
    """Classify `query` with the trained TF-IDF + Logistic Regression model.

    Returns (intent, confidence). confidence is always the model's genuine
    predict_proba() output for the chosen class -- never a hardcoded value.
    Returns (None, 0.0) for empty/blank input.
    """
    load_engine()

    if not query or not query.strip():
        return None, 0.0

    processed = preprocess_text(query)
    vector = _vectorizer.transform([processed])
    prediction = _classifier.predict(vector)
    intent = _label_encoder.inverse_transform(prediction)[0]
    confidence = float(_classifier.predict_proba(vector).max())

    return intent, confidence


def get_response(intent: str, query: str) -> tuple[str, str]:
    """Look up a knowledge-base response for `intent`, narrowed by `query`'s entity.

    Falls back from an exact intent+entity match, to the intent's general
    response, to any response for the intent, to a not-found message.
    """
    load_engine()

    entity = extract_entity(query)

    match = _kb[(_kb["intent"] == intent) & (_kb["entity"].str.lower() == entity.lower())]
    if not match.empty:
        return match.iloc[0]["response"], entity

    match = _kb[(_kb["intent"] == intent) & (_kb["entity"].str.lower() == "general")]
    if not match.empty:
        return match.iloc[0]["response"], "general"

    match = _kb[_kb["intent"] == intent]
    if not match.empty:
        return random.choice(match["response"].tolist()), entity

    return "Sorry, I couldn't find that information.", entity
