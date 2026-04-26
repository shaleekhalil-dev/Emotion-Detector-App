import requests
import json
import random

def emotion_detector(text_to_analyze):
    text = text_to_analyze.lower().strip()
    
    # موسوعة شعلي الشخصية
    shalee_kb = {
        "اسمك": "اسمي شعلي خليل، قائد استراتيجي هجين ومبرمج.",
        "بتشتغل": "أنا مبرمج Full Stack وخبير في إدارة الموارد البشرية وأنسنة العمل.",
        "بتدرس": "بدرس ماجستير موارد بشرية، وعيني على الدكتوراه (DBA) بإذن الله.",
        "طبختك": "المقلوبة طبعاً، سيد الأكلات!",
        "القيادة": "القيادة هي أنك تلمس قلوب الناس وتطور عقولهم."
    }

    # 1. البحث في موسوعة شعلي
    for key in shalee_kb:
        if key in text:
            return {"dominant_emotion": shalee_kb[key], "is_personal": True}

    # 2. تدخل "شموسة" بالردود المسكتة
    shams_triggers = ["بتحبني", "بتكرهني", "ليش", "كيف", "شو", "؟", "بتحب", "مين"]
    if any(word in text for word in shams_triggers):
        shams_responses = [
            'بديش! "بصوت شموسة" 🤐', 
            'حل عني! "بصوت شموسة" 🙄'
        ]
        return {"dominant_emotion": random.choice(shams_responses), "is_personal": True}

    # 3. تحليل المشاعر العميق (Watson)
    url = 'https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict'
    headers = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}
    input_json = { "raw_document": { "text": text_to_analyze } }
    
    try:
        response = requests.post(url, json=input_json, headers=headers, timeout=5)
        if response.status_code == 200:
            formatted_response = json.loads(response.text)
            emotions = formatted_response['emotionPredictions'][0]['emotion']
            dominant = max(emotions, key=emotions.get)
            return {"dominant_emotion": dominant, "lang": "en", "is_personal": False}
    except:
        return {"dominant_emotion": "Neutral / محايد", "lang": "ar", "is_personal": False}