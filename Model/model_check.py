import os
import joblib
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
import re

MODEL_PATH  = os.path.join(os.path.dirname(__file__), "intent_model.pkl")

VECTORIZER_PATH = os.path.join(os.path.dirname(__file__), "vectorizer.pkl")

def normalize(text):
    text = text.lower()
    text = re.sub(r"₹|rs|rupees?", " inr ", text)
    text = re.sub(r"doll(e|a)rs?|bucks?", " usd ", text)
    text = re.sub(r"→", " to ", text)
    text = re.sub(r"[^a-z0-9\s]", " ", text)  # keep alphanum
    return text.strip()


convert_examples = [
    "convert 100 usd to inr", "change 50 dollars into rupees",
    "how much is 70 euros in dollars", "show me 1 gbp in inr",
    "exchange 20 jpy into eur", "can you convert 500 rupees in usd",
    "tell me the dollar value of 1000 inr", "how many bucks is 300 inr",
    "1 crore inr to usd", "rs 500 to usd", "doller 200 to inr",
    "value of ₹999 in dollars", "give conversion from inr to usd"
]

chitchat_examples = [
    "hello bot", "hi there", "how are you", "tell me a joke",
    "what’s up", "who made you", "do you like pizza", "random talk",
    "good morning", "what’s your name", "bye", "thank you"
]


train_sentences = convert_examples + chitchat_examples
train_labels = ["convert"]*len(convert_examples) + ["chitchat"]*len(chitchat_examples)

# -------------------- LOAD OR TRAIN MODEL --------------------
if os.path.exists(MODEL_PATH) and os.path.exists(VECTORIZER_PATH):
    clf = joblib.load(MODEL_PATH)
    vectorizer = joblib.load(VECTORIZER_PATH)
else:
    vectorizer = TfidfVectorizer(ngram_range=(1,3), analyzer="char_wb")
    X = vectorizer.fit_transform([normalize(s) for s in train_sentences])
    clf = LogisticRegression(max_iter=200)
    clf.fit(X, train_labels)
    joblib.dump(clf, MODEL_PATH)
    joblib.dump(vectorizer, VECTORIZER_PATH)


def predict_intent(text):
    X_test = vectorizer.transform([normalize(text)])
    return clf.predict(X_test)[0]


complex_queries = [
    # Indirect questions
    "If I bring 7500 rupees to the US, how much money will I actually have in dollars?",
    "Suppose I have ₹12,345, what’s that in USD?",
    "How many American dollars can I get for fifty thousand INR?",
    "Exchange rate please: 2.5 lakh INR to USD?",
    "Could you calculate the value of 999.99 INR in dollars?",

    # Multiple currencies
    "Convert 200 USD into INR and also tell me what 200 INR is in USD",
    "Is 100 euros more than 100 dollars in INR?",
    "Change 10 GBP into INR first, then to USD",
    "How many yen equal 1 rupee?",
    "Convert 300 INR to USD and EUR",

    # Comparative / Yes-No style
    "Is 10,000 INR equal to 200 USD?",
    "Would 500 INR be enough to buy something worth $6?",
    "Tell me if 1500 rupees is more than 20 dollars",
    "Is 1 INR still less than 0.02 USD?",
    "Does ₹250 convert to more than 3 dollars?",

    # Tricky formatting
    "convert 1e5 inr to usd",          # scientific notation
    "what’s the usd value of INR 123,456.78?",
    "1000rs in usd??",
    "pls convrt INR 250.50 into doller",
    "how much usd $$ for 75₹",

    # Ambiguous / conversational
    "How many dollars for one crore?",
    "I’m planning a trip to USA, got 2 lakh INR – what’s that in USD?",
    "Between INR and USD, how much is 999 rupees?",
    "Need conversion from indian money 3333 to us money",
    "Tell me dollar worth of 1 rupee coin"
]


# r = 0
# for i in complex_queries:
#     intent = predict_intent(i)

#     if intent == "convert":
#         print("Intent: convert",end=" ")
#         r += 1  
#         print(r)
#     else:
#         print("Intent: chitchat",end=" ")
#         r += 1
#         print(r)
