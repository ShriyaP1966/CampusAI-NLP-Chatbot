# 🎓 CampusAI – Intelligent University Chatbot

An AI-powered University Chatbot built using **Natural Language Processing (NLP)**. The chatbot understands user queries related to admissions, courses, eligibility, fees, scholarships, hostel, placements, documents, contact information, and campus facilities.

The system uses **text preprocessing**, **TF-IDF feature extraction**, **Logistic Regression for intent classification**, **rule-based Named Entity Recognition (NER)**, and a **knowledge base retrieval system** to provide accurate responses through an interactive **Streamlit** web application.

---

## ✨ Features

- 🎯 Intent Classification using Logistic Regression
- 📝 Text Preprocessing (Tokenization, Stopword Removal, Lemmatization)
- 🔍 TF-IDF Feature Extraction
- 🏷️ Rule-Based Named Entity Recognition (NER)
- 📚 Knowledge Base Response Retrieval
- 💬 Interactive Streamlit Web Interface
- 📊 Displays Intent, Entity, and Confidence Score
- 🎓 Handles queries related to:
  - Admissions
  - Courses
  - Eligibility
  - Fees
  - Scholarships
  - Hostel
  - Placements
  - Documents
  - Contact Information
  - Campus Facilities

---

# 🏗️ NLP Pipeline

```
User Query
      │
      ▼
Text Preprocessing
      │
      ▼
TF-IDF Vectorization
      │
      ▼
Intent Classification
(Logistic Regression)
      │
      ▼
Named Entity Recognition
      │
      ▼
Knowledge Base Retrieval
      │
      ▼
Response Generation
```

---

# 📂 Project Structure

```
CampusAI/
│
├── app.py
├── chatbot.py
├── preprocess.py
├── ner.py
├── train_model.py
├── requirements.txt
│
├── data/
│   ├── intents.csv
│   └── university_kb.csv
│
├── models/
│   ├── intent_classifier.pkl
│   ├── tfidf_vectorizer.pkl
│   └── label_encoder.pkl
│
└── README.md
```

---

# 🛠️ Technologies Used

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| NLP | NLTK |
| Machine Learning | Scikit-learn |
| Vectorization | TF-IDF |
| Classifier | Logistic Regression |
| Data Processing | Pandas |
| Model Serialization | Joblib |
| Frontend | Streamlit |

---

# ⚙️ Installation

Clone the repository

```bash
git clone https://github.com/yourusername/CampusAI.git
```

Move into the project

```bash
cd CampusAI
```

Install dependencies

```bash
pip install -r requirements.txt
```

Run the application

```bash
streamlit run app.py
```

---

# 📊 Model Performance

Current model performance on the intent classification dataset:

| Metric | Score |
|---------|------:|
| Accuracy | 72% |
| Precision | 0.76 |
| Recall | 0.72 |
| F1 Score | 0.71 |

> Performance is expected to improve with a larger training dataset and advanced embedding models.

---

# 📸 Screenshots

Add screenshots here after completing the UI.

Example:

- Home Screen
- Chat Interface
- Sample Conversation
- NLP Details Panel

---

# 💡 Sample Questions

```
What is the last date for admission?

What is the fee for B.Sc AI?

Do you provide scholarships?

Who are the top recruiters?

Is hostel available?

What documents are required?

Where is the admission office?

Does the campus have Wi-Fi?
```

---

# 🔮 Future Improvements

- Replace TF-IDF with Sentence Transformers
- Fine-tune BERT for intent classification
- Replace rule-based NER with spaCy or a trained NER model
- Add conversation context for multi-turn dialogue
- Support multilingual queries
- Deploy using Streamlit Community Cloud
- Integrate Retrieval-Augmented Generation (RAG)
- Add voice-based interaction

---

# 👩‍💻 Author

**Shriya Patil**

B.Sc. Artificial Intelligence Student

---

# 📄 License

This project is licensed under the MIT License.