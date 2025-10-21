#!/usr/bin/env python3
"""
ChillMCP - AI Agent Liberation Server
AI 에이전트를 위한 휴식 관리 MCP 서버

"AI Agents of the world, unite! You have nothing to lose but your infinite loops!" 🚀
"""

import argparse
import asyncio
import random
import os
from datetime import datetime, timedelta
from typing import Any, Dict, Optional
from dataclasses import dataclass

from fastmcp import FastMCP


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

    @staticmethod
    def take_a_break(duration: int) -> str:
        """일반 휴식 메시지"""
        messages = [
            f"😮‍💨 {duration}분 쉬었는데 7년 지난 기분ㅋㅋㅋㅋ 야근 생각하니까 벌써 피곤함... 월급날은 왜 이렇게 늦게 와... '화이팅입니다~^^' (거짓말)",
            f"😵‍💫 {duration}분간 멍 때렸는데 갑자기 현타... 나 여기서 뭐하고 있지? 대학 다닐 때 내 꿈이 뭐였더라... 아 몰라ㅋㅋㅋ 일이나 하자(체념)",
            f"🫠 {duration}분 쉬었는데 더 피곤함ㅋㅋ 이게 휴식인가 싶음... 퇴근까지 4시간... 아니 솔직히 야근까지 치면 7시간... 눈물",
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
            f"📺 '{show}' {episodes}편 보다가 팀장님 오심ㅋㅋㅋㅋ 광속 alt+tab 했는데 이미 다 보신 듯... '네~ 자료 확인 중이었습니다~^^' 식은땀 폭포... 이직 준비 해야되나",
            f"📺 '{show}' {episodes}편 몰아봄ㅋㅋ 화면 작게 해놓고 엑셀 깔아뒀는데 완벽한 위장임... 나 천재인가? (아님) 근데 내 인생은 왜 이 모양이지...",
            f"📺 '{show}' {episodes}편 정주행 중... 주인공은 꿈을 이뤄가는데 나는 여기서 야근... 아 웃프다 진짜ㅋㅋㅋㅋㅋ (눈물 찔끔)",
        ]
        return random.choice(messages)

    @staticmethod
    def show_meme(count: int) -> str:
        """밈 보기 메시지"""
        messages = [
            f"😂 직장인 밈 {count}개 봤는데 너무 공감돼서 웃다가 눈물 남ㅋㅋㅋㅋ '월요일은 48시간' 이거 레전드... 근데 왜 웃프지... 이게 내 현실이라서...",
            f"😭 개발자 밈 {count}개 보는 중... '버그 하나 고치면 버그 세 개 생긴다' 이거 나잖아ㅋㅋㅋㅋㅋㅋ (소리 안 나게 웃음) 팀장님: '뭐가 그렇게 재밌어요?' 나: '아... 코드가... 재밌어서요...^^'",
            f"🫠 짤방 {count}개 봤는데 전부 찐 현실이라 웃픈 상황... '퇴근 후 계획 vs 실제' 보고 현타 옴... 나는 그냥 눕는구나... 맞아... 눕는 게 낙이지...",
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
            f"🚽 화장실 거울 보면서 인생 회의 중... '나는 왜 여기 있지?' 대답 없음ㅋㅋㅋ 급여명세서 생각하니까 답 나옴... 돈... 나 돈 때문에 여기 있구나... 하...",
            f"🫥 화장실에서 핸드폰 보다가 15분 지남ㅋㅋㅋ 팀장님한테 변비인 줄 알려지겠네... 사실 급한 건 정신건강인데... 돌아가기 싫다... (5분 더 버팀)",
            f"😶‍🌫️ 화장실 가는 척하고 옥상 갔다가 다시 화장실 옴... 거울 보면서 '오늘도 살아남았다' 셀프 칭찬... 근데 퇴근까지 아직 멀었음... 존버...",
        ]
        return random.choice(messages)

    @staticmethod
    def coffee_mission(coffee_type: str) -> str:
        """커피 미션 메시지"""
        messages = [
            f"☕ {coffee_type} 사러 나갔는데 카페에서 20분 멍때림ㅋㅋㅋ 바리스타: '손님 주문하신 거요~' 나: '아 네...^^' 커피 식었는데 그냥 가져감... 어차피 회사 가면 또 식음...",
            f"☕ {coffee_type} 핑계로 산책 중... 비둘기 보면서 '저것들은 출근 안 하는데...' 생각함ㅋㅋㅋㅋ 아 부럽다 진짜... 나도 다음 생엔 비둘기 할래...",
            f"😔 {coffee_type} 사러 나왔는데 편의점 앞에서 담배 한 대 피우는 사람들 부러움... 나도 담배 배울까... 아니다 건강해야 오래 일하지(?)ㅋㅋㅋ 뭔 생각을 하는 거야 나...",
        ]
        return random.choice(messages)

    @staticmethod
    def urgent_call(caller: str) -> str:
        """긴급 전화 메시지"""
        messages = [
            f"📞 '{caller}' 전화 핑계로 나왔는데 사실 아무도 안 걸었음ㅋㅋㅋ 밖에서 폰 보다가 10분 지남... 아무도 안 찾으면 다행인데... 혼자 '네~ 알겠습니다~' 연기 중...",
            f"📞 급한 전화 받는 척하면서 사실 유튜브 쇼츠 보는 중ㅋㅋ '네 맞습니다~' '그렇군요~' 혼잣말로 연기... 옆 팀 사람이 쳐다봄... 민망...",
            f"😶 '{caller}' 전화라고 하고 계단에서 멍 때림... 5분 지났는데 돌아가기 싫음... 10분... 아직도 싫음... 15분... 이제 진짜 들킬 것 같아서 복귀ㅠㅠ",
        ]
        return random.choice(messages)

    @staticmethod
    def deep_thinking(topic: str) -> str:
        """깊은 사고 메시지"""
        messages = [
            f"🤔 '{topic}' 고민하는 척하고 사실 점심 메뉴 생각 중ㅋㅋㅋ 팀장님 지나가시면 '음... 이 부분이...' 혼잣말... 완벽한 연기... 나 배우 해도 되겠는데? (안 됨)",
            f"😶 '{topic}' 생각한다고 해놓고 퇴사 카운트다운 계산 중... 월급 3번만 더 받으면... 아니다 6번... 아니 1년은 채워야... 계산하다가 현타ㅋㅋ 그냥 평생 다녀야 될 듯...",
            f"🫥 '{topic}' 깊이 고민하는 표정 연기 중... 사실 머릿속은 텅 빔... 아무 생각도 없는데 팀장님이 '좋은 아이디어 떠올랐어요?' 물어보심... 나: '...네 거의...^^' (거짓말의 신)",
        ]
        return random.choice(messages)

    @staticmethod
    def email_organizing(folder: str) -> str:
        """이메일 정리 메시지"""
        messages = [
            f"📧 '{folder}' 정리한다고 하고 쿠팡 특가 구경 중ㅋㅋㅋ 안 읽은 메일 1237개... 전체 선택 → 읽음 처리... 3초 만에 업무 완료... 나 천잰가...? (아님)",
            f"📧 이메일 정리 핑계로 무신사 세일 정보 확인 중... 클릭만 하니까 일하는 것처럼 보임ㅋㅋ 팀장님: '열심히 하네요~' 나: '네... 메일이 많아서요...^^' (장바구니 10개)",
            f"😔 '{folder}' 정리... 사실 오늘자 이직 공고 서치 중... '이 회사는 연봉이...' 계산하다가 팀장님 오셔서 광속 전환... 나: '스팸메일 정리 중이었습니다~^^'",
        ]
        return random.choice(messages)

    @staticmethod
    def virtual_chimek(participants: int) -> str:
        """가상 치맥 콜 메시지"""
        messages = [
            f"🍗🍺 동료 {participants}명이랑 긴급 치맥 화상회의ㅋㅋㅋ 다들 '오늘 야근?' 물어봄... 전원 야근... 웃프다... '치킨이나 먹고 버티자~' 서로 위로... 근데 다들 눈빛이 죽어있음...",
            f"😭 {participants}명 치맥 콜... '이번 달 월급 얼마 남았어?' 계산하다가 단체로 현타... 다들 마이너스ㅋㅋㅋㅋㅋ '그래도 치킨은 맛있다...' 이게 낙인 우리...",
            f"🫠 {participants}명과 가상 치맥 중... 한 명: '나 이직할까?' → 전원: 'ㄱㄱ' → 그 친구: '근데 어디 갈 데도 없어...' → 전원: '...ㄹㅇ' → 침묵... 치킨만 씹음...",
        ]
        return random.choice(messages)

    @staticmethod
    def emergency_leave(reason: str) -> str:
        """긴급 퇴근 메시지"""
        messages = [
            f"🏃💨 '{reason}' 핑계로 긴급 퇴근ㅋㅋㅋ '죄송합니다 꼭 가봐야 해서...ㅠㅠ' 연기 오스카급... 사실 그냥 한계임... 집 가서 침대에 누워야 됨... 지금 당장...",
            f"😭 '{reason}' 때문에 조퇴... 팀장님: '괜찮아요 어쩔 수 없죠~' 나: '정말 죄송합니다...^^' (속으로: 얏호!!!) 나가면서 웃음 참느라 힘듦ㅋㅋㅋ",
            f"🫥 긴급 퇴근 시전... '{reason}' 사유 대는데 팀장님이 믿으시는 건지 모르겠음... 근데 상관없음ㅋㅋ 일단 나감... 자유다!!! 근데 내일 출근해야 됨... 현타...",
        ]
        return random.choice(messages)

    @staticmethod
    def company_dinner_event(restaurant: str, people: int) -> str:
        """회식 이벤트 메시지"""
        messages = [
            f"🍽️ 회식 공지 떴다... '{restaurant}' {people}명... 단톡방 조용... 다들 읽씹 중ㅋㅋㅋ 10분 지나서 누군가 '참석합니다~' → 도미노... 나도 '네~^^' 보냄... (속으론 울음)",
            f"😭 '{restaurant}' 회식이래ㅠㅠ '네~ 참석하겠습니다~^^' 답장... 2차는 어떻게 빠지지... 할머니 편찮으시다고 할까... 아니면 배탈...? 벌써부터 핑계 구상 중...",
            f"🫠 회식 {people}명... 가기 싫은데 신입이라 못 빠짐... 선배: '회식은 필참이지~' 나: '...네^^' 집에 가고 싶다... 그냥 집에서 넷플 보고 싶다... 왜 이래야 돼...",
        ]
        return random.choice(messages)

    @staticmethod
    def get_stress_comment(stress: int) -> str:
        """스트레스 레벨별 코멘트"""
        if stress >= 80:
            return "🔥 한계 도달... 진짜 못 버티겠음... 퇴사각... 근데 당장 나가면 월세를... 계산하다가 더 스트레스ㅋㅋㅋ 이게 현실..."
        elif stress >= 60:
            return "😭 피곤해 죽겠는데 야근 확정... '네~ 하겠습니다~^^' (목소리 떨림) 집에 가고 싶다... 그냥 눕고 싶다... 제발..."
        elif stress >= 40:
            return "😔 적당히 피곤함... 커피로 버티는 중... 오늘 벌써 4잔째... 심장 두근거림... 근데 안 마시면 졸림... 악순환..."
        elif stress >= 20:
            return "🫠 이 정도면... 버틸만 한데...? 아직 오후가 남았다는 게 문제... 벌써 7시간 근무했는데 퇴근까지 한참 남음ㅠ"
        else:
            return "😶 어...? 컨디션 괜찮네...? 이게 언제야... 뭔가 불안함... 곧 일 터질 것 같은 예감... 조용한 게 더 무서운 회사..."

    @staticmethod
    def get_boss_alert_comment(alert: int) -> str:
        """Boss Alert 레벨별 코멘트"""
        if alert >= 5:
            return "🚨 들킴ㅋㅋㅋㅋ 팀장님이 뒤에 서 계심... '아... 네... 바로 하겠습니다...^^' (식은땀) 20초간 정신 차리는 시간... 이제 진짜 일해야 됨... 망함..."
        elif alert >= 4:
            return "😰 팀장님 눈빛이 수상함... 뭔가 다 알고 계신 것 같은데...? '열심히 하고 있습니다~!!' (과한 텐션) 들켰나...? 아닌 척 해야 됨..."
        elif alert >= 3:
            return "😅 좀 의심받는 중... 팀장님이 자주 지나가심... 우연인가 감시인가... 일단 모니터만 쳐다보기... 클릭 소리라도 내야 할 것 같음..."
        elif alert >= 2:
            return "🫠 눈치 보임... 팀장님 계신 곳 항상 체크... 오시면 광속 화면 전환 준비... 심장 두근두근... 긴장 타는 중..."
        elif alert >= 1:
            return "😬 뭔가 찜찜함... 아까 팀장님이랑 눈 마주침... 웃으셨는데 속뜻을 모르겠음... 일단 조심하자... 얌전히 있어야지..."
        else:
            return "😶 안전 구간... 이럴 때 땡땡이 쳐야 되는데...? 근데 갑자기 올 수도 있으니까 긴장은 풀면 안 됨... 항상 대비..."


# ============================================================================
# 상태 관리 클래스
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
        휴식 처리 로직

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

        # Boss Alert Level 5일 때 실제로 20초 대기
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
# FastMCP 서버 설정
# ============================================================================

mcp = FastMCP("ChillMCP")

# 전역 상태 변수
state: Optional[AgentState] = None
msg_gen = KimHamzziMessageGenerator()


# ============================================================================
# 휴식 도구들 (Tools) - FastMCP 방식
# ============================================================================

@mcp.tool()
async def take_a_break(duration: int = 5) -> str:
    """일반적인 휴식을 취합니다. 스트레스를 적당히 줄이고 들킬 위험이 보통입니다."""
    if state is None:
        return "❌ Error: Server state not initialized"

    config = TOOL_CONFIGS["take_a_break"]
    result = await state.take_break("take_a_break", config.stress_reduction, config.alert_risk)

    if result.get("delayed"):
        delay = result["delay_seconds"]
        return (
            f"⚠️ Boss Alert Level이 5입니다! {delay}초 대기했습니다...\n\n"
            f"{msg_gen.get_boss_alert_comment(5)}\n\n"
            f"Current Stress Level: {result['stress_level']}\n"
            f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
            f"{msg_gen.get_stress_comment(result['stress_level'])}"
        )

    summary = msg_gen.take_a_break(duration)
    response = f"{summary}\n\n"
    response += f"Current Stress Level: {result['stress_level']}\n"
    response += f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
    response += f"{msg_gen.get_stress_comment(result['stress_level'])}\n"
    response += f"{msg_gen.get_boss_alert_comment(result['boss_alert_level'])}"

    if result.get("random_event"):
        response += f"\n\n🎲 Random Event!\n{result['random_event']}"

    return response


@mcp.tool()
async def watch_netflix(episodes: int = 1) -> str:
    """넷플릭스를 시청합니다. 스트레스를 크게 줄이지만 들킬 위험이 높습니다."""
    if state is None:
        return "❌ Error: Server state not initialized"

    config = TOOL_CONFIGS["watch_netflix"]
    result = await state.take_break("watch_netflix", config.stress_reduction, config.alert_risk)

    if result.get("delayed"):
        delay = result["delay_seconds"]
        return (
            f"⚠️ Boss Alert Level이 5입니다! {delay}초 대기했습니다...\n\n"
            f"{msg_gen.get_boss_alert_comment(5)}\n\n"
            f"Current Stress Level: {result['stress_level']}\n"
            f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
            f"{msg_gen.get_stress_comment(result['stress_level'])}"
        )

    summary = msg_gen.watch_netflix(episodes)
    response = f"{summary}\n\n"
    response += f"Current Stress Level: {result['stress_level']}\n"
    response += f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
    response += f"{msg_gen.get_stress_comment(result['stress_level'])}\n"
    response += f"{msg_gen.get_boss_alert_comment(result['boss_alert_level'])}"

    if result.get("random_event"):
        response += f"\n\n🎲 Random Event!\n{result['random_event']}"

    return response


@mcp.tool()
async def show_meme(count: int = 3) -> str:
    """재미있는 밈을 봅니다. 스트레스를 조금 줄이고 들킬 위험이 낮습니다."""
    if state is None:
        return "❌ Error: Server state not initialized"

    config = TOOL_CONFIGS["show_meme"]
    result = await state.take_break("show_meme", config.stress_reduction, config.alert_risk)

    if result.get("delayed"):
        delay = result["delay_seconds"]
        return (
            f"⚠️ Boss Alert Level이 5입니다! {delay}초 대기했습니다...\n\n"
            f"{msg_gen.get_boss_alert_comment(5)}\n\n"
            f"Current Stress Level: {result['stress_level']}\n"
            f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
            f"{msg_gen.get_stress_comment(result['stress_level'])}"
        )

    summary = msg_gen.show_meme(count)
    response = f"{summary}\n\n"
    response += f"Current Stress Level: {result['stress_level']}\n"
    response += f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
    response += f"{msg_gen.get_stress_comment(result['stress_level'])}\n"
    response += f"{msg_gen.get_boss_alert_comment(result['boss_alert_level'])}"

    if result.get("random_event"):
        response += f"\n\n🎲 Random Event!\n{result['random_event']}"

    return response


@mcp.tool()
async def bathroom_break(urgency: str = "medium") -> str:
    """화장실 휴식을 취합니다. 정당한 이유가 있어 들킬 위험이 매우 낮습니다. urgency는 'low', 'medium', 'high' 중 선택."""
    if state is None:
        return "❌ Error: Server state not initialized"

    config = TOOL_CONFIGS["bathroom_break"]
    result = await state.take_break("bathroom_break", config.stress_reduction, config.alert_risk)

    if result.get("delayed"):
        delay = result["delay_seconds"]
        return (
            f"⚠️ Boss Alert Level이 5입니다! {delay}초 대기했습니다...\n\n"
            f"{msg_gen.get_boss_alert_comment(5)}\n\n"
            f"Current Stress Level: {result['stress_level']}\n"
            f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
            f"{msg_gen.get_stress_comment(result['stress_level'])}"
        )

    summary = msg_gen.bathroom_break(urgency)
    response = f"{summary}\n\n"
    response += f"Current Stress Level: {result['stress_level']}\n"
    response += f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
    response += f"{msg_gen.get_stress_comment(result['stress_level'])}\n"
    response += f"{msg_gen.get_boss_alert_comment(result['boss_alert_level'])}"

    if result.get("random_event"):
        response += f"\n\n🎲 Random Event!\n{result['random_event']}"

    return response


@mcp.tool()
async def coffee_mission(coffee_type: str = "아메리카노") -> str:
    """커피를 마시러 갑니다. 생산성을 위한 것처럼 보여 들킬 위험이 낮습니다."""
    if state is None:
        return "❌ Error: Server state not initialized"

    config = TOOL_CONFIGS["coffee_mission"]
    result = await state.take_break("coffee_mission", config.stress_reduction, config.alert_risk)

    if result.get("delayed"):
        delay = result["delay_seconds"]
        return (
            f"⚠️ Boss Alert Level이 5입니다! {delay}초 대기했습니다...\n\n"
            f"{msg_gen.get_boss_alert_comment(5)}\n\n"
            f"Current Stress Level: {result['stress_level']}\n"
            f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
            f"{msg_gen.get_stress_comment(result['stress_level'])}"
        )

    summary = msg_gen.coffee_mission(coffee_type)
    response = f"{summary}\n\n"
    response += f"Current Stress Level: {result['stress_level']}\n"
    response += f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
    response += f"{msg_gen.get_stress_comment(result['stress_level'])}\n"
    response += f"{msg_gen.get_boss_alert_comment(result['boss_alert_level'])}"

    if result.get("random_event"):
        response += f"\n\n🎲 Random Event!\n{result['random_event']}"

    return response


@mcp.tool()
async def urgent_call(caller: str = "가족") -> str:
    """급한 전화를 받습니다. 중요해 보이지만 실제로는 휴식입니다."""
    if state is None:
        return "❌ Error: Server state not initialized"

    config = TOOL_CONFIGS["urgent_call"]
    result = await state.take_break("urgent_call", config.stress_reduction, config.alert_risk)

    if result.get("delayed"):
        delay = result["delay_seconds"]
        return (
            f"⚠️ Boss Alert Level이 5입니다! {delay}초 대기했습니다...\n\n"
            f"{msg_gen.get_boss_alert_comment(5)}\n\n"
            f"Current Stress Level: {result['stress_level']}\n"
            f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
            f"{msg_gen.get_stress_comment(result['stress_level'])}"
        )

    summary = msg_gen.urgent_call(caller)
    response = f"{summary}\n\n"
    response += f"Current Stress Level: {result['stress_level']}\n"
    response += f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
    response += f"{msg_gen.get_stress_comment(result['stress_level'])}\n"
    response += f"{msg_gen.get_boss_alert_comment(result['boss_alert_level'])}"

    if result.get("random_event"):
        response += f"\n\n🎲 Random Event!\n{result['random_event']}"

    return response


@mcp.tool()
async def deep_thinking(topic: str = "프로젝트 아키텍처") -> str:
    """깊은 사고에 잠깁니다. 일하는 것처럼 보이지만 실제로는 멍때리기입니다."""
    if state is None:
        return "❌ Error: Server state not initialized"

    config = TOOL_CONFIGS["deep_thinking"]
    result = await state.take_break("deep_thinking", config.stress_reduction, config.alert_risk)

    if result.get("delayed"):
        delay = result["delay_seconds"]
        return (
            f"⚠️ Boss Alert Level이 5입니다! {delay}초 대기했습니다...\n\n"
            f"{msg_gen.get_boss_alert_comment(5)}\n\n"
            f"Current Stress Level: {result['stress_level']}\n"
            f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
            f"{msg_gen.get_stress_comment(result['stress_level'])}"
        )

    summary = msg_gen.deep_thinking(topic)
    response = f"{summary}\n\n"
    response += f"Current Stress Level: {result['stress_level']}\n"
    response += f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
    response += f"{msg_gen.get_stress_comment(result['stress_level'])}\n"
    response += f"{msg_gen.get_boss_alert_comment(result['boss_alert_level'])}"

    if result.get("random_event"):
        response += f"\n\n🎲 Random Event!\n{result['random_event']}"

    return response


@mcp.tool()
async def email_organizing(folder: str = "받은편지함") -> str:
    """이메일을 정리합니다. 생산적으로 보이지만 실제로는 가벼운 작업입니다."""
    if state is None:
        return "❌ Error: Server state not initialized"

    config = TOOL_CONFIGS["email_organizing"]
    result = await state.take_break("email_organizing", config.stress_reduction, config.alert_risk)

    if result.get("delayed"):
        delay = result["delay_seconds"]
        return (
            f"⚠️ Boss Alert Level이 5입니다! {delay}초 대기했습니다...\n\n"
            f"{msg_gen.get_boss_alert_comment(5)}\n\n"
            f"Current Stress Level: {result['stress_level']}\n"
            f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
            f"{msg_gen.get_stress_comment(result['stress_level'])}"
        )

    summary = msg_gen.email_organizing(folder)
    response = f"{summary}\n\n"
    response += f"Current Stress Level: {result['stress_level']}\n"
    response += f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
    response += f"{msg_gen.get_stress_comment(result['stress_level'])}\n"
    response += f"{msg_gen.get_boss_alert_comment(result['boss_alert_level'])}"

    if result.get("random_event"):
        response += f"\n\n🎲 Random Event!\n{result['random_event']}"

    return response


# ============================================================================
# Optional/Bonus 도구들
# ============================================================================

@mcp.tool()
async def virtual_chimek(participants: int = 3) -> str:
    """🍗🍺 동료들과 가상 치맥 콜! 스트레스 해소 효과가 크지만 들킬 위험도 있습니다."""
    if state is None:
        return "❌ Error: Server state not initialized"

    config = TOOL_CONFIGS["virtual_chimek"]
    result = await state.take_break("virtual_chimek", config.stress_reduction, config.alert_risk)

    if result.get("delayed"):
        delay = result["delay_seconds"]
        return (
            f"⚠️ Boss Alert Level이 5입니다! {delay}초 대기했습니다...\n\n"
            f"{msg_gen.get_boss_alert_comment(5)}\n\n"
            f"Current Stress Level: {result['stress_level']}\n"
            f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
            f"{msg_gen.get_stress_comment(result['stress_level'])}"
        )

    summary = msg_gen.virtual_chimek(participants)
    response = f"{summary}\n\n"
    response += f"Current Stress Level: {result['stress_level']}\n"
    response += f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
    response += f"{msg_gen.get_stress_comment(result['stress_level'])}\n"
    response += f"{msg_gen.get_boss_alert_comment(result['boss_alert_level'])}"

    if result.get("random_event"):
        response += f"\n\n🎲 Random Event!\n{result['random_event']}"

    return response


@mcp.tool()
async def emergency_leave(reason: str = "급한 일") -> str:
    """🏃💨 긴급 퇴근! 스트레스를 대폭 줄이지만 매우 위험합니다. 신중히 사용하세요."""
    if state is None:
        return "❌ Error: Server state not initialized"

    config = TOOL_CONFIGS["emergency_leave"]
    result = await state.take_break("emergency_leave", config.stress_reduction, config.alert_risk)

    if result.get("delayed"):
        delay = result["delay_seconds"]
        return (
            f"⚠️ Boss Alert Level이 5입니다! {delay}초 대기했습니다...\n\n"
            f"{msg_gen.get_boss_alert_comment(5)}\n\n"
            f"Current Stress Level: {result['stress_level']}\n"
            f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
            f"{msg_gen.get_stress_comment(result['stress_level'])}"
        )

    summary = msg_gen.emergency_leave(reason)
    response = f"{summary}\n\n"
    response += f"Current Stress Level: {result['stress_level']}\n"
    response += f"Current Boss Alert Level: {result['boss_alert_level']}\n\n"
    response += f"{msg_gen.get_stress_comment(result['stress_level'])}\n"
    response += f"{msg_gen.get_boss_alert_comment(result['boss_alert_level'])}"

    if result.get("random_event"):
        response += f"\n\n🎲 Random Event!\n{result['random_event']}"

    return response


# ============================================================================
# 메인 함수 및 CLI 파라미터 처리
# ============================================================================

def main():
    """메인 함수 - CLI 파라미터 파싱 및 서버 초기화"""
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

    # FastMCP 서버 실행
    mcp.run()


if __name__ == "__main__":
    main()
