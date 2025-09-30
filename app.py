from flask import Flask, render_template, request, jsonify
import requests
import spacy
from word2number import w2n
from Model import predict_intent
from Utility import format_response, preprocess_text
from FAQs import get_faq_response
from static import CURRENCY_MAP, DEFAULT_TARGET_CURRENCY

app = Flask(__name__)

# Load spaCy NLP model
nlp = spacy.load("en_core_web_sm")


# -------------------- CURRENCY EXTRACTION --------------------
def extract_currency_and_amount(text):
    text = preprocess_text(text)  # Preprocess first
    text = text.lower()
    doc = nlp(text)

    amount, from_curr, to_curr = None, None, None

    # Extract amount (digits)
    for token in doc:
        if token.like_num:
            try:
                amount = float(token.text)
                break
            except:
                pass

    # Extract amount (words → number)
    if amount is None:
        words = text.replace("-", " ").split()
        for i in range(len(words)):
            try:
                amt = w2n.word_to_num(" ".join(words[i:i+3]))
                amount = float(amt)
                break
            except:
                continue

    # Detect currencies
    currencies = []
    for token in doc:
        if token.text in CURRENCY_MAP:
            currencies.append(CURRENCY_MAP[token.text])

    if len(currencies) >= 2:
        from_curr, to_curr = currencies[0], currencies[1]
    elif len(currencies) == 1:
        from_curr = currencies[0]
        to_curr = DEFAULT_TARGET_CURRENCY
    return amount, from_curr, to_curr

# -------------------- CONVERSION --------------------
def convert_currency(amount, from_curr, to_curr):
    try:
        url = f"https://open.er-api.com/v6/latest/{from_curr}"
        res = requests.get(url).json()
        rate = res["rates"].get(to_curr)
        if rate:
            return round(amount * rate, 2)
        return None
    except:
        return None

# -------------------- ROUTES --------------------
@app.route("/")
def index():
    return render_template("index.html")

@app.route("/chat", methods=["POST"])
def chat():
    user_msg = request.json.get("message", "")

    # Predict intent
    intent = predict_intent(user_msg)

    if intent == "convert":
        amount, from_curr, to_curr = extract_currency_and_amount(user_msg)
        if amount and from_curr and to_curr:
            converted = convert_currency(amount, from_curr, to_curr)
            if converted is not None:
                bot_reply = format_response(amount, from_curr, to_curr, converted)
            else:
                bot_reply = "Oops! Couldn’t fetch rates right now 🤖"
        else:
            bot_reply = "I didn’t quite catch the currencies or amount 🧐. Try: 'Convert 50 USD to INR'."
    else:
         # Handle FAQ/non-conversion queries with dynamic learning
        bot_reply = get_faq_response(user_msg)
    print(f"User: {user_msg} | Intent: {intent} | Bot: {bot_reply}")
    return jsonify({"reply": bot_reply})

if __name__ == "__main__":
    app.run(debug=True)

