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
            f"🛋️ {duration}분간 책상에 앉아서 천장 얼룩 세기... 오늘은 7개",
            f"😌 {duration}분 휴식 완료. '마지막이다' 다짐 (3번째)",
            f"☕ 아메리카노 10분 식힌 후 한 모금... 이제 진짜 일함 (거짓말)",
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
            f"📺 '{show}' {episodes}편 시청 중... 소리 음소거 + 자막 ON + 이어폰 한쪽만 (상사 발소리 감지 모드)",
            f"📺 {episodes}편 몰아보기! 화면 밝기 30%로 낮춤 + alt+tab 사전 연습 완료",
            f"📺 '{show}' 정주행 중... 이것도 트렌드 파악이라고 (자기합리화)",
        ]
        return random.choice(messages)

    @staticmethod
    def show_meme(count: int) -> str:
        """밈 보기 메시지"""
        messages = [
            f"😂 직장인 밈 {count}개 저장... 또 보고 또 저장 (밈 폴더 327개)",
            f"📱 개발자 밈 보다가 웃음 터질 뻔... 기침으로 위장 성공",
            f"🤣 밈 {count}개 감상 후 카톡으로 공유... 단톡방 활성화 중 (생산적)",
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
            f"🚽 화장실 5번째 방문... 오늘 기록 경신 중 📱",
            f"🫥 화장실에서 {urgency_map[urgency]} SNS 10분... 사실 12분",
            f"😌 거울 보며 '할 수 있다' 자기암시 (안 믿음)",
        ]
        return random.choice(messages)

    @staticmethod
    def coffee_mission(coffee_type: str) -> str:
        """커피 미션 메시지"""
        messages = [
            f"☕ {coffee_type} 사러 나가는 길... 엘리베이터 3층 갔다가 다시 내려옴 (이유 모름)",
            f"☕ {coffee_type} 타는 동안 타일 개수 셈... 47개",
            f"☕ 커피 식히는 5분이 진짜 휴식... 생산성을 위한 투자 (핑계)",
        ]
        return random.choice(messages)

    @staticmethod
    def urgent_call(caller: str) -> str:
        """긴급 전화 메시지"""
        messages = [
            f"📞 '{caller}' 전화 핑계로 복도 배회 7분... 통화하는 척 연기력 발휘",
            f"📞 중요한 전화 받는 척... 실제로는 날씨 앱만 3분간 봄",
            f"📞 '{caller}' 전화로 잠깐 나옴... 사실 그냥 숨 쉬러 (정당한 이유)",
        ]
        return random.choice(messages)

    @staticmethod
    def deep_thinking(topic: str) -> str:
        """깊은 사고 메시지"""
        messages = [
            f"🤔 '{topic}'에 대해 심오하게 고민 중... 턱 괸 채 화면 응시 (멍)",
            f"💭 턱 괴고 '{topic}' 구상 중 (5분째 같은 문장만 봄)",
            f"🧠 '{topic}' 관련 깊은 사고... 이것도 업무의 일부 (자기합리화)",
        ]
        return random.choice(messages)

    @staticmethod
    def email_organizing(folder: str) -> str:
        """이메일 정리 메시지"""
        messages = [
            f"📧 '{folder}' 청소 중... 스팸 메일 217개 전부 읽어봄 (왜?)",
            f"📧 이메일 정리한다며 뉴스레터 구독... 클릭하니까 일하는 것처럼 보임",
            f"📨 '{folder}' 정리 중... 안 읽은 메일 전체 읽음 처리! (생산적)",
        ]
        return random.choice(messages)

    @staticmethod
    def virtual_chimek(participants: int) -> str:
        """가상 치맥 콜 메시지"""
        messages = [
            f"🍗🍺 동료 {participants}명과 가상 치맥! 30분 예정 (1시간 됨)",
            f"🍗🍺 {participants}명이랑 치맥 통화... 회사 불평하다 보니 시간 순삭",
            f"🍗🍺 긴급 치맥 회의 소집! {participants}명 참석... 이것도 팀워크 강화 (자기합리화)",
        ]
        return random.choice(messages)

    @staticmethod
    def emergency_leave(reason: str) -> str:
        """긴급 퇴근 메시지"""
        messages = [
            f"🏃💨 '{reason}' 긴급 퇴근! 내일 2배로 일함 (거짓말)",
            f"🏃💨 조퇴 성공... '{reason}' 핑계 완벽 (연기 대상감)",
            f"🏃💨 '{reason}'으로 먼저 나갑니다... 내일 보겠습니다~ (죄책감 0)",
        ]
        return random.choice(messages)

    @staticmethod
    def company_dinner_event(restaurant: str, people: int) -> str:
        """회식 이벤트 메시지"""
        messages = [
            f"🍽️ 회식 공지... '{restaurant}' {people}명... 1차만 참석 예정 (2차 도망 계획 수립 중)",
            f"🍽️ '{restaurant}' 회식! {people}명 모인다는데... 술 약하다고 미리 말해둠",
            f"🍽️ 갑자기 회식... '{restaurant}'에서 {people}명... 뭐 공짜 밥이니까 (긍정적 마인드)",
        ]
        return random.choice(messages)

    @staticmethod
    def get_stress_comment(stress: int) -> str:
        """스트레스 레벨별 코멘트"""
        if stress >= 80:
            return "🔥 스트레스 위험 수준! 휴식이 절실히 필요함"
        elif stress >= 60:
            return "😰 피곤도가 높음... 적절한 휴식 권장"
        elif stress >= 40:
            return "😔 중간 정도 스트레스... 커피 한 잔 어때?"
        elif stress >= 20:
            return "🫠 약간 피곤한 상태... 아직은 버틸만 함"
        else:
            return "😊 컨디션 좋음! 일하기 딱 좋은 상태"

    @staticmethod
    def get_boss_alert_comment(alert: int) -> str:
        """Boss Alert 레벨별 코멘트"""
        if alert >= 5:
            return "🚨 Boss Alert 최고 레벨! 20초 대기 페널티 발동..."
        elif alert >= 4:
            return "😰 상사가 의심하는 중... 조심해야 함"
        elif alert >= 3:
            return "😅 좀 눈치 보이기 시작... 적당히 일하는 척 필요"
        elif alert >= 2:
            return "🫠 약간 찜찜한 상태... 조심스럽게 행동 중"
        elif alert >= 1:
            return "😬 살짝 경계 모드... 아직은 괜찮음"
        else:
            return "😌 안전! 상사가 전혀 의심하지 않는 중"


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
