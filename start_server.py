#!/usr/bin/env python3
"""
MCP Calculator Server Starter
Start the MCP server using the configuration file.
"""

import json
import subprocess
import sys
import os
from pathlib import Path

def load_config():
    """Load the MCP server configuration."""
    config_path = Path("mcp_config.json")
    if not config_path.exists():
        print("❌ Configuration file 'mcp_config.json' not found!")
        return None
    
    try:
        with open(config_path, 'r') as f:
            return json.load(f)
    except json.JSONDecodeError as e:
        print(f"❌ Error parsing configuration file: {e}")
        return None

def start_server(server_name="calculator"):
    """Start the MCP server based on configuration."""
    config = load_config()
    if not config:
        return False
    
    servers = config.get("mcpServers", {})
    if server_name not in servers:
        print(f"❌ Server '{server_name}' not found in configuration!")
        print(f"Available servers: {list(servers.keys())}")
        return False
    
    server_config = servers[server_name]
    command = server_config.get("command", "python")
    args = server_config.get("args", [])
    cwd = server_config.get("cwd", ".")
    
    print(f"🚀 Starting MCP server: {server_name}")
    print(f"📁 Working directory: {os.path.abspath(cwd)}")
    print(f"🔧 Command: {command} {' '.join(args)}")
    print("📊 Server info:")
    
    server_info = server_config.get("serverInfo", {})
    print(f"   • Name: {server_info.get('name', 'Unknown')}")
    print(f"   • Version: {server_info.get('version', 'Unknown')}")
    
    tools = server_config.get("tools", [])
    print(f"   • Tools available: {len(tools)}")
    for tool in tools:
        print(f"     - {tool['name']}: {tool['description']}")
    
    print("\n🎯 Starting server...")
    print("💡 To test the server, run: python test_calculator.py")
    print("🌐 For web interface, run: streamlit run streamlit_app.py")
    print("🛑 Press Ctrl+C to stop the server\n")
    
    try:
        # Change to the specified working directory
        if cwd != ".":
            os.chdir(cwd)
        
        # Start the server
        subprocess.run([command] + args)
        
    except KeyboardInterrupt:
        print("\n🛑 Server stopped by user")
        return True
    except FileNotFoundError:
        print(f"❌ Command '{command}' not found!")
        return False
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        return False

def main():
    """Main function."""
    print("🧮 MCP Calculator Server Starter")
    print("=" * 40)
    
    # Check for help argument
    if len(sys.argv) > 1 and sys.argv[1] in ["-h", "--help", "help"]:
        print("Usage: python start_server.py [server_name]")
        print("\nOptions:")
        print("  server_name    Name of the server to start (default: calculator)")
        print("  -h, --help     Show this help message")
        print("\nExamples:")
        print("  python start_server.py              # Start default calculator server")
        print("  python start_server.py calculator   # Start calculator server explicitly")
        return 0
    
    # Check if server name is provided as argument
    server_name = "calculator"
    if len(sys.argv) > 1:
        server_name = sys.argv[1]
    
    # Show configuration info first
    config = load_config()
    if config:
        servers = config.get("mcpServers", {})
        print(f"📋 Available servers in configuration:")
        for name, server_config in servers.items():
            info = server_config.get("serverInfo", {})
            print(f"   • {name}: {info.get('name', 'Unknown')} v{info.get('version', '?')}")
        print()
    
    # Start the specified server
    success = start_server(server_name)
    
    if success:
        print("✅ Server started successfully!")
    else:
        print("❌ Failed to start server!")
        return 1
    
    return 0

if __name__ == "__main__":
    exit(main())
