#!/usr/bin/env python3
"""
Launch script to test the complete MCP Calculator Demo
"""

import subprocess
import time
import webbrowser
import sys
import os

def test_server():
    """Test the MCP server functionality."""
    print("🧪 Testing MCP Server...")
    result = subprocess.run([sys.executable, "test_calculator.py"], capture_output=True, text=True)
    
    if result.returncode == 0:
        print("✅ MCP Server test passed!")
        return True
    else:
        print("❌ MCP Server test failed!")
        print(result.stdout)
        print(result.stderr)
        return False

def launch_streamlit():
    """Launch the Streamlit app."""
    print("🚀 Launching Streamlit app...")
    
    # Start Streamlit in background
    process = subprocess.Popen(
        [sys.executable, "-m", "streamlit", "run", "streamlit_app.py", "--server.headless", "true"],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for server to start
    time.sleep(3)
    
    # Open browser
    print("🌐 Opening browser...")
    webbrowser.open("http://localhost:8501")
    
    return process

def main():
    """Main launch function."""
    print("🧮 MCP Calculator Demo Launcher")
    print("=" * 40)
    
    # Change to project directory
    project_dir = os.path.dirname(os.path.abspath(__file__))
    os.chdir(project_dir)
    
    # Test server first
    if not test_server():
        print("❌ Server test failed. Please check the setup.")
        return
    
    # Launch Streamlit
    streamlit_process = launch_streamlit()
    
    print("\n🎉 Demo is ready!")
    print("📋 What to do next:")
    print("   1. The web interface should open in your browser")
    print("   2. Click '🚀 Start MCP Server' in the sidebar")
    print("   3. Try the calculator operations")
    print("   4. Press Ctrl+C here to stop the demo")
    
    try:
        # Keep the script running
        streamlit_process.wait()
    except KeyboardInterrupt:
        print("\n🛑 Stopping demo...")
        streamlit_process.terminate()
        streamlit_process.wait()
        print("✅ Demo stopped successfully!")

if __name__ == "__main__":
    main()
