import json
import os
from sklearn.feature_extraction.text import TfidfVectorizer
import pickle

# FAQ_FILE = "bot_faq.json"
FAQ_FILE = os.path.join(os.path.dirname(__file__), "faq_data.json")

VECTORS_FILE = os.path.join(os.path.dirname(__file__), "faq_vectors.pkl")

# Load FAQs
def load_faqs():
    with open(FAQ_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

# Precompute TF-IDF vectors
def get_vectorizer_and_vectors():
    if os.path.exists(VECTORS_FILE):
        # Load precomputed vectorizer and vectors
        with open(VECTORS_FILE, "rb") as f:
            vectorizer, vectors, questions, faq_data = pickle.load(f)
    else:
        faq_data = load_faqs()
        questions = [item["question"] for item in faq_data]
        vectorizer = TfidfVectorizer()
        vectors = vectorizer.fit_transform(questions)
        # Save for future
        with open(VECTORS_FILE, "wb") as f:
            pickle.dump((vectorizer, vectors, questions, faq_data), f)
    return vectorizer, vectors, questions, faq_data
