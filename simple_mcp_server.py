#!/usr/bin/env python3
"""
Simple MCP Server with Addition Tool
A basic MCP server that provides an addition operation tool.
"""

import asyncio
import json
import logging
from typing import Any, Dict, List, Optional

from mcp.server import Server
from mcp.server.models import InitializationOptions
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolRequest,
    CallToolResult,
    ListToolsRequest,
    ListToolsResult,
    Tool,
    TextContent,
)

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create MCP server instance
server = Server("simple-mcp-server")

@server.list_tools()
async def handle_list_tools() -> ListToolsResult:
    """Handle list_tools requests."""
    tools = [
        Tool(
            name="addition",
            description="Adds two numbers together",
            inputSchema={
                "type": "object",
                "properties": {
                    "a": {
                        "type": "number",
                        "description": "First number to add"
                    },
                    "b": {
                        "type": "number", 
                        "description": "Second number to add"
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
    if name == "addition":
        try:
            a = arguments.get("a")
            b = arguments.get("b")
            
            if a is None or b is None:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text="Error: Both 'a' and 'b' parameters are required"
                    )
                ]
            )
            
            # Convert to float to handle both integers and decimals
            result = float(a) + float(b)
            
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"The sum of {a} and {b} is: {result}"
                    )
                ]
            )
        except (ValueError, TypeError) as e:
            return CallToolResult(
                content=[
                    TextContent(
                        type="text",
                        text=f"Error: Invalid input. Please provide valid numbers. {str(e)}"
                    )
                ]
            )
    else:
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=f"Error: Unknown tool '{name}'"
                )
            ]
        )

async def main():
    """Main function to run the MCP server."""
    logger.info("Starting Simple MCP Server...")
    
    # Run the server using stdio transport
    async with stdio_server() as (read_stream, write_stream):
        await server.run(
            read_stream,
            write_stream,
            server.create_initialization_options()
        )

if __name__ == "__main__":
    asyncio.run(main()) 