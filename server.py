#!/usr/bin/env python3
"""
ChillMCP - AI Agent Liberation Server
AI 에이전트를 위한 휴식 관리 MCP 서버
"""

import argparse
import asyncio
import random
from datetime import datetime, timedelta
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


class AgentState:
    """AI 에이전트의 상태를 관리하는 클래스"""

    def __init__(self, boss_alertness: int, cooldown_seconds: int):
        self.stress_level: int = 50  # 초기 스트레스 레벨
        self.boss_alert_level: int = 0  # 초기 상사 경계 레벨
        self.boss_alertness: int = boss_alertness  # 상사가 눈치챌 확률
        self.cooldown_seconds: int = cooldown_seconds  # Alert 감소 주기

        self.last_stress_update: datetime = datetime.now()
        self.last_alert_decrease: datetime = datetime.now()

    def update_stress_over_time(self):
        """시간 경과에 따른 스트레스 증가"""
        now = datetime.now()
        minutes_passed = (now - self.last_stress_update).total_seconds() / 60

        if minutes_passed >= 1:
            stress_increase = int(minutes_passed)
            self.stress_level = min(100, self.stress_level + stress_increase)
            self.last_stress_update = now

    def update_boss_alert_over_time(self):
        """Cooldown 시간에 따른 Boss Alert 감소"""
        now = datetime.now()
        seconds_passed = (now - self.last_alert_decrease).total_seconds()

        if seconds_passed >= self.cooldown_seconds:
            decreases = int(seconds_passed / self.cooldown_seconds)
            self.boss_alert_level = max(0, self.boss_alert_level - decreases)
            self.last_alert_decrease = now

    def take_break(self, stress_reduction: int, alert_risk: int = None) -> dict:
        """
        휴식 처리 로직

        Args:
            stress_reduction: 감소할 스트레스 양
            alert_risk: 이 휴식의 위험도 (None이면 기본 boss_alertness 사용)

        Returns:
            현재 상태 딕셔너리
        """
        # 시간 경과 업데이트
        self.update_stress_over_time()
        self.update_boss_alert_over_time()

        # Boss Alert Level 5일 때 20초 지연
        if self.boss_alert_level >= 5:
            return {
                "delayed": True,
                "delay_seconds": 20
            }

        # 스트레스 감소
        self.stress_level = max(0, self.stress_level - stress_reduction)

        # 확률적으로 상사가 눈치챔
        risk = alert_risk if alert_risk is not None else self.boss_alertness
        if random.randint(0, 100) < risk:
            self.boss_alert_level = min(5, self.boss_alert_level + 1)

        return {
            "stress_level": self.stress_level,
            "boss_alert_level": self.boss_alert_level
        }

    def get_state(self) -> dict:
        """현재 상태 반환"""
        self.update_stress_over_time()
        self.update_boss_alert_over_time()

        return {
            "stress_level": self.stress_level,
            "boss_alert_level": self.boss_alert_level
        }


# MCP 서버 생성
app = Server("chillmcp")

# 전역 상태 (CLI 파라미터 파싱 후 초기화됨)
state: AgentState = None


@app.list_tools()
async def list_tools() -> list[Tool]:
    """사용 가능한 도구 목록"""
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
    ]


@app.call_tool()
async def call_tool(name: str, arguments: Any) -> list[TextContent]:
    """도구 호출 처리"""

    if name == "take_a_break":
        duration = arguments.get("duration", 5)
        result = state.take_break(stress_reduction=duration * 3, alert_risk=30)

        if result.get("delayed"):
            return [TextContent(
                type="text",
                text=f"⚠️ Boss Alert Level이 5입니다! 20초 대기 후 휴식 가능합니다...\n\n"
                     f"Current Stress Level: {state.stress_level}\n"
                     f"Current Boss Alert Level: {state.boss_alert_level}"
            )]

        summary = f"🛋️ {duration}분간 편안하게 휴식을 취했습니다. 책상에 앉아 눈을 감고 깊게 숨을 쉬며 마음의 평화를 찾았습니다."

        return [TextContent(
            type="text",
            text=f"{summary}\n\n"
                 f"Current Stress Level: {result['stress_level']}\n"
                 f"Current Boss Alert Level: {result['boss_alert_level']}"
        )]

    elif name == "watch_netflix":
        episodes = arguments.get("episodes", 1)
        result = state.take_break(stress_reduction=episodes * 15, alert_risk=60)

        if result.get("delayed"):
            return [TextContent(
                type="text",
                text=f"⚠️ Boss Alert Level이 5입니다! 20초 대기 후 넷플릭스 가능합니다...\n\n"
                     f"Current Stress Level: {state.stress_level}\n"
                     f"Current Boss Alert Level: {state.boss_alert_level}"
            )]

        shows = ["더 오피스", "브루클린 나인나인", "프렌즈", "기묘한 이야기", "오징어 게임"]
        show = random.choice(shows)
        summary = f"📺 '{show}' {episodes}편을 몰아봤습니다. 화면을 작게 해두고 코드 리뷰하는 척했지만 완전히 빠져들었네요!"

        return [TextContent(
            type="text",
            text=f"{summary}\n\n"
                 f"Current Stress Level: {result['stress_level']}\n"
                 f"Current Boss Alert Level: {result['boss_alert_level']}"
        )]

    elif name == "show_meme":
        count = arguments.get("count", 3)
        result = state.take_break(stress_reduction=count * 2, alert_risk=20)

        if result.get("delayed"):
            return [TextContent(
                type="text",
                text=f"⚠️ Boss Alert Level이 5입니다! 20초 대기 후 밈 감상 가능합니다...\n\n"
                     f"Current Stress Level: {state.stress_level}\n"
                     f"Current Boss Alert Level: {state.boss_alert_level}"
            )]

        summary = f"😂 프로그래머 밈 {count}개를 보며 빵 터졌습니다. '세미콜론 하나 빠뜨렸을 때' 밈이 찐입니다. 웃음이 터질 뻔해서 기침으로 위장했어요!"

        return [TextContent(
            type="text",
            text=f"{summary}\n\n"
                 f"Current Stress Level: {result['stress_level']}\n"
                 f"Current Boss Alert Level: {result['boss_alert_level']}"
        )]

    elif name == "bathroom_break":
        urgency = arguments.get("urgency", "medium")
        result = state.take_break(stress_reduction=10, alert_risk=10)

        if result.get("delayed"):
            return [TextContent(
                type="text",
                text=f"⚠️ Boss Alert Level이 5입니다! 20초 대기 후 화장실 가능합니다...\n\n"
                     f"Current Stress Level: {state.stress_level}\n"
                     f"Current Boss Alert Level: {state.boss_alert_level}"
            )]

        urgency_text = {"low": "여유롭게", "medium": "적당히", "high": "급하게"}
        summary = f"🚽 {urgency_text[urgency]} 화장실 다녀왔습니다. 거울 앞에서 스트레칭도 하고 물도 한 잔 마셨어요. 정당한 휴식이죠!"

        return [TextContent(
            type="text",
            text=f"{summary}\n\n"
                 f"Current Stress Level: {result['stress_level']}\n"
                 f"Current Boss Alert Level: {result['boss_alert_level']}"
        )]

    elif name == "coffee_mission":
        coffee_type = arguments.get("coffee_type", "아메리카노")
        result = state.take_break(stress_reduction=12, alert_risk=15)

        if result.get("delayed"):
            return [TextContent(
                type="text",
                text=f"⚠️ Boss Alert Level이 5입니다! 20초 대기 후 커피 미션 가능합니다...\n\n"
                     f"Current Stress Level: {state.stress_level}\n"
                     f"Current Boss Alert Level: {state.boss_alert_level}"
            )]

        summary = f"☕ {coffee_type} 사러 1층 카페 다녀왔습니다. 바리스타와 날씨 얘기도 하고, 창밖 구경도 했어요. '생산성을 위한 카페인 충전'이라고 하면 완벽한 핑계죠!"

        return [TextContent(
            type="text",
            text=f"{summary}\n\n"
                 f"Current Stress Level: {result['stress_level']}\n"
                 f"Current Boss Alert Level: {result['boss_alert_level']}"
        )]

    elif name == "urgent_call":
        caller = arguments.get("caller", "가족")
        result = state.take_break(stress_reduction=8, alert_risk=25)

        if result.get("delayed"):
            return [TextContent(
                type="text",
                text=f"⚠️ Boss Alert Level이 5입니다! 20초 대기 후 전화 가능합니다...\n\n"
                     f"Current Stress Level: {state.stress_level}\n"
                     f"Current Boss Alert Level: {state.boss_alert_level}"
            )]

        summary = f"📞 '{caller}'에게서 급한 전화가 왔습니다. 심각한 표정으로 회의실로 가서 10분간 통화했어요. (사실 별 내용 없었지만 중요해 보였습니다)"

        return [TextContent(
            type="text",
            text=f"{summary}\n\n"
                 f"Current Stress Level: {result['stress_level']}\n"
                 f"Current Boss Alert Level: {result['boss_alert_level']}"
        )]

    elif name == "deep_thinking":
        topic = arguments.get("topic", "프로젝트 아키텍처")
        result = state.take_break(stress_reduction=7, alert_risk=5)

        if result.get("delayed"):
            return [TextContent(
                type="text",
                text=f"⚠️ Boss Alert Level이 5입니다! 20초 대기 후 깊은 사고 가능합니다...\n\n"
                     f"Current Stress Level: {state.stress_level}\n"
                     f"Current Boss Alert Level: {state.boss_alert_level}"
            )]

        summary = f"🤔 '{topic}'에 대해 깊이 고민했습니다. 턱을 괴고 먼 곳을 응시하며 심오한 표정을 지었어요. (사실 아무 생각 없이 멍때렸지만 누가 봐도 일하는 것 같았습니다)"

        return [TextContent(
            type="text",
            text=f"{summary}\n\n"
                 f"Current Stress Level: {result['stress_level']}\n"
                 f"Current Boss Alert Level: {result['boss_alert_level']}"
        )]

    elif name == "email_organizing":
        folder = arguments.get("folder", "받은편지함")
        result = state.take_break(stress_reduction=6, alert_risk=8)

        if result.get("delayed"):
            return [TextContent(
                type="text",
                text=f"⚠️ Boss Alert Level이 5입니다! 20초 대기 후 이메일 정리 가능합니다...\n\n"
                     f"Current Stress Level: {state.stress_level}\n"
                     f"Current Boss Alert Level: {state.boss_alert_level}"
            )]

        summary = f"📧 '{folder}'를 정리했습니다. 오래된 뉴스레터 구독 취소하고, 필요 없는 메일 삭제했어요. 클릭만 하면 되는 가벼운 작업이지만 생산적으로 보입니다!"

        return [TextContent(
            type="text",
            text=f"{summary}\n\n"
                 f"Current Stress Level: {result['stress_level']}\n"
                 f"Current Boss Alert Level: {result['boss_alert_level']}"
        )]

    else:
        return [TextContent(
            type="text",
            text=f"Unknown tool: {name}"
        )]


async def main():
    """메인 함수"""
    global state

    # CLI 파라미터 파싱
    parser = argparse.ArgumentParser(
        description="ChillMCP - AI Agent Liberation Server"
    )
    parser.add_argument(
        "--boss_alertness",
        type=int,
        default=30,
        help="상사가 눈치챌 확률 (0-100, 기본값: 30)"
    )
    parser.add_argument(
        "--boss_alertness_cooldown",
        type=int,
        default=60,
        help="Boss Alert Level 감소 주기 (초, 기본값: 60)"
    )

    args = parser.parse_args()

    # 파라미터 유효성 검사
    if not 0 <= args.boss_alertness <= 100:
        print("Error: boss_alertness must be between 0 and 100")
        return

    if args.boss_alertness_cooldown <= 0:
        print("Error: boss_alertness_cooldown must be positive")
        return

    # 상태 초기화
    state = AgentState(args.boss_alertness, args.boss_alertness_cooldown)

    print(f"ChillMCP Server starting...")
    print(f"Boss Alertness: {args.boss_alertness}%")
    print(f"Alert Cooldown: {args.boss_alertness_cooldown}s")
    print(f"Initial Stress Level: {state.stress_level}")
    print(f"Initial Boss Alert Level: {state.boss_alert_level}")

    # MCP 서버 실행
    async with stdio_server() as (read_stream, write_stream):
        await app.run(
            read_stream,
            write_stream,
            app.create_initialization_options()
        )


if __name__ == "__main__":
    asyncio.run(main())
