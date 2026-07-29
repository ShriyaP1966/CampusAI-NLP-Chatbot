import re
import string
import nltk
import spacy

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# Download NLTK resources (only first time)
nltk.download("punkt")
nltk.download("punkt_tab")
nltk.download("stopwords")

# Load spaCy model
nlp = spacy.load("en_core_web_sm")

# Stop words
STOP_WORDS = set(stopwords.words("english"))


def preprocess_text(text):
    """
    Preprocess text for the NLP chatbot.
    """

    # Lowercase
    text = text.lower()

    # Remove punctuation
    text = text.translate(str.maketrans("", "", string.punctuation))

    # Remove extra spaces
    text = re.sub(r"\s+", " ", text).strip()

    # Tokenize
    tokens = word_tokenize(text)

    # Remove stopwords
    tokens = [word for word in tokens if word not in STOP_WORDS]

    # Lemmatize
    doc = nlp(" ".join(tokens))

    lemmas = [
        token.lemma_
        for token in doc
        if token.lemma_ not in STOP_WORDS
    ]

    return " ".join(lemmas)


# ---------------- TESTING ---------------- #

if __name__ == "__main__":

    while True:

        query = input("\nEnter your query (type 'exit' to quit): ")

        if query.lower() == "exit":
            print("Goodbye!")
            break

        processed = preprocess_text(query)

        print("\nProcessed Text:")
        print(processed)