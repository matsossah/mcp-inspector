import asyncio
import httpx
import json

async def test_production_endpoint():
    # Replace with your actual production URL
    url = "https://realentless-backend.vercel.app/api/mcp/generateLevels"
    
    print("Testing MCP Production Endpoint")
    print("=" * 50)
    
    async with httpx.AsyncClient() as client:
        
        # Test 1: Initialize handshake
        print("\n1. Testing initialize...")
        initialize_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2025-03-26",
                "capabilities": {},
                "clientInfo": {
                    "name": "test-client",
                    "version": "1.0.0"
                }
            }
        }
        
        try:
            response = await client.post(url, json=initialize_request)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test 2: Tools/list
        print("\n2. Testing tools/list...")
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list",
            "params": {}
        }
        
        try:
            response = await client.post(url, json=tools_request)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test 3: Notifications/initialized
        print("\n3. Testing notifications/initialized...")
        notifications_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "notifications/initialized",
            "params": {}
        }
        
        try:
            response = await client.post(url, json=notifications_request)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test 4: GenerateLevels tool call
        print("\n4. Testing generateLevels tool call...")
        generate_levels_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "generateLevels",
            "params": {
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
        }
        
        try:
            response = await client.post(url, json=generate_levels_request)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test 5: Invalid method
        print("\n5. Testing invalid method...")
        invalid_request = {
            "jsonrpc": "2.0",
            "id": 5,
            "method": "invalidMethod",
            "params": {}
        }
        
        try:
            response = await client.post(url, json=invalid_request)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"Error: {e}")
        
        # Test 6: Invalid JSON-RPC (missing id)
        print("\n6. Testing invalid JSON-RPC (missing id)...")
        invalid_jsonrpc_request = {
            "jsonrpc": "2.0",
            "method": "initialize",
            "params": {}
        }
        
        try:
            response = await client.post(url, json=invalid_jsonrpc_request)
            print(f"Status: {response.status_code}")
            print(f"Response: {json.dumps(response.json(), indent=2)}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(test_production_endpoint())