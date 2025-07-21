#!/usr/bin/env python3
"""
Simple MCP Server - Minimal Working Version
"""

import asyncio
import json
import logging
from typing import Any, Dict

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolResult,
    ListToolsResult,
    Tool,
    TextContent,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server instance
server = Server("simple-calculator")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """Handle list_tools requests."""
    tools = [
        Tool(
            name="add",
            description="Add two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number", 
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"]
            }
        ),
        Tool(
            name="multiply",
            description="Multiply two numbers",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number"
                    },
                    "b": {
                        "type": "number", 
                        "description": "Second number"
                    }
                },
                "required": ["a", "b"]
            }
        )
    ]
    return ListToolsResult(tools=tools)

@server.call_tool()
async def handle_call_tool(name: str, arguments: Dict[str, Any]) -> CallToolResult:
    """Handle call_tool requests."""
    try:
        a = float(arguments.get("a", 0))
        b = float(arguments.get("b", 0))
        
        if name == "add":
            result = a + b
            message = f"Adding {a} + {b} = {result}"
        elif name == "multiply":
            result = a * b
            message = f"Multiplying {a} × {b} = {result}"
        else:
            message = f"Unknown tool: {name}"
            
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=message
                )
            ]
        )
    except Exception as e:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error: {str(e)}"
                )
            ]
        )

async def main():
    """Main function to run the MCP server."""
    logger.info("Starting Simple MCP Calculator Server...")
    
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main())
