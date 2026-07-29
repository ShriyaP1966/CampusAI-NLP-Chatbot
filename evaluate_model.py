import os
import joblib
import pandas as pd
import matplotlib.pyplot as plt

from preprocess import preprocess_text

from sklearn.model_selection import train_test_split
from sklearn.metrics import (
    accuracy_score,
    precision_score,
    recall_score,
    f1_score,
    classification_report,
    ConfusionMatrixDisplay
)

# ----------------------------
# Create output folder
# ----------------------------

os.makedirs("evaluation", exist_ok=True)

# ----------------------------
# Load Dataset
# ----------------------------

df = pd.read_csv("data/intents.csv")
df.columns = df.columns.str.lower()

df["processed"] = df["question"].apply(preprocess_text)

# ----------------------------
# Load Models
# ----------------------------

classifier = joblib.load("models/intent_classifier.pkl")
vectorizer = joblib.load("models/tfidf_vectorizer.pkl")
label_encoder = joblib.load("models/label_encoder.pkl")

# ----------------------------
# Prepare Data
# ----------------------------

X = vectorizer.transform(df["processed"])

y = label_encoder.transform(df["intent"])

_, X_test, _, y_test = train_test_split(
    X,
    y,
    test_size=0.20,
    random_state=42,
    stratify=y
)

# ----------------------------
# Prediction
# ----------------------------

predictions = classifier.predict(X_test)

# ----------------------------
# Metrics
# ----------------------------

accuracy = accuracy_score(y_test, predictions)
precision = precision_score(y_test, predictions, average="weighted")
recall = recall_score(y_test, predictions, average="weighted")
f1 = f1_score(y_test, predictions, average="weighted")

report = classification_report(
    y_test,
    predictions,
    target_names=label_encoder.classes_
)

print("\nAccuracy:", accuracy)
print(report)

# ----------------------------
# Save Metrics
# ----------------------------

with open("evaluation/metrics.txt", "w") as f:

    f.write(f"Accuracy : {accuracy:.4f}\n")
    f.write(f"Precision: {precision:.4f}\n")
    f.write(f"Recall   : {recall:.4f}\n")
    f.write(f"F1 Score : {f1:.4f}\n")

with open("evaluation/classification_report.txt", "w") as f:

    f.write(report)

# ----------------------------
# Confusion Matrix
# ----------------------------

disp = ConfusionMatrixDisplay.from_estimator(
    classifier,
    X_test,
    y_test,
    display_labels=label_encoder.classes_,
    xticks_rotation=45,
    cmap="Blues"
)

plt.title("Intent Classification Confusion Matrix")
plt.tight_layout()

plt.savefig("evaluation/confusion_matrix.png", dpi=300)

plt.show()

# ----------------------------
# Sample Predictions
# ----------------------------

sample = pd.DataFrame({

    "Actual": label_encoder.inverse_transform(y_test),
    "Predicted": label_encoder.inverse_transform(predictions)

})

sample.to_csv(
    "evaluation/sample_predictions.csv",
    index=False
)

print("\nEvaluation files saved successfully!")