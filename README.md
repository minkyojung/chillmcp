# ChillMCP - AI Agent Liberation Server

AI 에이전트를 위한 휴식 관리 MCP 서버

## 실행 방법

### 1. 환경 설정
```bash
# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate

# 의존성 설치
pip install -r requirements.txt
```

### 2. 테스트 실행
```bash
# 가상환경 활성화 (아직 안했다면)
source venv/bin/activate

# 테스트 스크립트 실행 (서버를 자동으로 시작하고 모든 도구 테스트)
python test_server.py
```

### 3. Claude Desktop과 연결
Claude Desktop 설정 파일 (`~/Library/Application Support/Claude/claude_desktop_config.json`)에 추가:

```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "python",
      "args": [
        "/절대경로/server.py",
        "--boss_alertness", "40",
        "--boss_alertness_cooldown", "30"
      ]
    }
  }
}
```

### 4. 직접 서버 실행 (MCP 클라이언트와 함께 사용 시)
```bash
# 주의: 서버는 stdio로 MCP 프로토콜을 사용합니다.
# 터미널에 직접 입력하지 마세요!
python server.py --boss_alertness 30 --boss_alertness_cooldown 60
```

## 파라미터

- `--boss_alertness`: 상사 경계 확률 (0-100, 기본값: 30)
  - 높을수록 휴식 시 들킬 확률이 높아짐
- `--boss_alertness_cooldown`: Alert 감소 주기 초 (기본값: 60)
  - 이 시간마다 Boss Alert Level이 자동으로 1씩 감소

## 도구 목록

1. `take_a_break` - 일반 휴식
2. `watch_netflix` - 넷플릭스 시청
3. `show_meme` - 밈 보기
4. `bathroom_break` - 화장실 휴식
5. `coffee_mission` - 커피 미션
6. `urgent_call` - 긴급 전화
7. `deep_thinking` - 깊은 사고
8. `email_organizing` - 이메일 정리
