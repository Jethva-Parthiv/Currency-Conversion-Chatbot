import random
from sklearn.metrics.pairwise import cosine_similarity
from FAQs.vectorising_FAQS import get_vectorizer_and_vectors
from rapidfuzz import fuzz


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
        fallback_responses = [
            "I’m just a humble currency bot 😅",
            "I know dollars, euros, and sarcasm 💸",
            "Ask me to convert money, or I’ll start charging fees 😎",
            "Want currency rates or just vibes? ✨"
        ]
        return random.choice(fallback_responses)
