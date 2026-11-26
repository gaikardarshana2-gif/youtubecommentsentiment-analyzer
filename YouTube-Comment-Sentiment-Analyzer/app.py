from flask import Flask, render_template, request, jsonify
from nltk.sentiment.vader import SentimentIntensityAnalyzer
import nltk


# =========================================
# DOWNLOAD VADER DATA
# =========================================

nltk.download("vader_lexicon")


# =========================================
# CREATE FLASK APP
# =========================================

app = Flask(__name__)


# =========================================
# VADER SENTIMENT ANALYZER
# =========================================

sentiment_analyzer = SentimentIntensityAnalyzer()


# =========================================
# HOME PAGE
# =========================================

@app.route("/")
def home():

    return render_template("home.html")


# =========================================
# ANALYZER PAGE
# =========================================

@app.route("/analyzer")
def analyzer_page():

    return render_template("index.html")


# =========================================
# HISTORY PAGE
# =========================================

@app.route("/history")
def history():

    return render_template("history.html")


# =========================================
# ANALYZE COMMENT
# =========================================

@app.route("/analyze", methods=["POST"])
def analyze():

    data = request.get_json()

    comment = data.get(
        "comment",
        ""
    ).strip()


    # Check empty comment

    if not comment:

        return jsonify({
            "error": "Please enter a comment."
        }), 400


    # VADER analysis

    scores = sentiment_analyzer.polarity_scores(
        comment
    )


    compound = scores["compound"]


    # Determine sentiment

    if compound >= 0.05:

        sentiment = "Positive"
        emoji = "😊"


    elif compound <= -0.05:

        sentiment = "Negative"
        emoji = "😞"


    else:

        sentiment = "Neutral"
        emoji = "😐"


    # Send result to frontend

    return jsonify({

        "comment": comment,

        "sentiment": sentiment,

        "emoji": emoji,

        "compound": round(
            compound,
            3
        ),

        "positive": round(
            scores["pos"] * 100,
            2
        ),

        "neutral": round(
            scores["neu"] * 100,
            2
        ),

        "negative": round(
            scores["neg"] * 100,
            2
        )

    })


# =========================================
# RUN SERVER
# =========================================

if __name__ == "__main__":

    print()
    print("==========================================")
    print("     YOUTUBE COMMENT SENTIMENT ANALYZER")
    print("==========================================")
    print()
    print("Server Started Successfully")
    print()
    print("Open in Chrome:")
    print("http://127.0.0.1:5000")
    print()
    print("==========================================")
    print()


    app.run(
        host="0.0.0.0",
        port=5000,
        debug=True
    )