#!/usr/bin/env python3
"""
Streamlit UI for MCP Calculator Server
A beautiful web interface to showcase the MCP server functionality.
"""

import streamlit as st
import subprocess
import json
import time
import threading
import queue
import sys
from pathlib import Path

class MCPClient:
    def __init__(self):
        self.process = None
        self.connected = False
        
    def start_server(self):
        """Start the MCP calculator server."""
        try:
            self.process = subprocess.Popen(
                [sys.executable, "calculator_server.py"],
                stdin=subprocess.PIPE,
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                bufsize=1
            )
            time.sleep(0.5)  # Wait for server to start
            return True
        except Exception as e:
            st.error(f"Failed to start server: {e}")
            return False
    
    def send_request(self, request):
        """Send a request to the MCP server and get response."""
        if not self.process:
            return None
            
        try:
            self.process.stdin.write(json.dumps(request) + "\n")
            self.process.stdin.flush()
            response = self.process.stdout.readline()
            return json.loads(response) if response.strip() else None
        except Exception as e:
            st.error(f"Communication error: {e}")
            return None
    
    def initialize(self):
        """Initialize the MCP server."""
        init_request = {
            "jsonrpc": "2.0",
            "id": 1,
            "method": "initialize",
            "params": {
                "protocolVersion": "2024-11-05",
                "capabilities": {},
                "clientInfo": {"name": "streamlit-client", "version": "1.0"}
            }
        }
        
        response = self.send_request(init_request)
        if response and "result" in response:
            self.connected = True
            return response["result"]["serverInfo"]
        return None
    
    def list_tools(self):
        """Get available tools from the server."""
        tools_request = {
            "jsonrpc": "2.0",
            "id": 2,
            "method": "tools/list"
        }
        
        response = self.send_request(tools_request)
        if response and "result" in response:
            return response["result"]["tools"]
        return []
    
    def call_tool(self, tool_name, arguments):
        """Call a specific tool with arguments."""
        request = {
            "jsonrpc": "2.0",
            "id": 3,
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        response = self.send_request(request)
        if response and "result" in response:
            return response["result"]["content"][0]["text"]
        elif response and "error" in response:
            return f"Error: {response['error']['message']}"
        return "No response received"
    
    def close(self):
        """Close the server connection."""
        if self.process:
            self.process.terminate()
            self.process.wait()
            self.process = None
            self.connected = False

def main():
    """Main Streamlit application."""
    st.set_page_config(
        page_title="MCP Calculator Server Demo",
        page_icon="🧮",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Custom CSS for better styling
    st.markdown("""
    <style>
    .main-header {
        font-size: 3rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .tool-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        border-left: 4px solid #1f77b4;
    }
    .result-box {
        background-color: #d4edda;
        color: #155724;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #c3e6cb;
        margin: 1rem 0;
    }
    .error-box {
        background-color: #f8d7da;
        color: #721c24;
        padding: 1rem;
        border-radius: 0.5rem;
        border: 1px solid #f5c6cb;
        margin: 1rem 0;
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Main header
    st.markdown('<h1 class="main-header">🧮 MCP Calculator Server Demo</h1>', unsafe_allow_html=True)
    
    # Initialize session state
    if 'client' not in st.session_state:
        st.session_state.client = MCPClient()
        st.session_state.server_info = None
        st.session_state.tools = []
    
    # Sidebar
    with st.sidebar:
        st.markdown("## 🔧 Server Control")
        
        if st.button("🚀 Start MCP Server", type="primary"):
            with st.spinner("Starting MCP server..."):
                if st.session_state.client.start_server():
                    server_info = st.session_state.client.initialize()
                    if server_info:
                        st.session_state.server_info = server_info
                        st.session_state.tools = st.session_state.client.list_tools()
                        st.success("✅ Server started successfully!")
                        st.rerun()
                    else:
                        st.error("❌ Failed to initialize server")
                else:
                    st.error("❌ Failed to start server")
        
        if st.button("🛑 Stop Server"):
            st.session_state.client.close()
            st.session_state.server_info = None
            st.session_state.tools = []
            st.success("✅ Server stopped")
            st.rerun()
        
        # Server status
        st.markdown("## 📊 Server Status")
        if st.session_state.client.connected:
            st.success("🟢 Connected")
            if st.session_state.server_info:
                st.info(f"**Name:** {st.session_state.server_info['name']}")
                st.info(f"**Version:** {st.session_state.server_info['version']}")
        else:
            st.error("🔴 Disconnected")
        
        # About section
        st.markdown("## 📖 About")
        st.markdown("""
        This demo showcases a **Model Context Protocol (MCP)** server that provides
        calculator functionality. The server implements the MCP specification and
        communicates via JSON-RPC over stdio.
        
        **Features:**
        - ➕ Addition
        - ➖ Subtraction  
        - ✖️ Multiplication
        - ➗ Division
        - 🛡️ Error handling
        """)
    
    # Main content
    if not st.session_state.client.connected:
        st.markdown("""
        ## 👋 Welcome to the MCP Calculator Demo!
        
        This application demonstrates a **Model Context Protocol (MCP)** server in action.
        The MCP server provides calculator tools that can be discovered and used through
        the standardized MCP protocol.
        
        **To get started:**
        1. Click "🚀 Start MCP Server" in the sidebar
        2. Once connected, you can use the calculator tools below
        3. Try different operations and see the results in real-time
        
        ### 🏗️ Architecture
        - **Server**: Pure Python MCP implementation with async/await
        - **Protocol**: JSON-RPC 2.0 over stdio transport
        - **Tools**: Dynamic tool discovery and execution
        - **UI**: Streamlit web interface for easy interaction
        """)
        
        # Show code preview
        with st.expander("👀 Peek at the Server Code"):
            st.code('''
# MCP Server Example
async def handle_request(self, request):
    method = request.get("method")
    
    if method == "tools/list":
        return {
            "jsonrpc": "2.0",
            "id": request["id"],
            "result": {"tools": self.get_available_tools()}
        }
    
    elif method == "tools/call":
        tool_name = request["params"]["name"]
        args = request["params"]["arguments"]
        result = await self.execute_tool(tool_name, args)
        return {"jsonrpc": "2.0", "id": request["id"], "result": result}
            ''', language='python')
    
    else:
        # Server is connected, show calculator interface
        st.markdown("## 🔧 Available Tools")
        
        # Display available tools
        if st.session_state.tools:
            cols = st.columns(2)
            for i, tool in enumerate(st.session_state.tools):
                with cols[i % 2]:
                    st.markdown(f"""
                    <div class="tool-card">
                        <h4>🔧 {tool['name'].title()}</h4>
                        <p>{tool['description']}</p>
                    </div>
                    """, unsafe_allow_html=True)
        
        st.markdown("## 🧮 Calculator Interface")
        
        # Calculator interface
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### Input")
            num1 = st.number_input("First Number", value=10.0, step=1.0, format="%.2f")
            num2 = st.number_input("Second Number", value=5.0, step=1.0, format="%.2f")
            
            operation = st.selectbox(
                "Operation",
                ["add", "subtract", "multiply", "divide"],
                format_func=lambda x: {
                    "add": "➕ Addition",
                    "subtract": "➖ Subtraction", 
                    "multiply": "✖️ Multiplication",
                    "divide": "➗ Division"
                }[x]
            )
        
        with col2:
            st.markdown("### Result")
            if st.button("🚀 Calculate", type="primary", use_container_width=True):
                with st.spinner("Calculating..."):
                    result = st.session_state.client.call_tool(
                        operation,
                        {"a": num1, "b": num2}
                    )
                    
                    if "Error" in result:
                        st.markdown(f'<div class="error-box">❌ {result}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="result-box">✅ {result}</div>', unsafe_allow_html=True)
        
        # Quick calculations section
        st.markdown("## ⚡ Quick Calculations")
        
        quick_ops = [
            ("100 + 50", "add", 100, 50),
            ("75 - 25", "subtract", 75, 25),
            ("12 × 8", "multiply", 12, 8),
            ("144 ÷ 12", "divide", 144, 12)
        ]
        
        cols = st.columns(4)
        for i, (label, op, a, b) in enumerate(quick_ops):
            with cols[i]:
                if st.button(label, use_container_width=True):
                    result = st.session_state.client.call_tool(op, {"a": a, "b": b})
                    st.success(result)
        
        # Real-time server communication log
        with st.expander("📋 Communication Log"):
            st.markdown("""
            **Recent MCP Protocol Messages:**
            - `initialize` → Server connection established
            - `tools/list` → Discovered 4 calculator tools
            - `tools/call` → Ready to execute calculations
            
            *This would show actual JSON-RPC messages in a production system*
            """)
    
    # Cleanup on session end
    if hasattr(st.session_state, 'client') and st.session_state.client.connected:
        # This will be called when the session ends
        pass

if __name__ == "__main__":
    main()
