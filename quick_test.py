#!/usr/bin/env python3
"""
Quick Test for MCP Server
"""

import subprocess
import json
import sys
import time

def main():
    print("Quick MCP Server Test")
    print("=" * 20)
    
    # Start server
    process = subprocess.Popen(
        [sys.executable, "simple_mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    try:
        # Wait a moment for server to start
        time.sleep(0.5)
        
        # Send initialization
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test", "version": "1.0"}
            }
        }
        
        print("Sending init request...")
        process.stdin.write(json.dumps(init_request) + "\n")
        process.stdin.flush()

        # Read response with timeout
        response = process.stdout.readline()
        print(f"Response: {response.strip()}")
        
        # Send initialized notification (required by MCP protocol)
        initialized_notification = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        
        print("Sending initialized notification...")
        process.stdin.write(json.dumps(initialized_notification) + "\n")
        process.stdin.flush()

        # Send list tools request
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        print("Sending tools list request...")
        process.stdin.write(json.dumps(tools_request) + "\n")
        process.stdin.flush()
        
        response = process.stdout.readline()
        print(f"Tools response: {response.strip()}")
        
        # Test addition
        add_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "addition",
                "arguments": {"a": 10, "b": 5}
            }
        }
        
        print("Testing addition (10 + 5)...")
        process.stdin.write(json.dumps(add_request) + "\n")
        process.stdin.flush()
        
        response = process.stdout.readline()
        print(f"Addition result: {response.strip()}")
        
        print("✅ Test completed successfully!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    main() 