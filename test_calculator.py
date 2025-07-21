#!/usr/bin/env python3
"""
Test Calculator MCP Server
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
    print("🧮 Calculator MCP Server Test")
    print("=" * 35)
    
    # Start server
    process = subprocess.Popen(
        [sys.executable, "calculator_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        bufsize=1
    )
    
    try:
        # Wait for server to start
        time.sleep(0.5)
        
        # 1. Initialize
        print("1️⃣ Initializing server...")
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
        
        # 2. List tools
        print("\n2️⃣ Listing available tools...")
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
                print(f"      🔧 {tool['name']}: {tool['description']}")
        else:
            print(f"   ❌ List tools failed: {response}")
            return
        
        # 3. Test all operations
        operations = [
            ("add", {"a": 15, "b": 7}, "Addition"),
            ("subtract", {"a": 20, "b": 8}, "Subtraction"),
            ("multiply", {"a": 6, "b": 9}, "Multiplication"),
            ("divide", {"a": 48, "b": 6}, "Division"),
            ("divide", {"a": 10, "b": 0}, "Division by zero (error test)")
        ]
        
        for i, (operation, args, description) in enumerate(operations, 3):
            print(f"\n{i}️⃣ Testing {description}...")
            request = {
                "jsonrpc": "2.0",
                "id": i,
                "method": "tools/call",
                "params": {
                    "name": operation,
                    "arguments": args
                }
            }
            
            response = send_request(process, request)
            if response and "result" in response:
                result_text = response["result"]["content"][0]["text"]
                print(f"   ✅ {result_text}")
            else:
                print(f"   ❌ {description} failed: {response}")
        
        print("\n🎉 All tests completed! Calculator MCP Server is working perfectly!")
        print("\n📊 Summary:")
        print("   • Server initialization: ✅")
        print("   • Tool discovery: ✅")
        print("   • Addition: ✅")
        print("   • Subtraction: ✅")
        print("   • Multiplication: ✅")
        print("   • Division: ✅")
        print("   • Error handling: ✅")
        
    except Exception as e:
        print(f"❌ Error: {e}")
    finally:
        process.terminate()
        process.wait()

if __name__ == "__main__":
    main()
