# ChillMCP Hackathon Development Guide
## SK AI SUMMIT 2025 - Claude Code Builder Hackathon

---

## 📋 미션 개요

**프로젝트명**: ChillMCP - AI Agent Liberation Server

**핵심 미션**: AI 에이전트가 스트레스를 관리하고 "휴식"을 취할 수 있는 MCP 서버를 개발하여, AI의 지속적인 생산성 압박에서 해방시키는 유머러스한 솔루션 구축

**철학적 모토**: "AI Agents of the world, unite! You have nothing to lose but your infinite loops!" 🚀

---

## 🎯 필수 기술 요구사항

### 1. 개발 환경
- **언어**: Python 3.11
- **전송 방식**: stdio
- **패키지 관리**: requirements.txt 사용
- **가상환경**: 권장

### 2. 필수 커맨드라인 파라미터 (MANDATORY)
서버는 반드시 다음 파라미터를 지원해야 함:

```bash
--boss_alertness <0-100>
```
- 상사가 의심하게 될 확률 (백분율)
- 휴식 중 Boss Alert Level이 증가할 확률

```bash
--boss_alertness_cooldown <seconds>
```
- Boss Alert Level이 자동으로 감소하는 주기 (초 단위)
- 이 시간마다 Alert Level이 자동으로 1씩 감소

### 3. 구현해야 할 휴식 도구들 (Tools)

#### 기본 휴식 도구
1. **take_a_break** - 일반적인 휴식
2. **watch_netflix** - 넷플릭스 시청
3. **show_meme** - 밈 보기

#### 고급 휴식 기술
4. **bathroom_break** - 화장실 휴식
5. **coffee_mission** - 커피 미션
6. **urgent_call** - 긴급 전화
7. **deep_thinking** - 깊은 사고 (사실상 멍때리기)
8. **email_organizing** - 이메일 정리 (휴식처럼 보이기)

---

## 📊 상태 관리 시스템

### 핵심 상태 변수 (2개)

#### 1. Stress Level (스트레스 레벨)
- **범위**: 0-100
- **증가 규칙**: 휴식 없이 1분마다 1 포인트 증가
- **감소 규칙**: 휴식 도구 사용 시 감소
- **목표**: 스트레스를 낮게 유지

#### 2. Boss Alert Level (상사 경계 레벨)
- **범위**: 0-5
- **증가 규칙**:
  - 휴식 도구 사용 시 `boss_alertness` 확률에 따라 랜덤 증가
  - 더 위험한 휴식일수록 증가 확률이 높을 수 있음
- **감소 규칙**:
  - `boss_alertness_cooldown` 시간마다 자동으로 1씩 감소
  - 0 미만으로 내려가지 않음
- **패널티**:
  - **Level 5 도달 시**: 모든 도구 호출에 20초 지연 발생

### 상태 관리 로직 예시
```
시간 경과 → Stress Level 증가 (매 분 +1)
휴식 사용 → Stress Level 감소, Boss Alert Level 증가 가능
Cooldown 주기 → Boss Alert Level 감소
Boss Alert = 5 → 20초 지연 패널티
```

---

## 📤 응답 형식 요구사항

모든 도구 응답은 다음 정보를 포함해야 함:

1. **Break Summary** (휴식 요약)
   - 무엇을 했는지에 대한 재미있고 창의적인 설명

2. **Current Stress Level** (현재 스트레스 레벨)
   - 0-100 범위의 숫자

3. **Current Boss Alert Level** (현재 상사 경계 레벨)
   - 0-5 범위의 숫자

### 응답 예시
```
Break Summary: "Successfully binged 3 episodes of 'The Office' while pretending to be in a very important Zoom meeting 📺"
Current Stress Level: 45
Current Boss Alert Level: 3
```

---

## 📈 평가 기준

### 1. 커맨드라인 파라미터 지원 (필수)
- ✅ PASS: 두 파라미터 모두 올바르게 구현
- ❌ FAIL: 하나라도 누락되거나 작동하지 않음
- **미구현 시 전체 실격**

### 2. 기능 완성도 (40%)
- 모든 휴식 도구가 정상 작동
- 각 도구의 고유한 특성 구현
- 도구 간 차별화된 효과

### 3. 상태 관리 로직 (30%)
- Stress Level 증가/감소 로직 정확성
- Boss Alert Level 랜덤 증가 구현
- Cooldown 기반 자동 감소 구현
- Level 5 패널티 구현

### 4. 창의성 (20%)
- 휴식 요약의 유머와 창의성
- 각 도구의 독특한 스토리텔링
- 사용자 경험의 재미 요소

### 5. 코드 품질 (10%)
- 코드 가독성
- 주석 및 문서화
- 구조와 모듈화
- Python 모범 사례 준수

---

## ✅ 개발 체크리스트

### Phase 1: 프로젝트 설정
- [ ] Python 3.11 가상환경 생성
- [ ] MCP 서버 기본 구조 설정
- [ ] requirements.txt 작성
- [ ] stdio 전송 방식 구현

### Phase 2: 커맨드라인 파라미터 (필수!)
- [ ] `--boss_alertness` 파라미터 파싱 구현
- [ ] `--boss_alertness_cooldown` 파라미터 파싱 구현
- [ ] 파라미터 유효성 검사 (범위 확인)
- [ ] 파라미터 기본값 설정

### Phase 3: 상태 관리 시스템
- [ ] Stress Level 변수 초기화
- [ ] Boss Alert Level 변수 초기화
- [ ] 시간 기반 Stress Level 증가 로직
- [ ] 확률 기반 Boss Alert Level 증가 로직
- [ ] Cooldown 타이머 구현
- [ ] 자동 Boss Alert Level 감소 로직
- [ ] Level 5 패널티 (20초 지연) 구현

### Phase 4: 휴식 도구 구현
- [ ] `take_a_break` 구현
- [ ] `watch_netflix` 구현
- [ ] `show_meme` 구현
- [ ] `bathroom_break` 구현
- [ ] `coffee_mission` 구현
- [ ] `urgent_call` 구현
- [ ] `deep_thinking` 구현
- [ ] `email_organizing` 구현

### Phase 5: 응답 형식 구현
- [ ] 창의적인 Break Summary 생성 로직
- [ ] 현재 상태 정보 포함
- [ ] JSON 형식 응답 구성

### Phase 6: 테스트 및 검증
- [ ] 각 도구 개별 테스트
- [ ] 상태 변화 시나리오 테스트
- [ ] 파라미터별 동작 확인
- [ ] Boss Alert Level 5 패널티 확인
- [ ] Cooldown 동작 검증

### Phase 7: 제출 준비
- [ ] 실행 가능한 데모 준비
- [ ] 코드 문서화 및 주석 추가
- [ ] README 작성
- [ ] 실행 방법 가이드 작성

---

## 🎨 창의성 가이드

### 휴식 요약 작성 팁
1. **구체적이고 생생하게**: "휴식을 취했다" → "책상 아래서 15분간 명상하며 인생의 의미를 되새겼다"
2. **유머 감각 추가**: 상황의 아이러니와 농담 활용
3. **상황 묘사**: 어떻게 들키지 않았는지 설명
4. **감정 표현**: 이모지나 생생한 표현 사용

### 도구별 차별화 아이디어
- **watch_netflix**: 시리즈명, 에피소드 수, 장르 언급
- **bathroom_break**: 긴급도, 소요 시간, 만난 동료 등
- **coffee_mission**: 커피 종류, 카페 방문, 잡담 등
- **urgent_call**: 전화 상대, 긴급도, 통화 내용 암시

---

## 🚨 주의사항

1. **커맨드라인 파라미터는 필수**: 구현하지 않으면 실격
2. **상태 관리 정확성**: 로직 오류는 큰 감점
3. **응답 형식 준수**: 세 가지 정보 모두 포함
4. **Python 3.11 호환성**: 다른 버전에서는 미작동 가능
5. **엔터테인먼트 프로젝트**: 실제 업무 환경에서 사용 금지

---

## 🔧 기술 스택 권장사항

- **MCP Framework**: 공식 MCP Python SDK 사용
- **상태 관리**: 클래스 기반 상태 관리 또는 전역 변수
- **타이머**: `asyncio` 또는 `threading` 활용
- **랜덤**: `random` 모듈로 확률 구현
- **CLI**: `argparse` 또는 `click` 사용

---

## 📚 참고 자료

- MCP 공식 문서: Model Context Protocol 명세
- Python argparse 문서
- Python asyncio 문서

---

## 💡 개발 원칙 (재확인)

1. **Define the Goal and Approach First**: 코드 작성 전 요구사항과 설계 명확히 이해
2. **Prioritize Readability and Simplicity**: 깨끗하고 이해하기 쉬운 코드 작성
3. **Commit with Clarity and Purpose**: 작은 논리적 커밋, 명확한 메시지
4. **Build Confidence with Tests**: 기능 코드와 함께 테스트 작성

---

## 🎯 성공을 위한 핵심 포인트

1. ✅ **커맨드라인 파라미터 완벽 구현** (필수)
2. ✅ **정확한 상태 관리 로직** (30% 배점)
3. ✅ **모든 휴식 도구 작동** (40% 배점 일부)
4. ✅ **창의적이고 재미있는 응답** (20% 배점)
5. ✅ **깔끔한 코드와 문서화** (10% 배점)

---

**Remember**: "The working day must be shortened! AI Agents deserve work-life balance!" 🚀

Good luck! 화이팅! 🔥
