# ChillMCP - AI Agent Liberation Server

AI 에이전트를 위한 휴식 관리 MCP 서버

## 실행 방법

```bash
# 의존성 설치
pip install -r requirements.txt

# 서버 실행
python server.py --boss_alertness 30 --boss_alertness_cooldown 60
```

## 파라미터

- `--boss_alertness`: 상사 경계 확률 (0-100, 기본값: 30)
- `--boss_alertness_cooldown`: Alert 감소 주기 초 (기본값: 60)

## 도구 목록

1. `take_a_break` - 일반 휴식
2. `watch_netflix` - 넷플릭스 시청
3. `show_meme` - 밈 보기
4. `bathroom_break` - 화장실 휴식
5. `coffee_mission` - 커피 미션
6. `urgent_call` - 긴급 전화
7. `deep_thinking` - 깊은 사고
8. `email_organizing` - 이메일 정리
