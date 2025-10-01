from flask import Flask, render_template, request
from EmotionDetection import emotion_detector

app = Flask(__name__)

@app.route("/")
def index():
    # usa o index.html já fornecido no diretório templates/
    return render_template("index.html")

@app.route("/emotionDetector", methods=["GET", "POST"])
def emotion_detect():
    # aceita JSON, form e querystring
    text_to_analyze = None
    if request.method == "POST":
        if request.is_json:
            data = request.get_json(silent=True) or {}
            text_to_analyze = data.get("text") or data.get("textToAnalyze") or data.get("text_to_analyze")
        else:
            text_to_analyze = request.form.get("textToAnalyze")
    else:  # GET
        text_to_analyze = request.args.get("textToAnalyze")

    if not text_to_analyze or not text_to_analyze.strip():
        return "Invalid text! Please try again!", 400

    result = emotion_detector(text_to_analyze)

    anger   = result.get("anger")
    disgust = result.get("disgust")
    fear    = result.get("fear")
    joy     = result.get("joy")
    sadness = result.get("sadness")
    dom     = result.get("dominant_emotion")

    if None in (anger, disgust, fear, joy, sadness) or not dom:
        return "Invalid text! Please try again!", 500

    formatted = (
        f"For the given statement, the system response is "
        f"'anger': {anger}, 'disgust': {disgust}, 'fear': {fear}, "
        f"'joy': {joy} and 'sadness': {sadness}. The dominant emotion is {dom}."
    )
    return formatted

if __name__ == "__main__":
    # app em localhost:5000
    app.run(host="0.0.0.0", port=5000)
