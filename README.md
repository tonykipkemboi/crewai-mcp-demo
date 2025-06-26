# CrewAI MCP Demo

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![CrewAI](https://img.shields.io/badge/CrewAI-0.134.0%2B-green)](https://github.com/crewai/crewai)

This repository demonstrates **two approaches** for using CrewAI with MCP (Model Context Protocol) to interact with external tools and services through a standardized protocol.

## 📋 Table of Contents

- [Overview](#overview)
- [Two Approaches](#two-approaches)
- [Prerequisites](#prerequisites)
- [Quick Start](#quick-start)
- [Scaffolding Approach - CrewAI Project](#scaffolding-approach---crewai-project)
- [Script Approach - Standalone Demos](#script-approach---standalone-demos)
- [Transport Mechanisms](#transport-mechanisms)
- [Project Structure](#project-structure)
- [Advanced Usage](#advanced-usage)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Overview

The Model Context Protocol (MCP) provides a standardized way for AI agents to interact with external tools and services. This demo showcases how to use CrewAI with MCP servers to build powerful AI applications that can leverage external capabilities.

**Transport mechanisms supported:**
- **Streamable HTTP** - For remote hosted servers (e.g., Context7)
- **Server-Sent Events (SSE)** - For real-time server-to-client communication
- **Standard Input/Output (StdIO)** - For local process communication

## 🚀 Two Approaches

This repository demonstrates **two different ways** to integrate CrewAI with MCP:

### 1. 🏗️ **Scaffolding Approach** (Recommended for Production)
- Uses CrewAI's project scaffolding with `@CrewBase` decorator
- Structured project with configuration files
- Built-in `get_mcp_tools()` method (CrewAI 0.134.0+)
- Better for complex, maintainable applications
- **Examples:** `scaffolding_approach_examples/` directory

### 2. 📝 **Script Approach** (Great for Learning/Prototyping)
- Standalone Python scripts using `MCPServerAdapter` directly
- Quick to set up and experiment with
- Perfect for understanding MCP concepts
- **Examples:** `*_client_demo.py` files in `script_approach_examples/` directory

## 🛠️ Prerequisites

- **Python**: Version >= 3.10 < 3.14
- **CrewAI**: Version >= 0.134.0 (for scaffolding approach)
- **API Key**: OpenAI API Key or another LLM provider
- **uv** (recommended) or pip for package management

## ⚡ Quick Start

### Option 1: Try the Scaffolding Approach (Mathematician Project)

1. **Clone and setup:**
   ```bash
   git clone https://github.com/tonykipkemboi/crewai-mcp-demo.git
   cd crewai-mcp-demo/scaffolding_approach_examples/mathematician_project
   ```

2. **Create environment and install:**
   ```bash
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   uv pip install -e .
   ```

3. **Set up environment:**
   ```bash
   # Create .env file with your API key
   echo "OPENAI_API_KEY=sk-your-openai-api-key-here" > .env
   ```

4. **Run the mathematician crew:**
   ```bash
   crewai run
   ```

### Option 2: Try the Script Approach

1. **Clone and setup:**
   ```bash
   git clone https://github.com/tonykipkemboi/crewai-mcp-demo.git
   cd crewai-mcp-demo
   ```

2. **Install dependencies:**
   ```bash
   uv pip install 'crewai-tools[mcp]'
   ```

3. **Run a demo:**
   ```bash
   # For math operations (local server)
   python3 script_approach_examples/stdio_client_demo.py
   
   # For Cloudflare docs (remote server)
   python3 script_approach_examples/sse_client_demo.py
   ```

## 🏗️ Scaffolding Approach - CrewAI Project

The scaffolding approach uses CrewAI's project structure with the `@CrewBase` decorator and built-in MCP support.

### Project Structure
```
mathematician_project/
├── src/mathematician_project/
│   ├── crew.py              # Main crew definition with @CrewBase
│   │   ├── crew.py              # Main crew definition with @CrewBase
│   │   └── main.py              # Entry point
│   │   ├── config/
│   │   │   ├── agents.yaml      # Agent configurations
│   │   │   └── tasks.yaml       # Task configurations
│   │   └── tools/
│   │       └── custom_tool.py   # Custom tools (optional)
│   ├── pyproject.toml           # Dependencies and project config
│   └── README.md
```

### Key Features

#### 1. Using `@CrewBase` Decorator
```python
from crewai.project import CrewBase, agent, crew, task

@CrewBase
class MathematicianProject():
    # MCP server configuration
    mcp_server_params = {
        "url": "https://api.context7.ai/mcp", 
        "transport": "streamable-http"
    }
    
    @agent
    def mathematician(self) -> Agent:
        return Agent(
            config=self.agents_config['mathematician'],
            tools=self.get_mcp_tools()  # Built-in method!
        )
```

#### 2. Built-in `get_mcp_tools()` Method
CrewAI 0.134.0+ includes a built-in `get_mcp_tools()` method:

```python
# Get all available tools
tools=self.get_mcp_tools()

# Get specific tools only
tools=self.get_mcp_tools("tool_name_1", "tool_name_2")
```

#### 3. MCP Server Configuration Options

**For Remote Servers (Streamable HTTP):**
```python
mcp_server_params = {
    "url": "https://api.context7.ai/mcp", 
    "transport": "streamable-http"
}
```

**For Local Servers (StdIO):**
```python
from mcp import StdioServerParameters

mcp_server_params = StdioServerParameters(
    command="python3",
    args=["path/to/server.py"],
    env={"UV_PYTHON": "3.12", **os.environ}
)
```

**For Multiple Servers:**
```python
mcp_server_params = [
    {"url": "https://api.context7.ai/mcp", "transport": "streamable-http"},
    {"url": "https://docs.mcp.cloudflare.com/sse"},
    StdioServerParameters(command="python3", args=["local_server.py"])
]
```

### Creating a New Scaffolded Project

```bash
# Create new CrewAI project with MCP support
crewai create my_mcp_project
cd my_mcp_project

# Update pyproject.toml dependencies
# Add: "crewai[tools]>=0.134.0,<1.0.0"
# Add: "crewai-tools[mcp]>=0.47.1"

# Install dependencies
uv pip install -e .
```

### Example: Context7 Integration Demo

The `scaffolding_approach_examples/crewai_context7_mcp/` project demonstrates using Context7's hosted MCP server:

```python
# scaffolding_approach_examples/crewai_context7_mcp/src/crewai_context7_mcp/crew.py
@CrewBase
class CrewaiContext7Mcp():
    mcp_server_params = {
        "url": f"https://server.smithery.ai/@upstash/context7-mcp/mcp?api_key={os.getenv('SMITHERY_API_KEY')}",
        "transport": "streamable-http",
    }
    
    @agent
    def researcher(self) -> Agent:
        return Agent(
            config=self.agents_config['researcher'],
            tools=self.get_mcp_tools()  # All available tools
        )
    
    @agent
    def answer_generator(self) -> Agent:
        return Agent(
            config=self.agents_config['answer_generator'],
            tools=self.get_mcp_tools("get-library-docs")  # Filtered tools
        )
```

**To run the Context7 demo:**
```bash
cd scaffolding_approach_examples/crewai_context7_mcp
cp .env.example .env
# Add your SMITHERY_API_KEY to .env
uv pip install -e .
crewai run
```

## 📝 Script Approach - Standalone Demos

The script approach uses standalone Python files with `MCPServerAdapter` directly.

### Available Demos

| Demo | Description | Transport | Server Type |
|------|-------------|-----------|-------------|
| `stdio_client_demo.py` | Math operations | StdIO | Local math server |
| `sse_client_demo.py` | Cloudflare docs search | SSE | Remote Cloudflare server |
| `streamable_http_client_demo.py` | Simple greeting | HTTP | Local hello server |
| `multiple_servers_client_demo.py` | Combined functionality | All | Multiple servers |

### Script Pattern
```python
from crewai import Agent, Task, Crew
from crewai_tools import MCPServerAdapter

# Configure MCP server
server_params = {
    "url": "https://api.example.com/mcp",
    "transport": "streamable-http"
}

# Use MCP tools with context manager
with MCPServerAdapter(server_params) as tools:
    agent = Agent(
        role="Your Agent Role",
        goal="Your agent's goal",
        tools=tools,  # Direct tools usage
        verbose=True
    )
    
    task = Task(
        description="Your task description",
        agent=agent,
        expected_output="Expected output format"
    )
    
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff()
```

### Running Script Demos

1. **Math Operations (StdIO):**
   ```bash
   python3 script_approach_examples/stdio_client_demo.py
   ```

2. **Cloudflare Docs Search (SSE):**
   ```bash
   python3 script_approach_examples/sse_client_demo.py
   ```

3. **Hello World (HTTP):**
   ```bash
   # Terminal 1: Start server
   python3 servers/hello_http_server.py
   
   # Terminal 2: Run client
   python3 script_approach_examples/streamable_http_client_demo.py
   ```

## 🔄 Transport Mechanisms

### 1. Streamable HTTP ⭐ (Recommended)
- **Use case**: Remote hosted servers (Context7, cloud services)
- **Benefits**: Simple setup, bidirectional communication, web-friendly
- **Example**: Context7 API, custom cloud MCP servers

```python
server_params = {
    "url": "https://api.context7.ai/mcp",
    "transport": "streamable-http"
}
```

### 2. Server-Sent Events (SSE)
- **Use case**: Real-time server-to-client updates
- **Benefits**: Good for streaming responses, widely supported
- **Example**: Cloudflare docs, real-time data feeds

```python
server_params = {
    "url": "https://docs.mcp.cloudflare.com/sse"
}
```

### 3. Standard Input/Output (StdIO)
- **Use case**: Local development, testing, process-based servers
- **Benefits**: Simple local setup, no network required
- **Example**: Local math server, file processing tools

```python
from mcp import StdioServerParameters

server_params = StdioServerParameters(
    command="python3",
    args=["servers/math_stdio_server.py"],
    env={"UV_PYTHON": "3.12", **os.environ}
)
```

## 📁 Project Structure

```
crewai-mcp-demo/
├── 🏗️ scaffolding_approach_examples/
│   ├── mathematician_project/         # Math operations via local StdIO server
│   │   ├── src/mathematician_project/
│   │   │   ├── crew.py               # @CrewBase with get_mcp_tools()
│   │   │   ├── main.py               # Entry point
│   │   │   ├── config/
│   │   │   │   ├── agents.yaml       # Agent configurations
│   │   │   │   └── tasks.yaml        # Task configurations
│   │   │   └── tools/custom_tool.py  # Custom tools
│   │   ├── pyproject.toml            # Project dependencies
│   │   └── README.md                 # Project-specific docs
│   └── crewai_context7_mcp/          # Context7 integration via streamable-HTTP
│       ├── src/crewai_context7_mcp/
│       │   ├── crew.py               # Context7 MCP integration
│       │   ├── main.py               # Entry point
│       │   ├── config/
│       │   │   ├── agents.yaml       # Agent configurations
│       │   │   └── tasks.yaml        # Task configurations
│       │   └── tools/custom_tool.py  # Custom tools
│       ├── pyproject.toml            # Project dependencies
│       ├── .env.example              # Environment variables template
│       └── README.md                 # Project-specific docs
├── 📝 script_approach_examples/       # Standalone script examples
│   ├── stdio_client_demo.py          # Math operations via StdIO
│   ├── sse_client_demo.py            # Cloudflare docs via SSE
│   ├── streamable_http_client_demo.py # Greeting via HTTP
│   └── multiple_servers_client_demo.py # Multiple servers example
├── 🖥️ servers/                        # Local MCP servers
│   ├── hello_http_server.py          # HTTP greeting server
│   └── math_stdio_server.py          # StdIO math server
├── 📄 test_outputs/                   # Generated test outputs
├── LICENSE.md
└── README.md                         # This file
```

## 🔧 Advanced Usage

### Context7 Integration

Context7 provides hosted MCP servers accessible via streamable-HTTP:

```python
# In scaffolding approach (crew.py)
mcp_server_params = {
    "url": "https://api.context7.ai/mcp",
    "transport": "streamable-http"
}

# In script approach
server_params = {
    "url": "https://api.context7.ai/mcp", 
    "transport": "streamable-http"
}
```

### Tool Filtering

In the scaffolding approach, you can filter which tools are available:

```python
@agent
def researcher(self) -> Agent:
    return Agent(
        config=self.agents_config['researcher'],
        tools=self.get_mcp_tools("search", "summarize")  # Only these tools
    )
```

### Environment Variables

Create a `.env` file in your project root:

```env
# Required: Your LLM API key
OPENAI_API_KEY=sk-your-openai-api-key-here

# Optional: Model configuration
MODEL=openai/gpt-4o-mini

# Optional: MCP server URLs (if using environment-based config)
CONTEXT7_MCP_URL=https://api.context7.ai/mcp
```

## 🔧 Troubleshooting

### Common Issues

1. **"AttributeError: 'CrewBase' object has no attribute 'get_mcp_tools'"**
   - **Solution**: Upgrade to CrewAI >= 0.134.0
   ```bash
   uv pip install --upgrade crewai>=0.134.0
   ```

2. **Version keeps reverting to 0.130.0**
   - **Cause**: Dependency constraint in `pyproject.toml`
   - **Solution**: Update constraint to `"crewai[tools]>=0.134.0,<1.0.0"`

3. **MCP server connection failed**
   - **Check**: Server URL is accessible
   - **Check**: Network connectivity for remote servers
   - **Check**: Local server is running for StdIO

4. **Import errors**
   - **Solution**: Ensure you have the MCP extras installed:
   ```bash
   uv pip install 'crewai-tools[mcp]'
   ```

### Debugging Tips

- Use `verbose=True` in your agents to see detailed execution logs
- Check MCP server logs for connection issues
- Test MCP servers independently before integrating with CrewAI
- Use the script approach first to validate MCP connectivity

### Version Requirements

| Component | Minimum Version | Notes |
|-----------|----------------|-------|
| Python | 3.10 | < 3.14 for compatibility |
| CrewAI | 0.134.0 | For `get_mcp_tools()` support |
| crewai-tools | 0.47.1 | For MCP adapter |

## 🤝 Contributing

Contributions are welcome! Areas where we'd love help:

- Additional MCP server examples
- More transport mechanism demos
- Documentation improvements
- Bug fixes and optimizations

Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

## 📚 Additional Resources

- [CrewAI Documentation](https://docs.crewai.com/)
- [CrewAI MCP Integration Guide](https://docs.crewai.com/mcp/crewai-mcp-integration/)
- [Model Context Protocol Specification](https://github.com/modelcontextprotocol/specification)
- [Context7 MCP Server](https://context7.ai/)

**Happy building with CrewAI and MCP! 🚀**