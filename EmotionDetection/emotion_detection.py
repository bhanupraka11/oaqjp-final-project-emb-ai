import requests
import json


def emotion_detector(text_to_analyse):
    if not text_to_analyse or not text_to_analyse.strip():
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    url = (
        'https://sn-watson-emotion.labs.skills.network/v1/'
        'watson.runtime.nlp.v1/NlpService/EmotionPredict'
    )
    headers = {
        'grpc-metadata-mm-model-id': 'emotion_aggregated-workflow_lang_en_stock'
    }
    payload = {"raw_document": {"text": text_to_analyse}}

    response = requests.post(url, headers=headers, json=payload)

    if response.status_code == 400:
        return {
            'anger': None,
            'disgust': None,
            'fear': None,
            'joy': None,
            'sadness': None,
            'dominant_emotion': None
        }

    response_data = json.loads(response.text)
    emotions_raw = (
        response_data
        .get('emotionPredictions', [{}])[0]
        .get('emotion', {})
    )

    emotion_scores = {
        'anger':   emotions_raw.get('anger', 0),
        'disgust': emotions_raw.get('disgust', 0),
        'fear':    emotions_raw.get('fear', 0),
        'joy':     emotions_raw.get('joy', 0),
        'sadness': emotions_raw.get('sadness', 0),
    }

    dominant_emotion = max(emotion_scores, key=emotion_scores.get)
    return {**emotion_scores, 'dominant_emotion': dominant_emotion}
