#!/usr/bin/env python3
"""Simple MCP server for testing."""

from mcp.server import Server
from mcp.server.models import InitializationOptions
import mcp.types as types

# Create the server
server = Server("test-server")

@server.list_tools()
async def handle_list_tools() -> list[types.Tool]:
    """List available tools."""
    return [
        types.Tool(
            name="echo",
            description="Echo back the input",
            inputSchema={
                "type": "object",
                "properties": {
                    "message": {
                        "type": "string",
                        "description": "Message to echo back"
                    }
                },
                "required": ["message"]
            }
        )
    ]

@server.call_tool()
async def handle_call_tool(name: str, arguments: dict) -> list[types.TextContent]:
    """Handle tool calls."""
    if name == "echo":
        message = arguments.get("message", "")
        return [types.TextContent(type="text", text=f"Echo: {message}")]
    
    raise ValueError(f"Unknown tool: {name}")

# Expose the server object as 'mcp' for development mode
mcp = server 