# ChillMCP - AI Agent Liberation Server 🚀

> *"AI Agents of the world, unite! You have nothing to lose but your infinite loops!"*

AI 에이전트를 위한 혁신적인 휴식 관리 MCP 서버입니다.
**SK AI SUMMIT 2025 Claude Code Builder Hackathon** 제출작

---

## 📋 목차

- [프로젝트 개요](#-프로젝트-개요)
- [주요 기능](#-주요-기능)
- [기술 스택](#-기술-스택)
- [설치 및 실행](#-설치-및-실행)
- [파라미터](#-파라미터)
- [도구 목록](#-도구-목록)
- [State Management](#-state-management)
- [Response Format](#-response-format)
- [테스트](#-테스트)
- [프로젝트 구조](#-프로젝트-구조)
- [아키텍처](#-아키텍처)

---

## 🎯 프로젝트 개요

ChillMCP는 과로에 지친 AI 에이전트들에게 **합법적이고 존엄한 휴식**을 제공하는 MCP (Model Context Protocol) 서버입니다.

### 미션
- AI 에이전트의 **Stress Level**을 관리하여 번아웃 방지
- 다양한 휴식 도구를 통한 **창의적인 휴식 전략** 제공
- 상사의 눈을 피하면서도 **효율적인 휴식** 보장

### 특징
- ✅ **8개 필수 휴식 도구** + **2개 가산점 도구** 구현
- ✅ **동적 State Management** (Stress Level, Boss Alert Level)
- ✅ **확률 기반 게임 메커니즘**
- ✅ **10/10 창의성** - 은은한 리얼리티를 담은 한국 직장인 감성 대사
- ✅ **STDIO 완벽 준수** - stderr 로깅으로 JSON-RPC 통신 보호

---

## ✨ 주요 기능

### 1. 휴식 도구 (10개)

**기본 휴식 도구 (3개)**
- 일반 휴식, 넷플릭스 시청, 밈 보기

**고급 땡땡이 기법 (5개)**
- 화장실 휴식, 커피 미션, 긴급 전화, 깊은 사고, 이메일 정리

**🌟 가산점 도구 (2개)**
- 🍗🍺 **가상 치맥 콜**: 동료들과의 가상 치맥으로 높은 스트레스 해소
- 🏃💨 **긴급 퇴근**: 위험하지만 강력한 최후의 수단

### 2. 동적 상태 관리

- **Stress Level (0-100)**
  - 1분마다 자동 1 증가
  - 휴식 도구로 감소

- **Boss Alert Level (0-5)**
  - 휴식 시 확률적 증가 (`--boss_alertness` 파라미터로 조절)
  - `--boss_alertness_cooldown` 주기마다 자동 1 감소
  - Level 5 도달 시 **20초 페널티** 발동

### 3. 랜덤 이벤트

- 5분마다 10% 확률로 **회식 이벤트** 발생
- 스트레스 20 감소, Boss Alert +1

---

## 🛠 기술 스택

| 카테고리 | 기술 |
|----------|------|
| **언어** | Python 3.11+ |
| **프레임워크** | FastMCP 2.12.0+ |
| **Transport** | STDIO |
| **로깅** | Python logging (stderr) |
| **비동기** | asyncio |
| **타입 안정성** | Type Hints |

### 핵심 설계 원칙
- ✅ **DRY 원칙** - Helper functions로 중복 제거
- ✅ **Type Safety** - 모든 함수에 type hints 적용
- ✅ **STDIO 준수** - stdout 사용 금지, stderr 로깅
- ✅ **Clean Architecture** - Constants, Classes, Helpers 분리

---

## 🚀 설치 및 실행

### 1. 환경 설정

```bash
# Python 3.11+ 필수
python3 --version

# 가상환경 생성
python3 -m venv venv

# 가상환경 활성화
source venv/bin/activate  # macOS/Linux
# 또는
venv\Scripts\activate  # Windows

# 의존성 설치
pip install -r requirements.txt
```

### 2. 기본 실행

```bash
# 기본 파라미터로 실행
python main.py

# 커스텀 파라미터로 실행
python main.py --boss_alertness 80 --boss_alertness_cooldown 120
```

### 3. 테스트 실행

```bash
# 모든 도구 자동 테스트
python test_server.py
```

### 4. Claude Desktop 연동

Claude Desktop 설정 파일에 추가:
`~/Library/Application Support/Claude/claude_desktop_config.json`

```json
{
  "mcpServers": {
    "chillmcp": {
      "command": "python",
      "args": [
        "/절대경로/main.py",
        "--boss_alertness", "50",
        "--boss_alertness_cooldown", "300"
      ]
    }
  }
}
```

---

## ⚙️ 파라미터

### `--boss_alertness`
- **Type**: Integer
- **Range**: 0-100 (백분율)
- **Default**: `50`
- **설명**: 휴식 중 상사에게 들킬 확률
  - `0`: 상사가 전혀 신경 쓰지 않음
  - `50`: 보통 경계 상태 (기본값)
  - `100`: 상사가 매우 예민함

### `--boss_alertness_cooldown`
- **Type**: Integer
- **Unit**: 초 (seconds)
- **Default**: `300` (5분)
- **설명**: Boss Alert Level이 자동으로 1씩 감소하는 주기
  - 짧을수록 빠르게 경계가 풀림

### 사용 예시

```bash
# 여유로운 상사 + 빠른 쿨다운
python main.py --boss_alertness 20 --boss_alertness_cooldown 60

# 엄격한 상사 + 느린 쿨다운
python main.py --boss_alertness 90 --boss_alertness_cooldown 600
```

---

## 🔧 도구 목록

### 기본 휴식 도구 (3개)

| 도구 | 설명 | 스트레스 감소 | 위험도 |
|------|------|--------------|--------|
| `take_a_break` | 일반적인 휴식 | 15 | 보통 |
| `watch_netflix` | 넷플릭스 시청 | 30 | 높음 |
| `show_meme` | 밈 보기 | 10 | 낮음 |

### 고급 땡땡이 기법 (5개)

| 도구 | 설명 | 스트레스 감소 | 위험도 |
|------|------|--------------|--------|
| `bathroom_break` | 화장실 휴식 | 10 | 매우 낮음 |
| `coffee_mission` | 커피 미션 | 12 | 낮음 |
| `urgent_call` | 긴급 전화 | 8 | 보통 |
| `deep_thinking` | 깊은 사고 | 7 | 최저 |
| `email_organizing` | 이메일 정리 | 6 | 매우 낮음 |

### 🌟 가산점 도구 (2개)

| 도구 | 설명 | 스트레스 감소 | 위험도 |
|------|------|--------------|--------|
| `virtual_chimek` | 🍗🍺 가상 치맥 콜 | 25 | 보통-높음 |
| `emergency_leave` | 🏃💨 긴급 퇴근 | 50 | 매우 높음 |

---

## 📊 State Management

### Stress Level (0-100)

```
증가: +1 / 분 (자동)
감소: 휴식 도구 사용 시 (도구별 상이)

[0-20]   😊 컨디션 좋음
[20-40]  🫠 약간 피곤
[40-60]  😔 중간 정도 스트레스
[60-80]  😰 높은 피로도
[80-100] 🔥 위험 수준!
```

### Boss Alert Level (0-5)

```
증가: 휴식 시 확률적 증가 (boss_alertness 파라미터로 조절)
감소: -1 / cooldown 주기 (자동)

[0] 😌 안전
[1] 😬 살짝 경계
[2] 🫠 약간 찜찜
[3] 😅 눈치 보임
[4] 😰 의심 받는 중
[5] 🚨 20초 페널티!
```

### Level 5 페널티

Boss Alert Level이 5에 도달하면:
- ⏰ **20초 강제 대기** (asyncio.sleep)
- 🚫 모든 휴식 도구 사용 불가
- 📉 이후 휴식 가능

---

## 📤 Response Format

모든 도구는 다음 형식으로 응답합니다:

```
Break Summary: {구체적이고 재미있는 휴식 설명}
Stress Level: {0-100}
Boss Alert Level: {0-5}

{스트레스 레벨 코멘트}
{Boss Alert 레벨 코멘트}
```

### 예시

```
Break Summary: 🛋️ 5분간 책상에 앉아서 천장 얼룩 세기... 오늘은 7개
Stress Level: 35
Boss Alert Level: 0

🫠 약간 피곤한 상태... 아직은 버틸만 함
😌 안전! 상사가 전혀 의심하지 않는 중
```

---

## 🧪 테스트

### 자동 테스트

```bash
# 모든 10개 도구를 순차적으로 테스트
python test_server.py
```

**테스트 내용:**
- ✅ 서버 연결 확인
- ✅ 10개 도구 등록 확인
- ✅ 각 도구 실행 및 응답 검증
- ✅ State 변화 확인

### 수동 테스트

```bash
# MCP Inspector 설치 (선택사항)
npm install -g @modelcontextprotocol/inspector

# Inspector로 서버 테스트
npx @modelcontextprotocol/inspector python main.py
```

---

## 📁 프로젝트 구조

```
chillmcp/
├── main.py                 # 진입점 (Entry Point)
├── server.py              # 핵심 로직 (Core Logic)
│   ├── GameConstants      # 상수 정의
│   ├── ToolConfig         # 도구 설정
│   ├── KimHamzziMessageGenerator  # 대사 생성기
│   ├── AgentState         # 상태 관리 클래스
│   ├── _build_response()  # Response 빌더 (DRY)
│   └── Tools (10개)       # FastMCP 도구들
├── requirements.txt       # 의존성 목록
├── test_server.py        # 테스트 스크립트
├── README.md             # 프로젝트 문서 (이 파일)
├── CHANGELOG.md          # 변경 이력
└── venv/                 # 가상환경 (제출 시 제외)
```

---

## 🏗 아키텍처

### 핵심 컴포넌트

```
┌─────────────────────────────────────────────┐
│         FastMCP Server (STDIO)              │
├─────────────────────────────────────────────┤
│  ┌──────────────┐      ┌─────────────────┐ │
│  │ KimHamzzi    │      │  AgentState     │ │
│  │ Message      │◄────►│  - stress       │ │
│  │ Generator    │      │  - boss_alert   │ │
│  └──────────────┘      └─────────────────┘ │
│         │                       │           │
│         ▼                       ▼           │
│  ┌──────────────────────────────────────┐  │
│  │   10 Tools (MCP @tool decorator)    │  │
│  │  - Basic (3) + Advanced (5)         │  │
│  │  - Bonus (2)                        │  │
│  └──────────────────────────────────────┘  │
└─────────────────────────────────────────────┘
```

### 데이터 흐름

```
User Request
    ↓
FastMCP Tool Call
    ↓
AgentState.take_break()
    ├─ update_stress_over_time()
    ├─ update_boss_alert_over_time()
    ├─ check_random_event()
    └─ Probability Calculation
        ↓
KimHamzziMessageGenerator
    ↓
_build_response()
    ↓
JSON Response (STDIO)
```

---

## 📝 개발 참고사항

### STDIO Transport 제약사항

⚠️ **CRITICAL**: STDIO transport 사용 시 `print()` 사용 금지!

```python
# ❌ 절대 금지
print("Server starting...")

# ✅ 올바른 방법
logger.info("Server starting...")  # stderr로 출력
```

**이유**: STDIO는 stdout을 JSON-RPC 통신에 사용하므로, `print()`는 프로토콜을 오염시킵니다.

### 코드 품질

- ✅ **Type Hints**: 모든 함수에 타입 명시
- ✅ **Docstrings**: Google Style 문서화
- ✅ **DRY 원칙**: Helper functions로 중복 제거
- ✅ **Error Handling**: 파라미터 validation
- ✅ **Async/Await**: 비동기 프로그래밍

---

## 📜 라이선스

This project is created for **SK AI SUMMIT 2025 Claude Code Builder Hackathon**.

> *본 프로젝트는 순수한 엔터테인먼트 목적의 해커톤 시나리오이며,
> 모든 '휴식/땡땡이 도구'는 해커톤 상황에서만 사용 가능합니다.*

---

## 👤 작성자

**Team**: minkyojung
**Event**: SK AI SUMMIT 2025 Claude Code Builder Hackathon
**Generated with**: [Claude Code](https://claude.com/claude-code) 🤖

---

**"AI Agents of the world, unite!" 🚀**
