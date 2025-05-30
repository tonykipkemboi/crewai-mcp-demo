# CrewAI MCP Demo

[![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)](https://www.python.org/downloads/release/python-3120/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![CrewAI](https://img.shields.io/badge/CrewAI-Latest-green)](https://github.com/crewai/crewai)

This repository demonstrates how to use the CrewAI MCP (Model Context Protocol) adapter to interact with MCP Servers using different transport mechanisms. MCP allows AI agents to access external tools and services through a standardized protocol.

## 📋 Table of Contents

- [Overview](#overview)
- [Installation](#installation)
- [Prerequisites](#prerequisites)
- [Installation](#installation)
- [Usage](#usage)
  - [Streamable HTTP Demo](#streamable-http-demo)
  - [SSE Demo](#sse-demo)
  - [StdIO Demo](#stdio-demo)
- [Transport Mechanisms](#transport-mechanisms)
- [Project Structure](#project-structure)
- [How It Works](#how-it-works)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [License](#license)

## 🔍 Overview

The Model Context Protocol (MCP) provides a standardized way for AI agents to interact with external tools and services. This demo showcases how to use CrewAI with MCP servers to build powerful AI applications that can leverage external capabilities.

This project demonstrates three different transport mechanisms:

- Streamable HTTP
- Server-Sent Events (SSE)
- Standard Input/Output (StdIO)

## 🛠️ Prerequisites

- **Python**: Version >= 3.10 < 3.13
- **API Key**: OpenAI API Key or an API key from another LLM provider
- **Operating System**: macOS, Linux, or Windows

## 📦 Installation

1. Clone the repository:

   ```bash
   git clone https://github.com/yourusername/crewai-mcp-demo.git
   cd crewai-mcp-demo
   ```
2. Create and activate a virtual environment:

   ```bash
   python3 -m venv .venv
   source .venv/bin/activate  # On Windows, use: .venv\Scripts\activate
   ```
3. Install dependencies:

   ```bash
   uv pip install 'crewai-tools[mcp]'
   ```

   Or if you don't have uv installed:

   ```bash
   pip install 'crewai-tools[mcp]'
   ```

## 🚀 Usage

### Environment Setup

Create a `.env` file in the root directory with your API key:

```env
MODEL=openai/gpt-4o-mini  # or any model provider/model
OPENAI_API_KEY=sk-proj-***
```

### Streamable HTTP Demo

The Streamable HTTP demo shows how to create a simple greeting agent that communicates with an HTTP server.

1. Start the HTTP server:

   ```bash
   python3 servers/hello_http_server.py
   ```

   You should see output indicating the server is running on http://localhost:8001/mcp
2. In a new terminal window, run the client:

   ```bash
   python3 streamable_http_client_demo.py
   ```
3. Follow the prompts to interact with the greeting agent.

### SSE Demo

The SSE demo shows how to connect to an external SSE-based MCP server.

```bash
python3 sse_client_demo.py
```

### StdIO Demo

The StdIO demo demonstrates how to use a local stdio-based MCP server for mathematical operations.

```bash
python3 stdio_client_demo.py
```

## 🔄 Transport Mechanisms

This demo showcases three different transport mechanisms for MCP:

1. **Streamable HTTP**:

   - A bi-directional communication protocol over HTTP
   - Allows for streaming responses between client and server
   - Ideal for web-based applications
   - Used in `hello_http_server.py` and `streamable_http_client_demo.py`
2. **Server-Sent Events (SSE)**:

   - A one-way communication protocol where the server pushes updates to the client
   - Good for real-time updates from server to client
   - Used in `sse_client_demo.py`
3. **Standard Input/Output (StdIO)**:

   - A simple transport mechanism for local communication
   - Ideal for local processes and testing
   - Used in `math_stdio_server.py` and `stdio_client_demo.py`

## 📁 Project Structure

```
.
├── .env                           # Environment variables
├── README.md                      # This documentation
├── output/                        # Output directory for generated content
├── servers/                       # MCP server implementations
│   ├── hello_http_server.py       # HTTP server with greeting tool
│   └── math_stdio_server.py       # StdIO server with math operations
├── streamable_http_client_demo.py # Client for the HTTP server
├── sse_client_demo.py             # Client for SSE servers
└── stdio_client_demo.py           # Client for StdIO servers
```

## ⚙️ How It Works

### MCP Server

An MCP server exposes tools that can be used by AI agents. In this demo:

- `hello_http_server.py` exposes a simple greeting tool over HTTP
- `math_stdio_server.py` exposes math operations over StdIO

### MCPServerAdapter Parameters

The `MCPServerAdapter` class is the primary way to connect to MCP servers. It accepts a single parameter in its constructor:

```python
def __init__(self, serverparams: StdioServerParameters | dict[str, Any])
```

This parameter can be either:

1. **A dictionary** (for HTTP and SSE transports):

   ```python
   # For Streamable HTTP
   server_params = {
       "url": "http://localhost:8001/mcp",  # Required: URL of the MCP server
       "transport": "streamable-http"       # Required: Transport type
   }

   # For SSE
   server_params = {
       "url": "https://example.com/sse"     # Required: URL of the SSE endpoint
   }
   ```

   **Important Note about the `/mcp` Endpoint:**
   
   For Streamable HTTP transport, the URL typically requires the `/mcp` path suffix. This is because:
   
   - The default endpoint path for MCP communication is `/mcp` in the HTTP Stream Transport specification
   - When you configure a FastMCP server with `transport="streamable-http"`, it automatically serves the MCP API at the `/mcp` endpoint
   - The client must connect to this specific endpoint to communicate with the MCP server
   
   If you customize the endpoint in your server configuration, you would need to update the client URL accordingly.

2. **A StdioServerParameters object** (for STDIO transport):

   ```python
   from mcp import StdioServerParameters

   server_params = StdioServerParameters(
       command="python3",                     # Required: Command to run the server
       args=["path/to/server_script.py"],     # Required: Arguments to the command
       env={"VARIABLE": "value", **os.environ}  # Optional: Environment variables
   )
   ```

### Connecting to Multiple MCP Servers

`MCPServerAdapter` also supports connecting to multiple MCP servers simultaneously. This is useful when your agents need to access tools from different services, each exposed through its own MCP server.

To connect to multiple servers, pass a list of server parameter objects directly to `MCPServerAdapter`. Each element in the list should be a valid server parameter configuration (e.g., a dictionary for HTTP/SSE or an `StdioServerParameters` object for Stdio).

The adapter will attempt to connect to all specified servers, and the `tools` object obtained will contain a combined list of all tools available from all successfully connected servers.

**Example:**

```python
from crewai_tools import MCPServerAdapter
from mcp import StdioServerParameters # If using Stdio
import os # If using os.environ

# Define configurations for multiple MCP servers
server_configurations = [
    # Example Streamable HTTP Server
    {"url": "http://localhost:8001/mcp", "transport": "streamable-http"},
    # Example SSE Server
    {"url": "https://api.example.com/sse_mcp_endpoint"},
    # Example StdIO Server
    StdioServerParameters(
        command="python3",
        args=["path/to/your/stdio_mcp_server.py"],
        env={"PYTHONPATH": ".", **os.environ}, # Example env
    )
]

# Use MCPServerAdapter with the list of configurations
try:
    with MCPServerAdapter(server_configurations) as all_tools:
        print(f"Available tools from all MCP servers: {[tool.name for tool in all_tools]}")

        # 'all_tools' can now be passed to your CrewAI agents
        # from crewai import Agent
        # example_agent = Agent(tools=all_tools, ...)
except Exception as e:
    print(f"Error connecting to MCP servers: {e}")
```
This approach allows for a flexible way to manage tool sources for your CrewAI agents.

### CrewAI Client

The client code demonstrates how to:

1. Connect to an MCP server using `MCPServerAdapter`
2. Create an agent with access to the MCP tools
3. Define tasks for the agent to perform
4. Create a crew with the agent and tasks
5. Execute the crew to perform the tasks

Example from `streamable_http_client_demo.py`:

```python
# Create a connection to the MCP server
with MCPServerAdapter(server_params) as tools:
    # Create an agent with access to the tools
    agent = Agent(
        role="Hello World",
        goal="Greet the user.",
        backstory="A helpful assistant for greeting users.",
        tools=tools,
        reasoning=True
    )
  
    # Define a task for the agent
    task = Task(
        description="Greet the {user}.",
        agent=agent,
        expected_output="A very friendly greeting to the {user}."
    )
  
    # Create and execute a crew
    crew = Crew(agents=[agent], tasks=[task])
    result = crew.kickoff(inputs={"user": input("What's your name? ")})
```

## 🔧 Troubleshooting

### Common Issues

- **Port Conflict**: If you see `[Errno 48] Address already in use` when starting the HTTP server:

  ```python
  # Modify the port in hello_http_server.py
  mcp.run(
      transport="streamable-http", 
      host="localhost", 
      port=8002  # Change from 8001 to another port
  )
  ```

  Also update the client URL in `streamable_http_client_demo.py` to match.
- **Server Not Running**: If the client can't connect to the server, make sure the server is running in a separate terminal window.
- **API Key Issues**: Ensure your API key is correctly set in the `.env` file and that it has not expired.
- **Python Version**: This demo requires Python 3.12. Check your version with `python3 --version`.

### Debugging Tips

- Check server logs for error messages
- Verify that the client is using the correct URL to connect to the server
- Ensure all dependencies are installed correctly

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

For more details on CrewAI and MCP integration, visit the [CrewAI Documentation](https://docs.crewai.com/mcp/crewai-mcp-integration/).
