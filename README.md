# FinSight: AI-Powered Financial Analyst 📈

FinSight is an autonomous financial analysis agent that integrates directly into your IDE via the Model Context Protocol (MCP). Built with **CrewAI** and **Deepseek-R1**, it analyzes stock market data, fetches historical prices, and provides intelligent financial insights right where you work.

Instead of switching back and forth between financial websites and your code, you can just ask your IDE to analyze stock performance, compare companies, and interpret market trends.

## 🚀 Features
- **Local AI Execution**: Uses Deepseek-R1 via Ollama to keep your analysis private and local.
- **Multi-Agent Orchestration**: Powered by CrewAI to break down complex financial queries into specialized agent tasks.
- **IDE Integration**: Runs natively as an MCP server in Cursor or any compatible IDE.
- **Real-Time Data**: Fetches stock prices, volume, and trends using `yfinance`.

---

## 🛠️ Getting Started

### 1. Prerequisites
- **Python 3.11+**
- **Docker** (Required by CrewAI for secure code execution)
- **Ollama** (For running Deepseek-R1 locally)

### 2. Install & Run Ollama
You'll need Ollama running in the background with the Deepseek-R1 model:
```bash
ollama run deepseek-r1
```

### 3. Install Dependencies
This project uses `uv` for fast dependency management.
```bash
uv sync --python 3.11
```

### 4. Connect to Your IDE (Cursor)
To use FinSight directly from your IDE, you need to add it as an MCP server.

1. Open your IDE settings and navigate to **MCP**.
2. Add a new global MCP server with the following configuration:

```json
{
    "mcpServers": {
        "financial-analyst": {
            "command": "uv",
            "args": [
                "--directory",
                "C:/absolute/path/to/FinSight",
                "run",
                "server.py"
            ]
        }
    }
}
```
3. Restart or reload the MCP server in your IDE.

---

## 💡 How to Use It
Once connected, you can chat with your IDE and ask financial questions like:
- *"Show me Tesla's stock performance over the last 3 months."*
- *"Compare Apple and Microsoft stocks for the past year."*
- *"Analyze the trading volume of Amazon stock for the last month."*

The AI will spin up the necessary CrewAI agents, fetch the data, and deliver a comprehensive analysis!

## 🤝 Contributing
Feel free to open issues or submit pull requests if you want to improve FinSight!
