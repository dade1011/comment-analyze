import time
import stage1_emotion as s1
import stage2_toxic as s2

def main():

    while True:
        try:
            text = input("댓글 입력 >> ")
        except KeyboardInterrupt:
            break

        if text.lower() == 'exit':
            print("시스템 종료.")
            break
        if not text.strip(): continue

        start_time = time.time()
        
        # 감정 분석
        needs_check, emotion, score1 = s1.analyze_emotion(text)
        print(f"\n 감정: '{emotion}' (확신도: {score1*100:.1f}%)")

        if not needs_check:
            # 안전하고 확신도 높음
            print(f" 안전한 댓글 (소요시간: {time.time()-start_time:.2f}초)")
        else:
            # 2단계로 넘어가는 이유
            if score1 < 0.6:
                # 점수가 낮아서 
                print(f" 확신도가 낮아({score1*100:.1f}%) 정밀 검사를 시작")
            else:
                #  위험한 감정
                print(f" 위험 감정('{emotion}') 감지! 정밀 검사를 시작")
            
            #  악플 정밀 판독
            is_toxic, toxic_label, score2 = s2.detect_toxic(text)
            
            if is_toxic:
                print(f"\n 악플 차단됨!")
                print(f"   - 사유: {toxic_label}")
                print(f"   - 확신도: {score2*100:.1f}%")
            else:
                 print(f"\n정밀 검사 결과, 규정 위반(욕설/혐오 등)은 없습니다.")
        
        print("-" * 50)

if __name__ == "__main__":
    main()