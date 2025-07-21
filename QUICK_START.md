# 🧮 MCP Calculator Server - Quick Start Guide

## 📁 Clean File Structure
```
📦 MCP Calculator Server
├── 🔧 calculator_server.py    # Main MCP server implementation  
├── ⚙️ mcp_config.json         # Server configuration (START HERE!)
├── 🚀 start_server.py         # Server launcher script
├── 🌐 streamlit_app.py        # Web UI interface
├── 🧪 test_calculator.py      # Test suite
├── 🎯 launch_demo.py          # Complete demo launcher
├── ⚡ quick_test.py           # Quick functionality test
├── 📋 requirements.txt        # Python dependencies
├── 📦 package.json            # Project metadata
└── 📖 README.md               # Detailed documentation
```

## 🚀 How to Start the Server

### 1️⃣ **From JSON Configuration** (RECOMMENDED)
```bash
python start_server.py
```
This uses the **`mcp_config.json`** file to start the server with proper configuration.

### 2️⃣ **Direct Server Start**
```bash
python calculator_server.py
```
Starts the server directly without configuration wrapper.

### 3️⃣ **With Web Interface**
```bash
streamlit run streamlit_app.py
```
Then click "🚀 Start MCP Server" in the web interface.

### 4️⃣ **Complete Demo**
```bash
python launch_demo.py
```
Runs tests first, then launches the web interface.

## 📋 Configuration File: `mcp_config.json`

This is the **main configuration file** that defines how to start your MCP server:

```json
{
  "mcpServers": {
    "calculator": {
      "command": "python",
      "args": ["calculator_server.py"],
      "cwd": ".",
      "description": "A simple calculator server",
      "serverInfo": {
        "name": "calculator-server", 
        "version": "1.0.0"
      },
      "tools": [
        {"name": "add", "description": "Add two numbers together"},
        {"name": "subtract", "description": "Subtract numbers"},
        {"name": "multiply", "description": "Multiply numbers"},
        {"name": "divide", "description": "Divide numbers"}
      ]
    }
  }
}
```

## 🎯 Quick Commands

| Command | Purpose |
|---------|---------|
| `python start_server.py` | Start server from config |
| `python test_calculator.py` | Run all tests |
| `streamlit run streamlit_app.py` | Launch web UI |
| `python launch_demo.py` | Full demo with browser |
| `python quick_test.py` | Quick functionality check |

## ✅ Verification

1. **Test the server**:
   ```bash
   python test_calculator.py
   ```
   Should show: `🎉 All tests completed! Calculator MCP Server is working perfectly!`

2. **Start web interface**:
   ```bash
   streamlit run streamlit_app.py
   ```
   Opens at: http://localhost:8501

3. **Check configuration**:
   ```bash
   python start_server.py --help
   ```

## 🎉 Success!

Your MCP Calculator Server is ready! Start with the **`mcp_config.json`** file and use `python start_server.py` to launch it properly configured.
