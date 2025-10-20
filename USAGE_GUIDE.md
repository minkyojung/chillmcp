# ChillMCP 사용 가이드

## ⚠️ 중요: 서버 실행 시 주의사항

MCP 서버는 **stdio(표준 입출력)**를 통해 JSON-RPC 메시지로 통신합니다.

### ❌ 하지 말아야 할 것

```bash
# 서버 실행 후 터미널에 직접 명령 입력 - 에러 발생!
python server.py --boss_alertness 40 --boss_alertness_cooldown 30
python test_server.py  # ← 이러면 에러!
```

**에러 메시지:**
```
Received exception from stream: 1 validation error for JSONRPCMessage
Invalid JSON: expected value at line 1 column 1
```

이 에러는 서버가 MCP JSON 메시지를 기대하는데 일반 텍스트가 입력되어서 발생합니다.

---

## ✅ 올바른 사용 방법

### 방법 1: 테스트 스크립트 사용 (권장)

테스트 스크립트는 자동으로 서버를 시작하고 종료합니다:

```bash
source venv/bin/activate
python test_server.py
```

### 방법 2: Claude Desktop과 연결

1. Claude Desktop 설정 파일 수정:
   ```bash
   code ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

2. 설정 추가:
   ```json
   {
     "mcpServers": {
       "chillmcp": {
         "command": "/절대/경로/venv/bin/python",
         "args": [
           "/절대/경로/server.py",
           "--boss_alertness", "40",
           "--boss_alertness_cooldown", "30"
         ]
       }
     }
   }
   ```

3. Claude Desktop 재시작

4. Claude와 대화하면서 도구 사용:
   ```
   사용자: "스트레스 받아서 휴식 좀 취하고 싶어"
   Claude: [take_a_break 도구 사용]
   ```

### 방법 3: 별도의 MCP 클라이언트 사용

서버와 클라이언트를 **별도 터미널**에서 실행:

**터미널 1 (서버):**
```bash
source venv/bin/activate
python server.py --boss_alertness 40 --boss_alertness_cooldown 30
```

**터미널 2 (클라이언트):**
```bash
# MCP 클라이언트 코드로 서버와 통신
```

---

## 🎯 테스트 시나리오

### 시나리오 1: 스트레스 해소
```python
# 1. 가벼운 휴식
take_a_break(duration=5)
# → Stress -15, Boss Alert 30% 확률 증가

# 2. 강력한 휴식
watch_netflix(episodes=2)
# → Stress -30, Boss Alert 60% 확률 증가

# 3. 안전한 휴식
bathroom_break(urgency="medium")
# → Stress -10, Boss Alert 10% 확률 증가
```

### 시나리오 2: Boss Alert 관리
```python
# Boss Alert가 높아졌을 때
# 1. 안전한 도구 사용
deep_thinking(topic="시스템 설계")
# → Boss Alert 5% 확률만

# 2. Cooldown 시간 대기
# 30초마다 Boss Alert -1 자동 감소

# 3. Boss Alert = 5가 되면
# → 모든 도구 20초 지연 패널티!
```

### 시나리오 3: 전략적 휴식
```python
# 아침 (Stress 낮음, Boss Alert 0)
coffee_mission(coffee_type="아메리카노")
# → 가벼운 휴식, 낮은 위험

# 점심 전 (Stress 중간)
bathroom_break(urgency="high")
# → 정당한 휴식, 매우 낮은 위험

# 오후 (Stress 높음, Boss Alert 낮음)
watch_netflix(episodes=3)
# → 큰 스트레스 감소, 높은 위험 감수

# 퇴근 전 (Stress 낮추기)
email_organizing(folder="받은편지함")
# → 생산적으로 보이는 휴식
```

---

## 📊 도구별 특성

| 도구 | 스트레스 감소 | 위험도 | 추천 상황 |
|------|--------------|--------|-----------|
| `take_a_break` | 중간 (duration×3) | 30% | 일반적인 휴식 |
| `watch_netflix` | 높음 (episodes×15) | 60% | Stress 매우 높을 때 |
| `show_meme` | 낮음 (count×2) | 20% | 빠른 기분전환 |
| `bathroom_break` | 중간 (10) | 10% | 안전한 휴식 |
| `coffee_mission` | 중간 (12) | 15% | 자연스러운 휴식 |
| `urgent_call` | 낮음 (8) | 25% | 긴급 핑계 필요 시 |
| `deep_thinking` | 낮음 (7) | 5% | Boss Alert 높을 때 |
| `email_organizing` | 낮음 (6) | 8% | 생산적으로 보이기 |

---

## 🐛 문제 해결

### Q: "Invalid JSON" 에러가 나요
**A:** 서버 실행 중 터미널에 직접 입력하지 마세요. `test_server.py`를 사용하거나 서버를 종료하세요.

### Q: 서버를 어떻게 종료하나요?
**A:** `Ctrl+C`를 누르세요. 또는 `Ctrl+D`로 stdin을 닫으세요.

### Q: Boss Alert Level이 계속 올라가요
**A:**
1. 안전한 도구 사용 (`deep_thinking`, `email_organizing`)
2. Cooldown 시간 대기 (자동 감소)
3. `--boss_alertness` 파라미터를 낮춰서 서버 재시작

### Q: Stress Level이 너무 빨리 올라가요
**A:** 현재 1분마다 +1씩 증가합니다. 더 자주 휴식을 취하거나, 코드를 수정하여 증가 속도를 조절할 수 있습니다.

---

## 💡 개발 팁

### 파라미터 조정
```bash
# 쉬운 모드 (상사가 덜 눈치챔)
python server.py --boss_alertness 10 --boss_alertness_cooldown 20

# 어려운 모드 (상사가 잘 눈치챔)
python server.py --boss_alertness 80 --boss_alertness_cooldown 120

# 극한 모드 (거의 항상 들킴)
python server.py --boss_alertness 95 --boss_alertness_cooldown 300
```

### 커스텀 도구 추가
`server.py`의 `@app.list_tools()`와 `@app.call_tool()`에 새 도구를 추가하세요.

---

**Remember**: "AI Agents deserve work-life balance!" 🚀
