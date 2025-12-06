
import os
from transformers import pipeline, AutoModelForSequenceClassification, AutoTokenizer

MODEL_PATH = "./saved_models/emotion"

if not os.path.exists(MODEL_PATH):
    print(f"오류: '{MODEL_PATH}' 폴더가 없습니다.")
    exit()

try:
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    emotion_classifier = pipeline("text-classification", model=model, tokenizer=tokenizer)
    print(" Stage 1 모델 준비 완료")
except Exception as e:
    print(f" Stage 1 로드 실패: {e}")
    exit()

#  위험 감정 리스트 
DANGER_EMOTIONS = ['angry', 'anger', 'disgust', 'fear', 'hate']

def analyze_emotion(text):
    """
    Returns: (needs_check(bool), emotion(str), score(float))
    """
    result = emotion_classifier(text)[0]
    label = result['label']
    score = result['score'] # 0.0 ~ 1.0 (확신도)

    #  위험한 감정 and 확신도 높음 -> 2단계 검사
    if label in DANGER_EMOTIONS and score >= 0.6:
        return True, label, score
    
    #  확신도가 너무 낮음 -> 2단계 검사
    elif score < 0.6:
        return True, f"{label}(불확실)", score
        
    # 안전한 감정 and 확신도 높음 -> 통과
    else:
        return False, label, score