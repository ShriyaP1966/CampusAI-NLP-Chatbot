import os
import joblib
import pandas as pd

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

from preprocess import preprocess_text


# -------------------------------
# Load Dataset
# -------------------------------

df = pd.read_csv("data/intents.csv")

print("Dataset Loaded Successfully!")
print(df.head())


# -------------------------------
# Preprocess Questions
# -------------------------------

df["processed_question"] = df["question"].apply(preprocess_text)

print("\nPreprocessing Complete!")


# -------------------------------
# Encode Labels
# -------------------------------

label_encoder = LabelEncoder()

df["intent_label"] = label_encoder.fit_transform(df["intent"])


# -------------------------------
# TF-IDF Vectorization
# -------------------------------

vectorizer = TfidfVectorizer()

X = vectorizer.fit_transform(df["processed_question"])

y = df["intent_label"]


# -------------------------------
# Split Dataset
# -------------------------------

X_train, X_test, y_train, y_test = train_test_split(
    X,
    y,
    test_size=0.2,
    random_state=42,
    stratify=y
)


# -------------------------------
# Train Model
# -------------------------------

classifier = LogisticRegression(max_iter=1000)

classifier.fit(X_train, y_train)

print("\nModel Training Complete!")


# -------------------------------
# Evaluate Model
# -------------------------------

predictions = classifier.predict(X_test)

from sklearn.metrics import confusion_matrix

cm = confusion_matrix(y_test, predictions)

print("\nConfusion Matrix")
print(cm)

accuracy = accuracy_score(y_test, predictions)

print(f"\nAccuracy: {accuracy:.2f}")

print("\nClassification Report")

print(classification_report(
    y_test,
    predictions,
    target_names=label_encoder.classes_
))


# -------------------------------
# Save Models
# -------------------------------

os.makedirs("models", exist_ok=True)

joblib.dump(classifier, "models/intent_classifier.pkl")
joblib.dump(vectorizer, "models/tfidf_vectorizer.pkl")
joblib.dump(label_encoder, "models/label_encoder.pkl")

print("\nModels Saved Successfully!")