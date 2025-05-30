# Hello Task
Hello, **Tony Kipkemboi**! Welcome! We're glad to have you here. Enjoy your day!

----------

# Math Task
The result of the mathematical operation is: 
**400**

----------

# Docs Task
## MCP Transports in Cloudflare

The **Model Context Protocol (MCP)** defines several transport mechanisms for handling communication between clients and servers, crucial for building responsive AI applications. Here’s a breakdown of the transport options available in MCP:

### Supported Transport Mechanisms

1. **Standard Input/Output (stdio)**:
   - Designed for local MCP connections, allowing communication through standard input and output.

2. **Server-Sent Events (SSE)**:
   - Currently supported by most remote MCP clients.
   - Requires two endpoints: one for sending requests to the server and another for receiving streamed responses.
   - While widely used, SSE is expected to be phased out as the newer Streamable HTTP method is adopted.

3. **Streamable HTTP**:
   - Introduced in March 2025, this transport method simplifies the communication process by utilizing a single HTTP endpoint capable of handling bidirectional messaging.
   - This new model is gaining traction and is expected to become the standard for future MCP interactions.

### Implementing Remote MCP Transport

For those building a new MCP server or upgrading an existing one on Cloudflare, it’s advisable to support both remote transport methods (SSE and Streamable HTTP) to maintain compatibility with a variety of clients. Here’s how you can get started:

- **Quick Deployment**: Use the "Deploy to Cloudflare" button to create a remote MCP server that supports both SSE and Streamable HTTP automatically. 

    [![Deploy to Workers](https://deploy.workers.cloudflare.com/button)](https://deploy.workers.cloudflare.com/?url=https://github.com/cloudflare/ai/tree/main/demos/remote-mcp-authless)

### Example Implementation

When configuring a remote MCP server without authentication, you might set it up like this:

```js
export default {
  fetch(request: Request, env: Env, ctx: ExecutionContext) {
    const { pathname } = new URL(request.url);

    if (pathname.startsWith('/sse')) {
      return MyMcpAgent.serveSSE('/sse').fetch(request, env, ctx);
    }

    if (pathname.startsWith('/mcp')) {
      return MyMcpAgent.serve('/mcp').fetch(request, env, ctx);
    }
  },
};
```

To create an MCP server that implements authentication, the configuration might resemble this:

```js
export default new OAuthProvider({
  apiHandlers: {
    '/sse': MyMCP.serveSSE('/sse'),
    '/mcp': MyMCP.serve('/mcp'),
  },
  // ... other OAuth configuration
});
```

### Testing with MCP Clients

Although the Streamable HTTP transport is still in the process of being adopted by many clients, developers can start testing this feature now using the mcp-remote adapter. This allows clients that typically only support local connections to interact with remote MCP servers.

For more detailed instructions on connecting to your remote MCP server, you can refer to the [testing guide](https://developers.cloudflare.com/agents/guides/test-remote-mcp-server/).

---

Understanding and implementing these transport mechanisms is critical for effective utilization of the MCP in Cloudflare, enhancing communication between AI systems and external applications.