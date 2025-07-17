# CrewAI MCP Demo

[![Python 3.10+](https://img.shields.io/badge/python-3.10%2B-blue.svg)](https://www.python.org/downloads/) [![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT) [![CrewAI](https://img.shields.io/badge/CrewAI-0.134.0%2B-green)](https://github.com/crewai/crewai)

This repository demonstrates **different approaches** for using CrewAI with MCP (Model Context Protocol) to interact with external tools and services through a standardized protocol.

## 🌟 **Featured Examples**

### 🏭 **Enterprise Regulatory Intelligence** 
**📍 Location:** `scaffolding_approach_examples/snowflake_mcp_demo/`

A **production-ready 3-agent system** that combines CrewAI's multi-agent orchestration with Snowflake's enterprise data capabilities to build regulatory intelligence systems.

**Key Features:**
- 🤖 **3-Agent Coordination**: Regulatory Intelligence + SEC Filing Analysis + Market News
- 📊 **Enterprise Scale**: Semantic search across 372,299 SEC filings via Snowflake MCP
- 🎯 **Professional Output**: Investment-grade regulatory impact reports
- 🚀 **Production Ready**: Complete deployment and configuration examples

[**→ View Detailed Tutorial**](scaffolding_approach_examples/snowflake_mcp_demo/)

---

## 🚀 **Two Integration Approaches**

This repository demonstrates **two different ways** to integrate CrewAI with MCP:

### 1. 🏗️ **Scaffolding Approach** (Recommended for Production)
- Uses CrewAI's project scaffolding with `@CrewBase` decorator
- Structured project with configuration files
- Built-in `get_mcp_tools()` method (CrewAI 0.134.0+)
- Better for complex, maintainable applications

**Examples:**
- **Snowflake Enterprise Demo** - Regulatory intelligence system
- **Mathematician Project** - Math operations via local StdIO server  
- **Context7 Integration** - Document search via streamable-HTTP

### 2. 📝 **Script Approach** (Great for Learning/Prototyping)
- Standalone Python scripts using `MCPServerAdapter` directly
- Quick to set up and experiment with
- Perfect for understanding MCP concepts

**Examples:**
- `stdio_client_demo.py` - Math operations
- `sse_client_demo.py` - Cloudflare docs search
- `streamable_http_client_demo.py` - Simple greeting
- `multiple_servers_client_demo.py` - Combined functionality

---

## 🔧 **Transport Mechanisms**

### **Streamable HTTP** ⭐ (Recommended)
- **Use case**: Remote hosted servers (Context7, cloud services)
- **Benefits**: Simple setup, bidirectional communication, web-friendly
- **Example**: Snowflake MCP, Context7 API

### **Server-Sent Events (SSE)**
- **Use case**: Real-time server-to-client updates
- **Benefits**: Good for streaming responses, widely supported
- **Example**: Cloudflare docs, real-time data feeds

### **Standard Input/Output (StdIO)**
- **Use case**: Local development, testing, process-based servers
- **Benefits**: Simple local setup, no network required
- **Example**: Local math server, file processing tools

---

## 📁 **Project Structure**

```
crewai-mcp-demo/
├── 🏗️ scaffolding_approach_examples/
│   ├── snowflake_mcp_demo/          # 🌟 FEATURED: Enterprise regulatory intelligence
│   ├── mathematician_project/       # Math operations via local StdIO server
│   └── crewai_context7_mcp/         # Context7 integration via streamable-HTTP
├── 📝 script_approach_examples/      # Standalone script examples
│   ├── stdio_client_demo.py         # Math operations via StdIO
│   ├── sse_client_demo.py           # Cloudflare docs via SSE
│   ├── streamable_http_client_demo.py # Greeting via HTTP
│   └── multiple_servers_client_demo.py # Multiple servers example
├── 🖥️ servers/                       # Local MCP servers
│   ├── hello_http_server.py         # HTTP greeting server
│   └── math_stdio_server.py         # StdIO math server
└── README.md                        # This file
```

---

## ⚡ **Quick Start**

### **Option 1: Try the Enterprise Demo** (Recommended)
```bash
cd scaffolding_approach_examples/snowflake_mcp_demo/
# Follow the detailed setup guide in that directory
```

### **Option 2: Try a Simple Script**
```bash
# For math operations (local server)
python3 script_approach_examples/stdio_client_demo.py

# For Cloudflare docs (remote server)  
python3 script_approach_examples/sse_client_demo.py
```

---

## 🛠️ **Prerequisites**

- **Python**: Version >= 3.10 < 3.14
- **CrewAI**: Version >= 0.134.0 (for scaffolding approach)
- **API Keys**: Depends on the example (OpenAI, Snowflake, etc.)
- **uv** (recommended) or pip for package management

---

## 📚 **Learn More**

### **Featured Documentation**
- [**🏭 Enterprise Regulatory Intelligence Tutorial**](scaffolding_approach_examples/snowflake_mcp_demo/) - Complete production system
- [**🧮 Mathematician Project**](scaffolding_approach_examples/mathematician_project/) - Local MCP server integration
- [**🔍 Context7 Integration**](scaffolding_approach_examples/crewai_context7_mcp/) - Cloud MCP service

### **Resources**
- [CrewAI Documentation](https://docs.crewai.com/)
- [CrewAI MCP Integration Guide](https://docs.crewai.com/mcp/crewai-mcp-integration/)
- [Model Context Protocol Specification](https://github.com/modelcontextprotocol/specification)

---

## 🤝 **Contributing**

Contributions welcome! Areas where we'd love help:
- Additional MCP server examples
- More transport mechanism demos  
- Documentation improvements
- Bug fixes and optimizations

---

## 📄 **License**

This project is licensed under the MIT License - see the [LICENSE.md](LICENSE.md) file for details.

---

## ⭐ **Star History**

<iframe style="width:100%;height:auto;min-width:600px;min-height:400px;" src="https://www.star-history.com/embed?secret=Z2hwX1l5NVBiS1U2UjA0Q1ZobW1FajRoaE5ncE5WNFJHMDFpQmtPQw==#tonykipkemboi/crewai-mcp-demo&Date" frameBorder="0"></iframe>

**Happy building with CrewAI and MCP! 🚀**