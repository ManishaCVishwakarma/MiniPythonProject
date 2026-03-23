from flask import Flask, request, jsonify
import json
import os

app = Flask(__name__)

# ---------------------------
# Word Lists
# ---------------------------
positive_words = ["good", "happy", "great", "excellent", "love"]
negative_words = ["bad", "sad", "hate", "angry", "worst"]

BLOCK_FILE = "blocked_words.json"

# ---------------------------
# Create blocked_words.json if not exists
# ---------------------------
if not os.path.exists(BLOCK_FILE):
    with open(BLOCK_FILE, "w") as f:
        json.dump([], f)

# ---------------------------
# Load blocked words
# ---------------------------
def load_blocked_words():
    with open(BLOCK_FILE, "r") as f:
        return json.load(f)

# ---------------------------
# Save blocked words
# ---------------------------
def save_blocked_words(words):
    with open(BLOCK_FILE, "w") as f:
        json.dump(words, f)

# ---------------------------
# Home Route
# ---------------------------
@app.route("/")
def home():
    return "Project2 API is running!"

# ---------------------------
# Analyze Sentiment
# ---------------------------
@app.route("/analyze", methods=["POST"])
def analyze():
    try:
        data = request.get_json()

        if not data or "text" not in data:
            return jsonify({"error": "Text is required"}), 400

        text = data["text"].lower()
        blocked_words = load_blocked_words()

        # Check blocked words
        for word in blocked_words:
            if word in text:
                return jsonify({"message": "Text contains blocked word"}), 400

        pos = sum(word in text for word in positive_words)
        neg = sum(word in text for word in negative_words)

        if pos > neg:
            result = "Positive"
        elif neg > pos:
            result = "Negative"
        else:
            result = "Neutral"

        return jsonify({"sentiment": result}), 200

    except Exception as e:
        return jsonify({"error": "Server Error"}), 500

# ---------------------------
# Block Word API
# ---------------------------
@app.route("/block", methods=["POST"])
def block_word():
    data = request.get_json()

    if not data or "word" not in data:
        return jsonify({"error": "Word is required"}), 400

    words = load_blocked_words()
    words.append(data["word"])
    save_blocked_words(words)

    return jsonify({"message": "Word blocked successfully"}), 200

# ---------------------------
# Unblock Word API
# ---------------------------
@app.route("/unblock", methods=["POST"])
def unblock_word():
    data = request.get_json()

    if not data or "word" not in data:
        return jsonify({"error": "Word is required"}), 400

    words = load_blocked_words()

    if data["word"] in words:
        words.remove(data["word"])
        save_blocked_words(words)
        return jsonify({"message": "Word unblocked successfully"}), 200
    else:
        return jsonify({"error": "Word not found"}), 400

# ---------------------------
# Run Server
# ---------------------------
if __name__ == "__main__":
    app.run(debug=True)