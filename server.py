import os
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)
COUNTER_FILE = "visitor_count.txt"

emotion_map = {
    "joy": "السعادة 😊", "anger": "الغضب 😡", 
    "disgust": "الاشمئزاز 🤢", "fear": "الخوف 😨", "sadness": "الحزن 😢"
}

def get_visitor_count():
    if not os.path.exists(COUNTER_FILE):
        with open(COUNTER_FILE, "w") as f: f.write("0")
    with open(COUNTER_FILE, "r") as f:
        try: count = int(f.read())
        except: count = 0
    count += 1
    with open(COUNTER_FILE, "w") as f: f.write(str(count))
    return count

@app.route("/emotionDetector")
def sent_detector():
    text = request.args.get('textToAnalyze')
    ui_lang = request.args.get('ui_lang', 'en')
    if not text: return "Input is empty!"
    
    result = emotion_detector(text)
    count = get_visitor_count()
    
    if result.get('is_personal'):
        res_text = result['dominant_emotion']
    else:
        if ui_lang == "ar":
            res_text = emotion_map.get(result['dominant_emotion'].lower(), result['dominant_emotion'])
        else:
            res_text = result['dominant_emotion']

    prefix = "النتيجة: " if ui_lang == "ar" else "Result: "
    user_msg = f"أنت المستخدم رقم: {count}" if ui_lang == "ar" else f"You are visitor number: {count}"
    
    return f"{prefix} <b>{res_text}</b> <br><small>{user_msg}</small>"

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)