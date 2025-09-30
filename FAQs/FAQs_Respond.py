import random
import json
import os
from sklearn.metrics.pairwise import cosine_similarity
from FAQs.vectorising_FAQS import get_vectorizer_and_vectors
from rapidfuzz import fuzz

UNKNOWN_FILE = "FAQs/unknown_questions.json"

def save_unknown_question(user_msg):
    """Save unanswered queries for future learning."""
    if not os.path.exists(UNKNOWN_FILE):
        with open(UNKNOWN_FILE, "w") as f:
            json.dump([], f, indent=4)

    with open(UNKNOWN_FILE, "r") as f:
        data = json.load(f)

    if user_msg not in [q["question"] for q in data]:
        data.append({"question": user_msg, "answers": []})

    with open(UNKNOWN_FILE, "w") as f:
        json.dump(data, f, indent=4)


def learn_new_answer(question, answer):
    """Teach the bot a new answer for an unknown question."""
    if not os.path.exists(UNKNOWN_FILE):
        return "No unknown questions stored."

    with open(UNKNOWN_FILE, "r") as f:
        data = json.load(f)

    for q in data:
        if q["question"].lower() == question.lower():
            q["answers"].append(answer)
            break
    else:
        data.append({"question": question, "answers": [answer]})

    with open(UNKNOWN_FILE, "w") as f:
        json.dump(data, f, indent=4)

    return f"Learned a new answer for: '{question}'"


def get_faq_response(user_msg):
    vectorizer, vectors, questions, faq_data = get_vectorizer_and_vectors()
    
    # Transform user message
    user_vec = vectorizer.transform([user_msg])
    
    # Compute cosine similarity
    similarities = cosine_similarity(user_vec, vectors)
    best_idx = similarities.argmax()
    best_score = similarities[0][best_idx]

    # Compute fuzzy ratio for typo-tolerance
    fuzzy_scores = [fuzz.ratio(user_msg.lower(), q.lower()) for q in questions]
    best_fuzzy_idx = fuzzy_scores.index(max(fuzzy_scores))
    best_fuzzy_score = max(fuzzy_scores) / 100  # normalize 0-1

    # Use the better of cosine similarity or fuzzy match
    if max(best_score, best_fuzzy_score) > 0.5:
        if best_score >= best_fuzzy_score:
            answers = faq_data[best_idx]["answers"]
        else:
            answers = faq_data[best_fuzzy_idx]["answers"]
        return random.choice(answers)
    else:
        # Save unknown question for learning
        save_unknown_question(user_msg)

        fallback_responses = [
            "I don’t know that yet 🤔, but I can learn if you teach me!",
            "Hmm… that’s new for me. Want to give me the right answer?",
            "I’m not sure, but I can remember if you tell me 😊",
            "That’s outside my knowledge. Would you like to teach me?",
            "I’m just a humble currency bot 😅", 
            "I know dollars, euros, and sarcasm 💸",
            "Ask me to convert money, or I’ll start charging fees 😎",
            "Want currency rates or just vibes? ✨"
        ]
        return random.choice(fallback_responses)
