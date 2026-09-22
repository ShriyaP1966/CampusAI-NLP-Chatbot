import streamlit as st

from engine import predict_intent, get_response, load_engine, EngineLoadError

# -----------------------
# Page Configuration
# -----------------------

st.set_page_config(
    page_title="CampusAI",
    page_icon="🎓",
    layout="centered"
)

# -----------------------
# Load Engine
# -----------------------

try:
    load_engine()
except EngineLoadError as exc:
    st.error(f"CampusAI couldn't start: {exc}")
    st.stop()

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
    if intent is None or confidence < 0.40:

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
