"""Flask app for Watson NLP Emotion Detection.

Exposes:
- GET /               -> loads index.html
- GET/POST /emotionDetector -> runs emotion detection and returns a formatted string
"""

from typing import Optional
from flask import Flask, render_template, request
from EmotionDetection import emotion_detector  # pylint: disable=import-error

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index() -> str:
    """Render the home page with the input form."""
    return render_template("index.html")


def _get_text_from_request() -> Optional[str]:
    """Extract 'textToAnalyze' from JSON body, form data, or query string."""
    if request.method == "POST":
        if request.is_json:
            data = request.get_json(silent=True) or {}
            return (
                data.get("text")
                or data.get("textToAnalyze")
                or data.get("text_to_analyze")
            )
        return request.form.get("textToAnalyze")
    return request.args.get("textToAnalyze")


@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detect() -> str:
    """Run emotion detection and return the formatted response or an error message."""
    text_to_analyze = _get_text_from_request()
    if not text_to_analyze or not text_to_analyze.strip():
        return "Invalid text! Please try again!"

    result = emotion_detector(text_to_analyze)

    anger = result.get("anger")
    disgust = result.get("disgust")
    fear = result.get("fear")
    joy = result.get("joy")
    sadness = result.get("sadness")
    dominant = result.get("dominant_emotion")

    # When API returns None values / dominant is None, show error message
    if dominant is None or None in (anger, disgust, fear, joy, sadness):
        return "Invalid text! Please try again!"

    formatted = (
        "For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. The dominant emotion is {dominant}."
    )
    return formatted


if __name__ == "__main__":
    # Run on localhost:5000 for the lab
    app.run(host="0.0.0.0", port=5000)
