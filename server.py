from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

@app.route("/emotionDetector")
def sent_detector():
    text_to_analyze = request.args.get('textToAnalyze')
    if not textToAnalyze:
        return "Please provide some text to analyze."
    
    response = emotion_detector(text_to_analyze)
    if response['dominant_emotion'] is None:
        return "Invalid text! Please try again!"
        
    return (
        f"For the given statement, the system response is: "
        f"<b>Anger</b>: {response['anger']}, <b>Disgust</b>: {response['disgust']}, "
        f"<b>Fear</b>: {response['fear']}, <b>Joy</b>: {response['joy']} and "
        f"<b>Sadness</b>: {response['sadness']}. "
        f"<br>The dominant emotion is <b>{response['dominant_emotion']}</b>."
    )

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)