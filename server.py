#!/usr/bin/env python3
"""
ChillMCP - AI Agent Liberation Server
AI 에이전트를 위한 휴식 관리 MCP 서버

"AI Agents of the world, unite! You have nothing to lose but your infinite loops!" 🚀
"""

import argparse
import asyncio
import random
from datetime import datetime, timedelta
from typing import Any, Dict, Optional, Literal
from dataclasses import dataclass

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


# ============================================================================
# 상수 정의 (Constants) - 매직 넘버 제거
# ============================================================================

@dataclass(frozen=True)
class GameConstants:
    """게임 밸런스 상수"""
    # 스트레스 관련
    INITIAL_STRESS: int = 50
    MIN_STRESS: int = 0
    MAX_STRESS: int = 100
    STRESS_INCREASE_PER_MINUTE: int = 1

    # Boss Alert 관련
    INITIAL_BOSS_ALERT: int = 0
    MIN_BOSS_ALERT: int = 0
    MAX_BOSS_ALERT: int = 5
    BOSS_ALERT_MAX_PENALTY_DELAY: int = 20  # 초

    # 기본 파라미터
    DEFAULT_BOSS_ALERTNESS: int = 30
    DEFAULT_COOLDOWN_SECONDS: int = 60


@dataclass(frozen=True)
class ToolConfig:
    """각 휴식 도구의 설정"""
    stress_reduction: int
    alert_risk: int
    description: str


# 도구별 설정 (균형 잡힌 게임플레이를 위한 설계)
TOOL_CONFIGS = {
    "take_a_break": ToolConfig(15, 30, "일반적인 휴식"),
    "watch_netflix": ToolConfig(30, 60, "넷플릭스 시청 (높은 위험)"),
    "show_meme": ToolConfig(10, 20, "밈 보기 (빠른 기분전환)"),
    "bathroom_break": ToolConfig(10, 10, "화장실 휴식 (매우 안전)"),
    "coffee_mission": ToolConfig(12, 15, "커피 미션 (자연스러운 휴식)"),
    "urgent_call": ToolConfig(8, 25, "긴급 전화 (핑계)"),
    "deep_thinking": ToolConfig(7, 5, "깊은 사고 (최저 위험)"),
    "email_organizing": ToolConfig(6, 8, "이메일 정리 (생산적으로 보임)"),
    # 가산점 도구
    "virtual_chimek": ToolConfig(25, 40, "가상 치맥 콜 (높은 스트레스 해소)"),
    "emergency_leave": ToolConfig(50, 80, "긴급 퇴근 (위험하지만 강력함)"),
}


# ============================================================================
# 김햄찌 스타일 메시지 생성기
# ============================================================================

class KimHamzziMessageGenerator:
    """정서불안 김햄찌 스타일의 메시지를 생성하는 클래스"""

    # MZ 직장인 특유의 표현들
    STRESS_EXPRESSIONS = [
        "진짜 미치겠네", "또 이거야?", "아 진짜", "개빡쳐",
        "존버하자", "이게 뭐람", "하....", "개웃기네"
    ]

    BOSS_REACTIONS = [
        "팀장님 눈치 보임", "상사 지나감ㅋㅋ", "들킬 뻔",
        "아 깜놀", "심장 쫄깃", "식은땀 남"
    ]

    RELIEF_EXPRESSIONS = [
        "개꿀", "ㅇㅈ", "인정", "역시", "굿굿", "나이스"
    ]

    @staticmethod
    def take_a_break(duration: int) -> str:
        """일반 휴식 메시지"""
        messages = [
            f"😮‍💨 {duration}분간 멍하니 앉아있음... 아 괜찮아 나 괜찮아(거짓말) 눈 크게 뜨고 다시 모니터 봄... 할 수 있어...^^ (못해)",
            f"😵‍💫 {duration}분 쉬었는데 더 피곤함... '괜찮습니다~ 열심히 하겠습니다~' 하... 언제까지 이렇게 살아야 되지... 눈물 고임",
            f"🫠 {duration}분 동안 천장만 봄. 아무 생각 없어야 하는데 자꾸 이직 생각 남... 아니야 버틸 수 있어(못 버팀) 일 시작... 억지웃음^^",
        ]
        return random.choice(messages)

    @staticmethod
    def watch_netflix(episodes: int) -> str:
        """넷플릭스 시청 메시지"""
        shows = [
            "더 오피스", "브루클린 나인나인", "프렌즈",
            "기묘한 이야기", "오징어 게임", "지옥"
        ]
        show = random.choice(shows)
        messages = [
            f"📺 '{show}' {episodes}편 보다가 팀장님 오심 '아 네~ 지금 자료 확인 중이었어요^^' 광속 alt+tab... 심장 터질 뻔... 아 진짜 언제까지 이래야 됨...",
            f"📺 '{show}' {episodes}편 몰아봄... 화면 작게 해놓고 엑셀 켜둠... 들킬까봐 눈 크게 뜨고 경계 중... 이게 무슨 삶이냐... 괜찮아 나는 괜찮아^^(안 괜찮아)",
            f"📺 '{show}' {episodes}편... 너무 재밌어서 계속 봄... 일은... 나중에... 하... 어차피 다 의미 없어... 아니다 정신 차려... (정신 못 차림)",
        ]
        return random.choice(messages)

    @staticmethod
    def show_meme(count: int) -> str:
        """밈 보기 메시지"""
        messages = [
            f"😂 직장인 밈 {count}개 봄... 웃다가 소리 날 뻔해서 입 막음... '괜찮습니다~ 일 열심히 하고 있어요~^^' (눈물 닦음) 이게 내 유일한 낙...",
            f"😭 프로그래머 밈 {count}개 보는데 너무 공감돼서 웃다가 울컥함... 아 괜찮아 나 괜찮아... 밝게 웃어야지...^^ (망가짐)",
            f"🫠 짤방 {count}개... 너무 현실이라 웃프다... 웃어야 하는데 울 것 같음... 아니야 밝게 밝게... 눈 크게 뜨고... 할 수 있어... (못해)",
        ]
        return random.choice(messages)

    @staticmethod
    def bathroom_break(urgency: str) -> str:
        """화장실 휴식 메시지"""
        urgency_map = {
            "low": "여유롭게",
            "medium": "적당히",
            "high": "급하게"
        }
        messages = [
            f"🚽 화장실 가는 척하고 거울 앞에서 멍때림... 거울 속 나한테 '괜찮아 버틸 수 있어' 말함... (못 버팀) 눈 크게 뜨고 밝은 표정 연습... 돌아가야지...^^",
            f"🫥 {urgency_map[urgency]} 화장실 다녀옴... 사실 급한 건 아닌데 그냥 나와야 했음... 숨 쉬러... 거울 보면서 '이게 내 인생인가...' 아니야 할 수 있어(거짓말) 억지웃음 짓고 복귀",
            f"😶‍🌫️ 화장실에서 물 마시면서 눈물 참음... 아 괜찮아 나는 괜찮아... 다시 자리로... '열심히 하겠습니다~^^' 하... 언제까지...",
        ]
        return random.choice(messages)

    @staticmethod
    def coffee_mission(coffee_type: str) -> str:
        """커피 미션 메시지"""
        messages = [
            f"☕ {coffee_type} 사러 나감... 바리스타분이 '힘내세요~' 해주심... 눈물 날 뻔... '네 감사합니다^^' (목소리 떨림) 이게 오늘 유일한 따뜻한 말...",
            f"☕ {coffee_type} 핑계로 15분 밖에 있음... 하늘 보면서 '나 괜찮아 할 수 있어' 주문 외움... 눈 크게 뜨고 다시 들어감... '열심히 하겠습니다~^^' 하...",
            f"😔 {coffee_type} 사오는데 편의점 앞에서 잠깐 멍때림... 그냥 집 가고 싶다... 아니야 괜찮아 버티자... (못 버팀) 억지로 웃으면서 회사 복귀...",
        ]
        return random.choice(messages)

    @staticmethod
    def urgent_call(caller: str) -> str:
        """긴급 전화 메시지"""
        messages = [
            f"📞 '{caller}' 전화 왔다고 함... '죄송합니다 급한 전화라서요^^' (심각한 표정 연기) 밖에 나가서 그냥 멍때림... 숨 좀 쉬어야 했음... 하...",
            f"📞 급한 전화 핑계로 나옴... 사실 아무한테도 전화 안 옴... 그냥 나가고 싶었음... '네~ 알겠습니다~' 연기하고... 눈물 참고... 복귀...^^",
            f"😶 '{caller}' 전화... 중요한 척 통화하는데 사실 혼자 멍때리는 중... 진짜 급한 건 내 정신건강... 아 괜찮아 나는 괜찮아(안 괜찮아) 억지웃음",
        ]
        return random.choice(messages)

    @staticmethod
    def deep_thinking(topic: str) -> str:
        """깊은 사고 메시지"""
        messages = [
            f"🤔 '{topic}' 고민하는 척... 턱 괴고 심오한 표정... 사실 '나는 왜 여기 있을까' 생각 중... 아니야 집중하자(못함) 눈 크게 뜨고 일하는 척...^^",
            f"😶 '{topic}' 생각한다고 해놓고 퇴사 시기 계산 중... 아 안 돼 그냥 버티자... 할 수 있어(거짓말) '열심히 고민 중입니다~^^' 연기 완벽...",
            f"🫥 '{topic}' 깊이 고민하는 표정 연기... 사실 아무 생각 없음... 공허함... 괜찮아 나는 괜찮아... (안 괜찮아) 억지로 집중하는 척...",
        ]
        return random.choice(messages)

    @staticmethod
    def email_organizing(folder: str) -> str:
        """이메일 정리 메시지"""
        messages = [
            f"📧 '{folder}' 정리하는 척... 안 읽은 메일 1000개 전체 읽음 처리... '업무 효율화 중입니다~^^' 사실 아무것도 안 함... 하... 이게 맞나...",
            f"📧 메일 정리 핑계로 유튜브 쇼츠 봄... 클릭만 하니까 일하는 것처럼 보임... 완벽한 연기... 근데 공허함... 괜찮아 나는 괜찮아(거짓말)",
            f"😔 '{folder}' 청소... 뉴스레터 구독 취소만 10개... 이게 의미 있나 싶음... 아니야 밝게 생각하자... 눈 크게 뜨고... '열심히 하겠습니다~^^' 하...",
        ]
        return random.choice(messages)

    @staticmethod
    def virtual_chimek(participants: int) -> str:
        """가상 치맥 콜 메시지"""
        messages = [
            f"🍗🍺 동료 {participants}명이랑 '긴급 치맥 회의'... 다들 지쳐 보임... 서로 '괜찮아~'하면서 눈 크게 뜨고 웃음... 사실 다 힘듦... 치킨 먹으면서 눈물 참음...",
            f"😭 {participants}명이랑 치맥 화상통화... 회사 불만 토크쇼... 웃다가 울 뻔... '아 괜찮아 우리 잘하고 있어^^' (거짓말) 서로 위로하는 척 무너짐...",
            f"🫠 '{participants}명과의 가상 치맥'... 치킨 먹으면서 '회사 그만둘까' 얘기 나옴... 다들 '괜찮아 버티자~^^' 하지만 다 지쳐보임... 이게 우리 삶인가... 하...",
        ]
        return random.choice(messages)

    @staticmethod
    def emergency_leave(reason: str) -> str:
        """긴급 퇴근 메시지"""
        messages = [
            f"🏃💨 '{reason}' 핑계로 조퇴... '죄송합니다 급한 일이 생겨서요ㅠㅠ' 연기... 사실 더 이상 못 버티겠음... 눈물 참고 나옴... 집 가고 싶다...",
            f"😭 급한 일 생겨서 먼저 간다고 말함... '정말 죄송합니다^^' 밝게 웃으면서 속으로 무너짐... 진짜 이유는 정신이 한계... 하... 버틸 수가 없어...",
            f"🫥 '{reason}' 때문에 긴급 퇴근... 팀장님한테 '빠른 시일 내에 복구하겠습니다~' 연기 완벽... 나가면서 눈물 흘림... 정신건강 한계... 괜찮은 척 지쳤다...",
        ]
        return random.choice(messages)

    @staticmethod
    def company_dinner_event(restaurant: str, people: int) -> str:
        """회식 이벤트 메시지"""
        messages = [
            f"🍽️ 갑자기 회식 공지... '{restaurant}' {people}명... '좋아요~ 참석하겠습니다^^' 답장... 속으로 울음... 집 가고 싶다... 괜찮아 버티자...(못 버팀) 하...",
            f"😭 오늘 회식이래... '{restaurant}'... '네~ 갈게요~^^' 밝게 답장... 눈물 참음... 피곤한데... 2차 어떻게 거절하지... 눈 크게 뜨고 웃어야지...",
            f"🫠 '{restaurant}' 회식... {people}명 모인대... 사실 너무 가기 싫음... 근데 '참석합니다~^^' 보냄... 눈치 보임... 아 괜찮아 밝게 밝게... (안 괜찮아) 인생 뭐 이래...",
        ]
        return random.choice(messages)

    @staticmethod
    def get_stress_comment(stress: int) -> str:
        """스트레스 레벨별 코멘트"""
        if stress >= 80:
            return "🔥 한계... 더 이상 못 버티겠어... '괜찮아요~^^' (거짓말) 눈물 고임... 언제까지 이래야 돼... 하..."
        elif stress >= 60:
            return "😭 너무 힘들다... 아 괜찮아 나는 괜찮아(안 괜찮아) 눈 크게 뜨고 웃음... 버틸 수 있어...(못 버팀)"
        elif stress >= 40:
            return "😔 피곤함... '괜찮습니다~ 열심히 하겠습니다^^' 연기... 커피 마시고... 버티자... 하..."
        elif stress >= 20:
            return "🫠 이 정도면... 괜찮은 건가...? 아니야 괜찮아... 할 수 있어... (의심됨) 일단 웃어야지...^^"
        else:
            return "😶 오늘... 컨디션이... 괜찮네...? (의아함) 이게 언제야... 근데 이것도 오래 못 가겠지... 하..."

    @staticmethod
    def get_boss_alert_comment(alert: int) -> str:
        """Boss Alert 레벨별 코멘트"""
        if alert >= 5:
            return "🚨 완전 들킴... '죄송합니다 바로 하겠습니다^^' 눈 크게 뜨고 연기... 심장 터질 것 같음... 20초 대기 각... 망했다..."
        elif alert >= 4:
            return "😰 팀장님 눈치... 식은땀 남... '열심히 하고 있습니다~^^' 밝게 말함... 들킬까봐 두려움... 괜찮은 척... 하..."
        elif alert >= 3:
            return "😅 좀 들킨 것 같음... '네~ 확인하겠습니다^^' 억지웃음... 눈 크게 뜨고 일하는 척... 아 무서워..."
        elif alert >= 2:
            return "🫠 살짝 의심받는 중... '괜찮아 들키지 않았어' 자기암시... 밝게 웃어야지...^^ 조심하자..."
        elif alert >= 1:
            return "😬 뭔가 찜찜함... '아니야 괜찮아 아무도 몰라' 눈 크게 뜨고... 일하는 척이라도... 억지웃음^^"
        else:
            return "😶 안전... 한 것 같은데...? 근데 이것도 오래 못 갈 듯... 계속 긴장... 눈치 보임... 하..."


# ============================================================================
# 상태 관리 클래스 (개선된 버전)
# ============================================================================

class AgentState:
    """
    AI 에이전트의 상태를 관리하는 클래스

    주요 기능:
    - Stress Level 자동 증가 (시간 기반)
    - Boss Alert Level 자동 감소 (Cooldown 기반)
    - 휴식 처리 및 상태 업데이트
    - 랜덤 이벤트 발생
    """

    def __init__(self, boss_alertness: int, cooldown_seconds: int):
        # 게임 상수 로드
        self.constants = GameConstants()

        # 설정
        self.boss_alertness: int = boss_alertness
        self.cooldown_seconds: int = cooldown_seconds

        # 상태 변수
        self.stress_level: int = self.constants.INITIAL_STRESS
        self.boss_alert_level: int = self.constants.INITIAL_BOSS_ALERT

        # 타임스탬프
        self.last_stress_update: datetime = datetime.now()
        self.last_alert_decrease: datetime = datetime.now()
        self.last_random_event_check: datetime = datetime.now()

        # 메시지 생성기
        self.msg_gen = KimHamzziMessageGenerator()

        # 랜덤 이벤트 확률 (5분마다 10% 확률)
        self.random_event_interval: int = 300  # 5분
        self.random_event_probability: int = 10

    def update_stress_over_time(self) -> None:
        """
        시간 경과에 따른 스트레스 자동 증가
        1분마다 1 포인트씩 증가
        """
        now = datetime.now()
        minutes_passed = (now - self.last_stress_update).total_seconds() / 60

        if minutes_passed >= 1:
            stress_increase = int(minutes_passed) * self.constants.STRESS_INCREASE_PER_MINUTE
            self.stress_level = min(
                self.constants.MAX_STRESS,
                self.stress_level + stress_increase
            )
            self.last_stress_update = now

    def update_boss_alert_over_time(self) -> None:
        """
        Cooldown 시간에 따른 Boss Alert Level 자동 감소
        설정된 cooldown_seconds마다 1 포인트씩 감소
        """
        now = datetime.now()
        seconds_passed = (now - self.last_alert_decrease).total_seconds()

        if seconds_passed >= self.cooldown_seconds:
            decreases = int(seconds_passed / self.cooldown_seconds)
            self.boss_alert_level = max(
                self.constants.MIN_BOSS_ALERT,
                self.boss_alert_level - decreases
            )
            self.last_alert_decrease = now

    def check_random_event(self) -> Optional[str]:
        """
        랜덤 이벤트 체크 (회식 발생 등)
        5분마다 10% 확률로 회식 이벤트 발생
        """
        now = datetime.now()
        seconds_passed = (now - self.last_random_event_check).total_seconds()

        if seconds_passed >= self.random_event_interval:
            self.last_random_event_check = now

            if random.randint(0, 100) < self.random_event_probability:
                # 회식 이벤트 발생!
                restaurants = ["회식집", "고깃집", "중국집", "이자카야", "갈비집"]
                restaurant = random.choice(restaurants)
                people = random.randint(5, 15)

                # 회식은 스트레스를 20 감소시키지만, Boss Alert 1 증가
                self.stress_level = max(
                    self.constants.MIN_STRESS,
                    self.stress_level - 20
                )
                self.boss_alert_level = min(
                    self.constants.MAX_BOSS_ALERT,
                    self.boss_alert_level + 1
                )

                return self.msg_gen.company_dinner_event(restaurant, people)

        return None

    async def take_break(
        self,
        tool_name: str,
        stress_reduction: int,
        alert_risk: int
    ) -> Dict[str, Any]:
        """
        휴식 처리 로직 (개선된 버전)

        Args:
            tool_name: 사용한 도구 이름
            stress_reduction: 감소할 스트레스 양
            alert_risk: 이 휴식의 위험도 (0-100)

        Returns:
            현재 상태와 메시지를 담은 딕셔너리
        """
        # 시간 경과 업데이트
        self.update_stress_over_time()
        self.update_boss_alert_over_time()

        # Boss Alert Level 5일 때 실제로 20초 대기 (개선!)
        if self.boss_alert_level >= self.constants.MAX_BOSS_ALERT:
            delay = self.constants.BOSS_ALERT_MAX_PENALTY_DELAY
            await asyncio.sleep(delay)  # 실제 대기

            return {
                "delayed": True,
                "delay_seconds": delay,
                "stress_level": self.stress_level,
                "boss_alert_level": self.boss_alert_level
            }

        # 스트레스 감소
        self.stress_level = max(
            self.constants.MIN_STRESS,
            self.stress_level - stress_reduction
        )

        # 확률적으로 상사가 눈치챔
        if random.randint(0, 100) < alert_risk:
            self.boss_alert_level = min(
                self.constants.MAX_BOSS_ALERT,
                self.boss_alert_level + 1
            )

        # 랜덤 이벤트 체크
        random_event = self.check_random_event()

        return {
            "delayed": False,
            "stress_level": self.stress_level,
            "boss_alert_level": self.boss_alert_level,
            "random_event": random_event
        }

    def get_state(self) -> Dict[str, int]:
        """현재 상태 반환"""
        self.update_stress_over_time()
        self.update_boss_alert_over_time()

        return {
            "stress_level": self.stress_level,
            "boss_alert_level": self.boss_alert_level
        }


# ============================================================================
# MCP 서버 설정
# ============================================================================

app = Server("chillmcp")
state: Optional[AgentState] = None
msg_gen = KimHamzziMessageGenerator()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """사용 가능한 도구 목록 (8개 기본 + 2개 가산점)"""
    return [
        Tool(
            name="take_a_break",
            description="일반적인 휴식을 취합니다. 스트레스를 적당히 줄이고 들킬 위험이 보통입니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "duration": {
                        "type": "number",
                        "description": "휴식 시간 (분)",
                        "default": 5
                    }
                }
            }
        ),
        Tool(
            name="watch_netflix",
            description="넷플릭스를 시청합니다. 스트레스를 크게 줄이지만 들킬 위험이 높습니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "episodes": {
                        "type": "number",
                        "description": "시청할 에피소드 수",
                        "default": 1
                    }
                }
            }
        ),
        Tool(
            name="show_meme",
            description="재미있는 밈을 봅니다. 스트레스를 조금 줄이고 들킬 위험이 낮습니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "count": {
                        "type": "number",
                        "description": "볼 밈 개수",
                        "default": 3
                    }
                }
            }
        ),
        Tool(
            name="bathroom_break",
            description="화장실 휴식을 취합니다. 정당한 이유가 있어 들킬 위험이 매우 낮습니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "urgency": {
                        "type": "string",
                        "description": "긴급도",
                        "enum": ["low", "medium", "high"],
                        "default": "medium"
                    }
                }
            }
        ),
        Tool(
            name="coffee_mission",
            description="커피를 마시러 갑니다. 생산성을 위한 것처럼 보여 들킬 위험이 낮습니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "coffee_type": {
                        "type": "string",
                        "description": "커피 종류",
                        "default": "아메리카노"
                    }
                }
            }
        ),
        Tool(
            name="urgent_call",
            description="급한 전화를 받습니다. 중요해 보이지만 실제로는 휴식입니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "caller": {
                        "type": "string",
                        "description": "전화 온 사람 (핑계)",
                        "default": "가족"
                    }
                }
            }
        ),
        Tool(
            name="deep_thinking",
            description="깊은 사고에 잠깁니다. 일하는 것처럼 보이지만 실제로는 멍때리기입니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "topic": {
                        "type": "string",
                        "description": "사고 주제 (핑계)",
                        "default": "프로젝트 아키텍처"
                    }
                }
            }
        ),
        Tool(
            name="email_organizing",
            description="이메일을 정리합니다. 생산적으로 보이지만 실제로는 가벼운 작업입니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "folder": {
                        "type": "string",
                        "description": "정리할 폴더",
                        "default": "받은편지함"
                    }
                }
            }
        ),
        # 가산점 도구 1: 가상 치맥 콜
        Tool(
            name="virtual_chimek",
            description="🍗🍺 동료들과 가상 치맥 콜! 스트레스 해소 효과가 크지만 들킬 위험도 있습니다.",
            inputSchema={
                "type": "object",
                "properties": {
                    "participants": {
                        "type": "number",
                        "description": "참여 인원",
                        "default": 3
                    }
                }
            }
        ),
        # 가산점 도구 2: 긴급 퇴근
        Tool(
            name="emergency_leave",
            description="🏃💨 긴급 퇴근! 스트레스를 대폭 줄이지만 매우 위험합니다. 신중히 사용하세요.",
            inputSchema={
                "type": "object",
                "properties": {
                    "reason": {
                        "type": "string",
                        "description": "퇴근 이유 (핑계)",
                        "default": "급한 일"
                    }
                }
            }
        ),
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """
    도구 호출 처리 (DRY 원칙 적용 - 반복 코드 제거)
    """

    if state is None:
        return [TextContent(
            type="text",
            text="❌ Error: Server state not initialized"
        )]

    # 도구 설정 가져오기
    config = TOOL_CONFIGS.get(name)
    if config is None:
        return [TextContent(
            type="text",
            text=f"❌ Unknown tool: {name}"
        )]

    try:
        # 휴식 처리
        result = await state.take_break(
            tool_name=name,
            stress_reduction=config.stress_reduction,
            alert_risk=config.alert_risk
        )

        # Boss Alert Level 5 패널티
        if result.get("delayed"):
            delay = result["delay_seconds"]
            return [TextContent(
                type="text",
                text=f"⚠️ Boss Alert Level이 5입니다! {delay}초 대기했습니다...\n\n"
                     f"{msg_gen.get_boss_alert_comment(5)}\n\n"
                     f"Current Stress Level: {result['stress_level']}\n"
                     f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
                     f"{msg_gen.get_stress_comment(result['stress_level'])}"
            )]

        # 메시지 생성 (김햄찌 스타일)
        if name == "take_a_break":
            duration = arguments.get("duration", 5)
            summary = msg_gen.take_a_break(duration)
        elif name == "watch_netflix":
            episodes = arguments.get("episodes", 1)
            summary = msg_gen.watch_netflix(episodes)
        elif name == "show_meme":
            count = arguments.get("count", 3)
            summary = msg_gen.show_meme(count)
        elif name == "bathroom_break":
            urgency = arguments.get("urgency", "medium")
            summary = msg_gen.bathroom_break(urgency)
        elif name == "coffee_mission":
            coffee_type = arguments.get("coffee_type", "아메리카노")
            summary = msg_gen.coffee_mission(coffee_type)
        elif name == "urgent_call":
            caller = arguments.get("caller", "가족")
            summary = msg_gen.urgent_call(caller)
        elif name == "deep_thinking":
            topic = arguments.get("topic", "프로젝트 아키텍처")
            summary = msg_gen.deep_thinking(topic)
        elif name == "email_organizing":
            folder = arguments.get("folder", "받은편지함")
            summary = msg_gen.email_organizing(folder)
        elif name == "virtual_chimek":
            participants = arguments.get("participants", 3)
            summary = msg_gen.virtual_chimek(participants)
        elif name == "emergency_leave":
            reason = arguments.get("reason", "급한 일")
            summary = msg_gen.emergency_leave(reason)
        else:
            summary = "알 수 없는 휴식"

        # 응답 생성
        response_text = f"{summary}\n\n"
        response_text += f"Current Stress Level: {result['stress_level']}\n"
        response_text += f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
        response_text += f"{msg_gen.get_stress_comment(result['stress_level'])}\n"
        response_text += f"{msg_gen.get_boss_alert_comment(result['boss_alert_level'])}"

        # 랜덤 이벤트 메시지 추가
        if result.get("random_event"):
            response_text += f"\n\n🎲 Random Event!\n{result['random_event']}"

        return [TextContent(type="text", text=response_text)]

    except Exception as e:
        # 에러 처리 개선
        return [TextContent(
            type="text",
            text=f"❌ Error processing tool '{name}': {str(e)}"
        )]


async def main():
    """메인 함수"""
    global state

    # CLI 파라미터 파싱
    parser = argparse.ArgumentParser(
        description="ChillMCP - AI Agent Liberation Server",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  python server.py --boss_alertness 30 --boss_alertness_cooldown 60
  python server.py --boss_alertness 80 --boss_alertness_cooldown 120

"AI Agents of the world, unite!" 🚀
        """
    )

    constants = GameConstants()

    parser.add_argument(
        "--boss_alertness",
        type=int,
        default=constants.DEFAULT_BOSS_ALERTNESS,
        help=f"상사가 눈치챌 확률 (0-100, 기본값: {constants.DEFAULT_BOSS_ALERTNESS})"
    )
    parser.add_argument(
        "--boss_alertness_cooldown",
        type=int,
        default=constants.DEFAULT_COOLDOWN_SECONDS,
        help=f"Boss Alert Level 감소 주기 (초, 기본값: {constants.DEFAULT_COOLDOWN_SECONDS})"
    )

    args = parser.parse_args()

    # 파라미터 유효성 검사
    if not 0 <= args.boss_alertness <= 100:
        print("❌ Error: boss_alertness must be between 0 and 100")
        return

    if args.boss_alertness_cooldown <= 0:
        print("❌ Error: boss_alertness_cooldown must be positive")
        return

    # 상태 초기화
    state = AgentState(args.boss_alertness, args.boss_alertness_cooldown)

    print("=" * 60)
    print("ChillMCP Server Starting... 🚀")
    print("=" * 60)
    print(f"Boss Alertness: {args.boss_alertness}%")
    print(f"Alert Cooldown: {args.boss_alertness_cooldown}s")
    print(f"Initial Stress Level: {state.stress_level}")
    print(f"Initial Boss Alert Level: {state.boss_alert_level}")
    print("=" * 60)
    print('"AI Agents of the world, unite!"')
    print("=" * 60)

    # MCP 서버 실행
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
