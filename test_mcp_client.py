import asyncio
import json
import logging
from contextlib import AsyncExitStack

from mcp import ClientSession
from mcp.client.streamable_http import streamablehttp_client

# Configure logging
logging.basicConfig(
    level=logging.INFO, format="%(asctime)s - %(levelname)s - %(message)s"
)


async def test_realentless_mcp():
    """Test the Realentless MCP endpoint using the official MCP SDK."""
    
    print("Testing Realentless MCP Endpoint with Official SDK")
    print("=" * 60)
    
    # MCP endpoint URL
    url = "https://realentless-backend.vercel.app/api/mcp/generateLevels"
    
    async with AsyncExitStack() as exit_stack:
        try:
            # Create streamable HTTP transport
            transport = await exit_stack.enter_async_context(
                streamablehttp_client(url)
            )
            read, write, get_session_id = transport
            
            # Create client session
            session = await exit_stack.enter_async_context(
                ClientSession(read, write)
            )
            
            # Test 1: Initialize handshake
            print("\n1. Testing initialize...")
            try:
                await session.initialize()
                print("✅ Initialize successful")
            except Exception as e:
                print(f"❌ Initialize failed: {e}")
                return
            
            # Test 2: List tools
            print("\n2. Testing tools/list...")
            try:
                tools_response = await session.list_tools()
                print("✅ Tools list successful")
                print("Found tools:")
                for item in tools_response:
                    if isinstance(item, tuple) and item[0] == "tools":
                        for tool in item[1]:
                            print(f"  - {tool.name}: {tool.description}")
            except Exception as e:
                print(f"❌ Tools list failed: {e}")
            
            # Test 3: Call generateLevels tool
            print("\n3. Testing generateLevels tool call...")
            try:
                arguments = {
                    "userId": "6c7e2bee-9f6f-4831-b7bf-868274e52374",
                    "levels": [
                        {
                            "id": "level-1",
                            "title": {
                                "en": "Beginner Level",
                                "fr": "Niveau Débutant"
                            },
                            "subtitle": {
                                "en": "Start your fitness journey",
                                "fr": "Commencez votre parcours fitness"
                            },
                            "message": {
                                "en": "Welcome to your fitness journey!",
                                "fr": "Bienvenue dans votre parcours fitness !"
                            },
                            "position": 1,
                            "availableAt": "2024-01-01T00:00:00Z",
                            "userId": "6c7e2bee-9f6f-4831-b7bf-868274e52374",
                            "bodyExercisesPerRound": 5,
                            "bodyIntensity": 1,
                            "bodyMessage": {
                                "en": "Let's get moving!",
                                "fr": "Mettons-nous en mouvement !"
                            },
                            "bodyRounds": 3,
                            "mindIntensity": 1,
                            "mindMessage": {
                                "en": "Focus on your breathing",
                                "fr": "Concentrez-vous sur votre respiration"
                            },
                            "mindRounds": 2
                        }
                    ],
                    "exercises": [
                        {
                            "id": "exercise-1",
                            "exerciseId": "5d792951-af94-4d55-bea1-75907490e49a",
                            "type": "BODY",
                            "userLevelId": "level-1",
                            "title": "Push-ups",
                            "description": "Basic push-ups for beginners"
                        }
                    ]
                }
                
                result = await session.call_tool("generateLevels", arguments)
                print("✅ generateLevels tool call successful")
                print(f"Result: {json.dumps(result, indent=2)}")
                
            except Exception as e:
                print(f"❌ generateLevels tool call failed: {e}")
            
            # Test 4: Test invalid tool
            print("\n4. Testing invalid tool...")
            try:
                await session.call_tool("invalidTool", {})
                print("❌ Should have failed for invalid tool")
            except Exception as e:
                print(f"✅ Correctly failed for invalid tool: {e}")
            
        except Exception as e:
            print(f"❌ Session setup failed: {e}")
        finally:
            print("\n5. Cleaning up...")
            await exit_stack.aclose()
            print("✅ Cleanup complete")


if __name__ == "__main__":
    asyncio.run(test_realentless_mcp()) 