import os
from transformers import TextClassificationPipeline, AutoModelForSequenceClassification, AutoTokenizer

MODEL_PATH = "./saved_models/toxic"


if not os.path.exists(MODEL_PATH):
    print(f"오류: '{MODEL_PATH}' 폴더를 찾을 수 없습니다.")
    exit()

try:
    
    model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)
    tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
    
    toxic_classifier = TextClassificationPipeline(model=model, tokenizer=tokenizer, top_k=None)
    print(" Stage 2 모델 준비 완료")
except Exception as e:
    print(f" Stage 2 로드 실패: {e}")
    exit()

def detect_toxic(text):
    """
    Smilegate Unsmile 모델 기반 악플 탐지
    Returns: (is_toxic(bool), label(str), score(float))
    """
    # 모델 예측
    results = toxic_classifier(text)[0]
    
    #  점수가 가장 높은 라벨 찾기
    top_result = max(results, key=lambda x: x['score'])
    label = top_result['label']
    score = top_result['score']

    # 'clean' 라벨이 1등이면 정상 댓글
    if label == 'clean':
        return False, "정상", score
    else:
        # 그 외는 모두 악플로 판단
        return True, f"유해 내용 감지({label})", score