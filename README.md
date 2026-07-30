# 🎓 CampusAI – Intelligent University Chatbot

![Python](https://img.shields.io/badge/Python-3.11-blue)

![Streamlit](https://img.shields.io/badge/Streamlit-App-red)

![License](https://img.shields.io/badge/License-MIT-green)

An AI-powered University Chatbot built using **Natural Language Processing (NLP)**. The chatbot understands user queries related to admissions, courses, eligibility, fees, scholarships, hostel, placements, documents, contact information, and campus facilities.

The system uses **text preprocessing**, **TF-IDF feature extraction**, **Logistic Regression for intent classification**, **rule-based Named Entity Recognition (NER)**, and a **knowledge base retrieval system** to provide accurate responses through an interactive **Streamlit** web application.

# 🚀 Project Highlights

- Developed an end-to-end NLP chatbot for university information.
- Achieved 72% intent classification accuracy using Logistic Regression and TF-IDF.
- Implemented rule-based Named Entity Recognition for entity extraction.
- Built an interactive Streamlit web application.
- Deployed the chatbot online using Streamlit Community Cloud.

# 🌐 Live Demo

Try the chatbot here:

https://campusai-nlp-chatbot-v1.streamlit.app/

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
CampusAI-NLP-Chatbot/
│
├── app.py
├── chatbot.py
├── preprocess.py
├── ner.py
├── train_model.py
├── evaluate_model.py
├── requirements.txt
├── README.md
├── LICENSE
│
├── data/
├── models/
├── evaluation/
└── screenshots/
```

---

# 🛠️ Technologies Used

| Category | Technology |
|----------|------------|
| Programming Language | Python |
| NLP | NLTK + spaCy |
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
git clone https://github.com/ShriyaP1966/CampusAI-NLP-Chatbot.git
```

Move into the project

```bash
cd CampusAI-NLP-Chatbot
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

The intent classification model was trained on a dataset containing 250 manually labeled queries across 10 university-related intents.

> Performance is expected to improve with a larger training dataset and advanced embedding models.


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

- Integrate Large Language Models (LLMs)
- Improve intent classification with transformer embeddings
- Fine-tune a custom Named Entity Recognition model
- Add Retrieval-Augmented Generation (RAG)
- Enable voice interaction
- Support multilingual conversations

---

# 👩‍💻 Author

**Shriya Patil**

B.Sc. Artificial Intelligence Student

---

# 📄 License

This project is licensed under the MIT License.