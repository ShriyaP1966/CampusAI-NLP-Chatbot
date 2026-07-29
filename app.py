import random
import joblib
import pandas as pd
import streamlit as st

from preprocess import preprocess_text
from ner import extract_entity

# -----------------------
# Page Configuration
# -----------------------

st.set_page_config(
    page_title="CampusAI",
    page_icon="🎓",
    layout="centered"
)

# -----------------------
# Load Models
# -----------------------

classifier = joblib.load("models/intent_classifier.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

# -----------------------
# Load Knowledge Base
# -----------------------

kb = pd.read_csv("data/university_kb.csv")
kb.columns = kb.columns.str.lower()

# -----------------------
# Predict Intent
# -----------------------
def predict_intent(query):

    if not query:
        return None, 0.0

    query_lower = query.lower()

def predict_intent(query):

    query_lower = query.lower()

    # -------------------------
    # Rule-based Intent Detection
    # -------------------------

    if any(word in query_lower for word in ["eligibility", "eligible", "qualification", "criteria"]):
        return "eligibility", 1.0

    elif any(word in query_lower for word in ["fee", "fees", "tuition", "payment"]):
        return "fees", 1.0

    elif any(word in query_lower for word in ["scholarship", "scholarships"]):
        return "scholarship", 1.0

    elif any(word in query_lower for word in ["hostel", "mess", "laundry"]):
        return "hostel", 1.0

    elif any(word in query_lower for word in ["placement", "placements", "recruiter", "recruiters", "package", "internship"]):
        return "placement", 1.0

    elif any(word in query_lower for word in ["document", "documents", "certificate", "aadhaar"]):
        return "documents", 1.0

    elif any(word in query_lower for word in ["admission", "apply", "application", "deadline"]):
        return "admission", 1.0

    elif any(word in query_lower for word in ["course", "courses", "program", "programs", "offer", "offered"]):
        return "courses", 1.0
    
    elif any(word in query_lower for word in ["contact", "office", "website", "email", "phone"]):
        return "contact", 1.0

    elif any(word in query_lower for word in ["library", "lab", "wifi", "transport", "cafeteria", "sports"]):
        return "facilities", 1.0

    # -------------------------
    # ML Model
    # -------------------------

    processed = preprocess_text(query)

    vector = vectorizer.transform([processed])

    prediction = classifier.predict(vector)

    intent = label_encoder.inverse_transform(prediction)[0]

    confidence = classifier.predict_proba(vector).max()

    return intent, confidence
# -----------------------
# Retrieve Response
# -----------------------

def get_response(intent, query):

    entity = extract_entity(query)

    response = kb[
        (kb["intent"] == intent) &
        (kb["entity"].str.lower() == entity.lower())
    ]

    if not response.empty:
        return response.iloc[0]["response"], entity

    response = kb[
        (kb["intent"] == intent) &
        (kb["entity"].str.lower() == "general")
    ]

    if not response.empty:
        return response.iloc[0]["response"], entity

    response = kb[kb["intent"] == intent]

    if not response.empty:
        return random.choice(response["response"].tolist()), entity

    return "Sorry, I couldn't understand your question.", entity

# -----------------------
# UI
# -----------------------

# -----------------------
# UI
# -----------------------

st.title("🎓 CampusAI")
st.caption("AI-Powered University Assistant")

# Sidebar
with st.sidebar:

    st.header("📘 About")

    st.write(
        """
        CampusAI is an NLP-powered chatbot that answers
        university-related questions.

        **Model:** Logistic Regression

        **Vectorizer:** TF-IDF

        **NER:** Rule-Based

        **Frontend:** Streamlit
        """
    )

    st.divider()

    st.subheader("💡 Try asking")

    st.write("• What is the fee for B.Sc AI?")
    st.write("• Do you provide scholarships?")
    st.write("• Is hostel available?")
    st.write("• Who are the top recruiters?")
    st.write("• What documents are required?")

    st.divider()

    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# -----------------------
# Chat History
# -----------------------

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

        if message["role"] == "assistant":

            with st.expander("🧠 NLP Details"):

                st.write(f"**Intent:** {message['intent']}")
                st.write(f"**Entity:** {message['entity']}")

                st.progress(float(message["confidence"]))

                st.caption(
                    f"Confidence: {message['confidence']:.2%}"
                )

# -----------------------
# User Input
# -----------------------

prompt = st.chat_input("Ask a university-related question...")

if prompt:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Generate response
    intent, confidence = predict_intent(prompt)

    # Check confidence
    if confidence < 0.40:

        response = (
            "I'm not confident enough to answer that question.\n\n"
            "Try asking about:\n"
            "• Admissions\n"
            "• Courses\n"
            "• Eligibility\n"
            "• Fees\n"
            "• Scholarships\n"
            "• Hostel\n"
            "• Placements\n"
            "• Documents\n"
            "• Contact\n"
            "• Campus Facilities"
        )

        entity = "N/A"

    else:

        response, entity = get_response(intent, prompt)

    # Save assistant message
    st.session_state.messages.append({
        "role": "assistant",
        "content": response,
        "intent": intent,
        "entity": entity,
        "confidence": confidence
    })

    # Refresh page
    st.rerun()