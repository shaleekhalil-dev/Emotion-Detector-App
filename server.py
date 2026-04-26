import os
from flask import Flask, render_template, request
from EmotionDetection.emotion_detection import emotion_detector

app = Flask(__name__)

# مترجم المشاعر
emotion_map = {
    "joy": "السعادة 😊", "anger": "الغضب 😡", 
    "disgust": "الاشمئزاز 🤢", "fear": "الخوف 😨", "sadness": "الحزن 😢"
}

@app.route("/emotionDetector")
def sent_detector():
    text = request.args.get('textToAnalyze')
    ui_lang = request.args.get('ui_lang', 'en')
    if not text: return "Input is empty!"
    
    result = emotion_detector(text)
    
    # الرد بناءً على نوع النتيجة (شخصي أو تحليل مشاعر)
    if result.get('is_personal'):
        res_text = result['dominant_emotion']
    else:
        if ui_lang == "ar":
            res_text = emotion_map.get(result['dominant_emotion'].lower(), result['dominant_emotion'])
        else:
            res_text = result['dominant_emotion']

    prefix = "النتيجة: " if ui_lang == "ar" else "Result: "
    # عداد وهمي بسيط أو جملة ترحيبية لأن فيرسال لا يدعم الكتابة على الملفات
    user_msg = "منور الموقع يا بطل!" if ui_lang == "ar" else "Welcome to the site, hero!"
    
    return f"{prefix} <b>{res_text}</b> <br><small>{user_msg}</small>"

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)