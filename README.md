# CrewAI MCP Demo

This repository contains a demo of how to use the CrewAI MCP adapter to interact with the MCP Servers.

## Prerequisites

- Python >= 3.12 < 3.13
- OPENAI API Key or an API key from another LLM provider

## Installation

```bash
python -m venv .venv
source .venv/bin/activate
uv pip install 'crewai-tools[mcp]'
```

## Usage

1. Add API key to `.env`:
```.env
MODEL=openai/gpt-4o-mini # or any model provider/model
OPENAI_API_KEY=sk-proj-***
```

2. Run the SSE demo
```bash
python sse_client_demo.py
```

3. Run the StdIO demo
```bash
python stdio_client_demo.py
```    

More details in [CrewAI Docs](https://docs.crewai.com/mcp/crewai-mcp-integration/)
