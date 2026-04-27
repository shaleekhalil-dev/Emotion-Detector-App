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
    text = request.args.get('textToAnalyze', '').strip()
    ui_lang = request.args.get('ui_lang', 'en')
    
    if not text: 
        return "الخيار فارغ!" if ui_lang == "ar" else "Input is empty!"

    # 1. شرط علامة السؤال (إذا ما في علامة سؤال، الجواب مش بصوت شموسة)
    if not text.endswith('؟') and not text.endswith('?'):
        return "لازم تسأل بعلامة سؤال عشان شموسة ترد عليك! 🙄" if ui_lang == "ar" else "Add a question mark so Shams can answer! 🙄"

    # تحليل النص عبر الدالة الأساسية
    result = emotion_detector(text)
    
    # 2. شرط الأسئلة غير المدرجة (إذا لم يتم التعرف على رد شخصي أو مشاعر قوية)
    # ملاحظة: سنعتبر أي نتيجة 'dominant_emotion' فيها None أو غير موجودة كـ "حل عني"
    if not result or result.get('dominant_emotion') is None:
        return "حل عني!" if ui_lang == "ar" else "Leave me alone!"

    # الرد بناءً على نوع النتيجة (شخصي أو تحليل مشاعر)
    if result.get('is_personal'):
        res_text = result['dominant_emotion']
    else:
        # ترجمة المشاعر إذا كانت اللغة عربية
        if ui_lang == "ar":
            res_text = emotion_map.get(result['dominant_emotion'].lower(), "حل عني!")
        else:
            res_text = result['dominant_emotion']

    prefix = "النتيجة: " if ui_lang == "ar" else "Result: "
    user_msg = "منور الموقع يا بطل!" if ui_lang == "ar" else "Welcome to the site, hero!"
    
    return f"{prefix} <b>{res_text}</b> <br><small>{user_msg}</small>"

@app.route("/")
def render_index_page():
    return render_template('index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)