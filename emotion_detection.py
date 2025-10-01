import requests

URL = "https://sn-watson-emotion.labs.skills.network/v1/watson.runtime.nlp.v1/NlpService/EmotionPredict"
HEADERS = {"grpc-metadata-mm-model-id": "emotion_aggregated-workflow_lang_en_stock"}

def emotion_detector(text_to_analyze):
    """
    Chama a API Watson NLP EmotionPredict e retorna um dicionário com
    as 5 emoções e a 'dominant_emotion' (maior score).
    """
    # retorno padrão (em caso de erro/entrada vazia)
    result = {
        'anger': None,
        'disgust': None,
        'fear': None,
        'joy': None,
        'sadness': None,
        'dominant_emotion': None
    }

    if not text_to_analyze or not text_to_analyze.strip():
        return result

    payload = {"raw_document": {"text": text_to_analyze}}
    response = requests.post(URL, headers=HEADERS, json=payload)

    if response.status_code != 200:
        return result

    data = response.json()  # converte string JSON para dict

    # estrutura típica: data['emotionPredictions'][0]['emotion']
    preds = data.get('emotionPredictions') or data.get('predictions') or []
    if not preds:
        return result

    emotions = preds[0].get('emotion', {})
    # copia apenas as cinco emoções requisitadas
    for k in ['anger', 'disgust', 'fear', 'joy', 'sadness']:
        result[k] = emotions.get(k)

    # calcula a emoção dominante (maior score entre as que não são None)
    scores_only = {k: v for k, v in result.items() if k != 'dominant_emotion' and v is not None}
    if scores_only:
        result['dominant_emotion'] = max(scores_only, key=scores_only.get)

    return result

