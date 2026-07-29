import random
import joblib
import pandas as pd

from preprocess import preprocess_text
from ner import extract_entity


# -------------------------
# Load Trained Models
# -------------------------

classifier = joblib.load("models/intent_classifier.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")


# -------------------------
# Load Knowledge Base
# -------------------------

kb = pd.read_csv("data/university_kb.csv")

# Make column names lowercase
kb.columns = kb.columns.str.lower()


# -------------------------
# Predict Intent
# -------------------------

def predict_intent(query):

    processed = preprocess_text(query)

    vector = vectorizer.transform([processed])

    prediction = classifier.predict(vector)

    intent = label_encoder.inverse_transform(prediction)[0]

    confidence = classifier.predict_proba(vector).max()

    return intent, confidence


# -------------------------
# Retrieve Response
# -------------------------

def get_response(intent, query):

    entity = extract_entity(query)

    # 1. Exact match
    response = kb[
        (kb["intent"] == intent) &
        (kb["entity"].str.lower() == entity.lower())
    ]

    if not response.empty:
        return response.iloc[0]["response"], entity

    # 2. Course-specific fallback
    course = extract_entity(query)

    if course in ["B.Sc AI", "BCA", "MCA", "Data Science"]:

        response = kb[
            (kb["intent"] == intent) &
            (kb["entity"] == course)
        ]

        if not response.empty:
            return response.iloc[0]["response"], course

    # 3. General response
    response = kb[
        (kb["intent"] == intent) &
        (kb["entity"].str.lower() == "general")
    ]

    if not response.empty:
        return response.iloc[0]["response"], "general"

    # 4. Any response
    response = kb[kb["intent"] == intent]

    if not response.empty:
        return random.choice(response["response"].tolist()), entity

    return "Sorry, I couldn't find that information.", entity

# -------------------------
# Chat Loop
# -------------------------

print("=" * 50)
print("🎓 CampusAI - Intelligent University Assistant")
print("=" * 50)

while True:

    query = input("\nYou : ")

    if query.lower() == "exit":
        print("\nBot : Goodbye! Have a great day.")
        break

    intent, confidence = predict_intent(query)

    response, entity = get_response(intent, query)

    print("\n" + "=" * 50)

    print(f"Detected Intent : {intent}")
    print(f"Detected Entity : {entity}")
    print(f"Confidence      : {confidence:.2f}")

    print(f"\nBot : {response}")

    print("=" * 50)