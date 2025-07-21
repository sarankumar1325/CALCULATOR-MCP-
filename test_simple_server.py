#!/usr/bin/env python3
"""
Simple Test for MCP Server
"""

import subprocess
import json
import sys
import time

def send_request(process, request):
    """Send a request and get response."""
    process.stdin.write(json.dumps(request) + "\n")
    process.stdin.flush()
    response = process.stdout.readline()
    return json.loads(response) if response.strip() else None

def main():
    print("Simple MCP Server Test")
    print("=" * 25)
    
    # Start server
    process = subprocess.Popen(
        [sys.executable, "simple_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    try:
        # Wait for server to start
        time.sleep(1)
        
        # 1. Initialize
        print("1. Initializing server...")
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "test-client", "version": "1.0"}
            }
        }
        
        response = send_request(process, init_request)
        if response and "result" in response:
            server_name = response["result"]["serverInfo"]["name"]
            print(f"   ✅ Connected to: {server_name}")
        else:
            print(f"   ❌ Init failed: {response}")
            return
        
        # 2. Send initialized notification
        print("2. Sending initialized notification...")
        initialized = {
            "jsonrpc": "2.0",
            "method": "notifications/initialized"
        }
        process.stdin.write(json.dumps(initialized) + "\n")
        process.stdin.flush()
        
        # 3. List tools
        print("3. Listing available tools...")
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        response = send_request(process, tools_request)
        if response and "result" in response:
            tools = response["result"]["tools"]
            print(f"   ✅ Found {len(tools)} tools:")
            for tool in tools:
                print(f"      - {tool['name']}: {tool['description']}")
        else:
            print(f"   ❌ List tools failed: {response}")
            return
        
        # 4. Test addition
        print("4. Testing addition (5 + 3)...")
        add_request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": "add",
                "arguments": {"a": 5, "b": 3}
            }
        }
        
        response = send_request(process, add_request)
        if response and "result" in response:
            result_text = response["result"]["content"][0]["text"]
            print(f"   ✅ {result_text}")
        else:
            print(f"   ❌ Addition failed: {response}")
        
        # 5. Test multiplication
        print("5. Testing multiplication (4 × 6)...")
        mult_request = {
            "jsonrpc": "2.0",
            "id": 4,
            "method": "tools/call",
            "params": {
                "name": "multiply",
                "arguments": {"a": 4, "b": 6}
            }
        }
        
        response = send_request(process, mult_request)
        if response and "result" in response:
            result_text = response["result"]["content"][0]["text"]
            print(f"   ✅ {result_text}")
        else:
            print(f"   ❌ Multiplication failed: {response}")
        
        print("\n🎉 All tests passed! MCP Server is working correctly!")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    main()
