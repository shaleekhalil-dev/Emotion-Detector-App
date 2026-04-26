"""
Flask server for the Emotion Detection application.
This module provides endpoints for analyzing text emotions using Watson NLP.
"""
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route("/emotionDetector")
def sent_detector():
    """
    Analyzes the input text for emotions and returns the formatted response.
    Handles blank input by checking for None in the dominant_emotion.
    """
    text_to_analyze = request.args.get('textToAnalyze')
    response = emotion_detector(text_to_analyze)

    # التحقق من المدخلات الفارغة (Task 7)
    if response['dominant_emotion'] is None:
        return "Invalid text! Please try again!"

    # تنسيق الرد النهائي المطلوب للمشروع
    return (
        f"For the given statement, the system response is "
        f"'anger': {response['anger']}, 'disgust': {response['disgust']}, "
        f"'fear': {response['fear']}, 'joy': {response['joy']} and "
        f"'sadness': {response['sadness']}. "
        f"The dominant emotion is {response['dominant_emotion']}."
    )

@app.route("/")
def render_index_page():
    """
    Renders the main application interface (index.html).
    """
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
