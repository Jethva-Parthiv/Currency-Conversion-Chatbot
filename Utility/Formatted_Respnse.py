import random


# Map currencies to emojis
CURRENCY_EMOJI = {
    "USD": "💵", "INR": "₹", "EUR": "💶", "JPY": "¥", "GBP": "£",
    "AUD": "A$", "CAD": "C$", "CHF": "CHF", "CNY": "¥"
}

# Combined response templates
RESPONSES = [
    # Original emoji-style
    "{from_emoji}{amount} {from_curr} ≈ {to_emoji}{converted} {to_curr}! 💰",
    "You’d get around {to_emoji}{converted} {to_curr} for {from_emoji}{amount} {from_curr}.",
    "📈 {from_emoji}{amount} {from_curr} → {to_emoji}{converted} {to_curr}",
    "Here’s the conversion: {to_emoji}{converted} {to_curr} for {from_emoji}{amount} {from_curr}!",
    "That’s about {to_emoji}{converted} {to_curr} 😉",

    # Original non-emoji, formal-style
    "{amount} {from_curr} equals {converted:.2f} {to_curr} today.",
    "You'll get about {converted:.2f} {to_curr} for {amount} {from_curr}.",
    "If you exchange {amount} {from_curr}, you'll receive ~{converted:.2f} {to_curr}.",
    "At today’s rate, {amount} {from_curr} = {converted:.2f} {to_curr}.",
    "Sure thing! {amount} {from_curr} will get you about {converted:.2f} {to_curr} right now.",
    "At the current rate, {amount} {from_curr} comes to roughly {converted:.2f} {to_curr}.",
    "Exchanging {amount} {from_curr}? You’d get around {converted:.2f} {to_curr} today.",
    "{amount} {from_curr} equals about {converted:.2f} {to_curr} at today’s rate.",
    "Right now, {amount} {from_curr} is worth approximately {converted:.2f} {to_curr}."
]

def format_response(amount, from_curr, to_curr, converted):
    from_emoji = CURRENCY_EMOJI.get(from_curr, "")
    to_emoji = CURRENCY_EMOJI.get(to_curr, "")
    
    template = random.choice(RESPONSES)
    return template.format(
        amount=amount,
        from_curr=from_curr.upper(),
        to_curr=to_curr.upper(),
        converted=converted,
        from_emoji=from_emoji,
        to_emoji=to_emoji
    )



def same_currency_reply(currency):
    replies = [
        f"Converting {currency} to {currency}? Wow, mind blown 🤯!",
        f"Hmm... {currency} is already {currency}. Are we practicing math? 😄",
        f"Trying to turn {currency} into more {currency}? Magic! 🪄",
        f"{currency} → {currency}. That's a classic! 😂",
        f"Did you just try to duplicate {currency}? Nice try 😎",
        f"Oops! {currency} to {currency} is like copying homework 😜",
    ]
    return random.choice(replies)



# Symbols mapping
SYMBOL_MAP = {
    "$": "usd",
    "₹": "inr",
    "€": "eur",
    "£": "gbp",
    "¥": "jpy"
}

def preprocess_text(text):
    # Replace symbols with currency words
    for symbol, currency_word in SYMBOL_MAP.items():
        text = text.replace(symbol, f" {currency_word} ")
    # Add space between numbers and letters (e.g., 100inr → 100 inr)
    new_text = ""
    for i, c in enumerate(text):
        if i > 0 and c.isalpha() and text[i-1].isdigit():
            new_text += " "
        new_text += c
    return new_text.lower()

