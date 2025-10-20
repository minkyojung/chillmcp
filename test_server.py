#!/usr/bin/env python3
"""
ChillMCP 서버 테스트 스크립트
MCP 클라이언트로 서버에 연결하여 도구들을 테스트합니다.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_chillmcp():
    """ChillMCP 서버 테스트"""

    # 서버 파라미터 설정
    server_params = StdioServerParameters(
        command="python",
        args=["server.py", "--boss_alertness", "40", "--boss_alertness_cooldown", "30"],
        env=None
    )

    print("🚀 ChillMCP 서버에 연결 중...")

    async with stdio_client(server_params) as (read, write):
        async with ClientSession(read, write) as session:
            # 서버 초기화
            await session.initialize()

            print("✅ 서버 연결 성공!\n")

            # 사용 가능한 도구 목록 가져오기
            tools = await session.list_tools()
            print(f"📋 사용 가능한 도구: {len(tools.tools)}개\n")

            for tool in tools.tools:
                print(f"  - {tool.name}: {tool.description}")

            print("\n" + "="*60)
            print("도구 테스트 시작")
            print("="*60 + "\n")

            # 1. take_a_break 테스트
            print("1️⃣ take_a_break 테스트")
            print("-" * 60)
            result = await session.call_tool("take_a_break", {"duration": 5})
            print(result.content[0].text)
            print()

            await asyncio.sleep(1)

            # 2. watch_netflix 테스트
            print("2️⃣ watch_netflix 테스트")
            print("-" * 60)
            result = await session.call_tool("watch_netflix", {"episodes": 2})
            print(result.content[0].text)
            print()

            await asyncio.sleep(1)

            # 3. show_meme 테스트
            print("3️⃣ show_meme 테스트")
            print("-" * 60)
            result = await session.call_tool("show_meme", {"count": 5})
            print(result.content[0].text)
            print()

            await asyncio.sleep(1)

            # 4. bathroom_break 테스트
            print("4️⃣ bathroom_break 테스트")
            print("-" * 60)
            result = await session.call_tool("bathroom_break", {"urgency": "high"})
            print(result.content[0].text)
            print()

            await asyncio.sleep(1)

            # 5. coffee_mission 테스트
            print("5️⃣ coffee_mission 테스트")
            print("-" * 60)
            result = await session.call_tool("coffee_mission", {"coffee_type": "카페라떼"})
            print(result.content[0].text)
            print()

            await asyncio.sleep(1)

            # 6. urgent_call 테스트
            print("6️⃣ urgent_call 테스트")
            print("-" * 60)
            result = await session.call_tool("urgent_call", {"caller": "은행"})
            print(result.content[0].text)
            print()

            await asyncio.sleep(1)

            # 7. deep_thinking 테스트
            print("7️⃣ deep_thinking 테스트")
            print("-" * 60)
            result = await session.call_tool("deep_thinking", {"topic": "시스템 설계"})
            print(result.content[0].text)
            print()

            await asyncio.sleep(1)

            # 8. email_organizing 테스트
            print("8️⃣ email_organizing 테스트")
            print("-" * 60)
            result = await session.call_tool("email_organizing", {"folder": "스팸함"})
            print(result.content[0].text)
            print()

            await asyncio.sleep(1)

            # 9. virtual_chimek 테스트 (가산점)
            print("9️⃣ virtual_chimek 테스트 🍗🍺 (가산점)")
            print("-" * 60)
            result = await session.call_tool("virtual_chimek", {"participants": 4})
            print(result.content[0].text)
            print()

            await asyncio.sleep(1)

            # 10. emergency_leave 테스트 (가산점)
            print("🔟 emergency_leave 테스트 🏃💨 (가산점)")
            print("-" * 60)
            result = await session.call_tool("emergency_leave", {"reason": "가족 일"})
            print(result.content[0].text)
            print()

            print("="*60)
            print("✅ 모든 도구 테스트 완료! (기본 8개 + 가산점 2개)")
            print("="*60)


if __name__ == "__main__":
    asyncio.run(test_chillmcp())
