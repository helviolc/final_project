import requests

URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

def _empty_result():
    return {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }

def emotion_detector(text_to_analyze):
    """
    Calls Watson NLP EmotionPredict and returns:
    {
      'anger': float|None, 'disgust': float|None, 'fear': float|None,
      'joy': float|None, 'sadness': float|None, 'dominant_emotion': str|None
    }
    - For blank/invalid input (API 400) returns all None.
    """
    # Early guard (saves a network call) – still handle 400 explicitly below
    if not text_to_analyze or not str(text_to_analyze).strip():
        return _empty_result()

    payload = {"raw_document": {"text": text_to_analyze}}

    try:
        response = requests.post(URL, headers=HEADERS, json=payload)
    except requests.RequestException:
        # Network or other transport error → treat as invalid
        return _empty_result()

    # Explicit rubric requirement: if API says 400, return all None
    if response.status_code == 400:
        return _empty_result()

    if response.status_code != 200:
        # Any other unexpected status → also return all None
        return _empty_result()

    data = response.json()
    preds = data.get('emotionPredictions') or data.get('predictions') or []
    if not preds:
        return _empty_result()

    emotions = preds[0].get('emotion', {})
    result = _empty_result()
    for k in ['anger', 'disgust', 'fear', 'joy', 'sadness']:
        result[k] = emotions.get(k)

    # Dominant emotion = highest score among the 5 (when not None)
    scores_only = {k: v for k, v in result.items()
                   if k != 'dominant_emotion' and v is not None}
    if scores_only:
        result['dominant_emotion'] = max(scores_only, key=scores_only.get)

    return result