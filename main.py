import httpx
from typing import Any
from mcp.server.fastmcp import FastMCP

# Create an MCP server
mcp = FastMCP("Realentless MCP")

# Backend URL
BACKEND_URL = "https://realentless-backend.vercel.app/api/mcp/generateLevels"


@mcp.tool()
async def generateLevels(
    userId: str,
    levels: list[dict[str, Any]],
    exercises: list[dict[str, Any]]
) -> dict[str, Any]:
    """
    Generate personalized levels and exercises for a user.
    
    Args:
        userId: The user's unique ID
        levels: Array of level objects with multilingual titles, messages, and workout configuration
        exercises: Array of exercise objects. The exerciseId must reference a valid exercise from the available exercises provided in the context.
    
    Returns:
        Success message with created levels and exercises count
    """
    # Prepare the request payload
    payload = {
        "jsonrpc": "2.0",
        "id": 1,
        "method": "generateLevels",
        "params": {
            "userId": userId,
            "levels": levels,
            "exercises": exercises
        }
    }
    
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(BACKEND_URL, json=payload)
            response.raise_for_status()
            
            result = response.json()
            
            # Check if it's a successful response
            if "result" in result:
                return result["result"]
            elif "error" in result:
                raise ValueError(f"Backend error: {result['error']}")
            else:
                raise ValueError(f"Unexpected response format: {result}")
                
    except httpx.HTTPStatusError as e:
        raise ValueError(f"HTTP error {e.response.status_code}: {e.response.text}")
    except Exception as e:
        raise ValueError(f"Request failed: {str(e)}")


if __name__ == "__main__":
    mcp.run() 