# Agents > Model Context Protocol (MCP) > Transport

The Model Context Protocol (MCP) specification defines three standard transport mechanisms for communication between clients and servers:

1. **stdio, communication over standard in and standard out** — designed for local MCP connections.
2. **Server-Sent Events (SSE)** — Currently supported by most remote MCP clients, but is expected to be replaced by Streamable HTTP over time. It requires two endpoints: one for sending requests, another for receiving streamed responses.
3. **Streamable HTTP** — New transport method introduced in March 2025. It simplifies communication by using a single HTTP endpoint for bidirectional messaging. It is currently gaining adoption among remote MCP clients but is expected to become the standard transport in the future.

MCP servers built with the Agents SDK can support both remote transport methods (SSE and Streamable HTTP), with the `McpAgent` class automatically handling the transport configuration. 

## Implementing remote MCP transport

If you're building a new MCP server or upgrading an existing one on Cloudflare, supporting both remote transport methods (SSE and Streamable HTTP) concurrently is recommended to ensure compatibility with all MCP clients.

### Get started quickly
You can deploy a remote MCP server that automatically supports both SSE and Streamable HTTP transport methods.

#### Remote MCP server (without authentication)
If you're manually configuring your MCP server, here's how to use the `McpAgent` class to handle both transport methods:

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

### MCP Server with Authentication
If your MCP server implements authentication & authorization using the Workers OAuth Provider Library, you can configure it to support both transport methods using the `apiHandlers` property.

```js
export default new OAuthProvider({
  apiHandlers: {
    '/sse': MyMCP.serveSSE('/sse'),
    '/mcp': MyMCP.serve('/mcp'),
  },
  // ... other OAuth configuration
});
```

### Upgrading an Existing Remote MCP Server
If you've already built a remote MCP server using the Cloudflare Agents SDK, make the following changes to support the new Streamable HTTP transport while maintaining compatibility with remote MCP clients using SSE:
- Use `MyMcpAgent.serveSSE('/sse')` for the existing SSE transport. Previously, this would have been `MyMcpAgent.mount('/sse')`, which has been kept as an alias.
- Add a new path with `MyMcpAgent.serve('/mcp')` to support the new Streamable HTTP transport.

To use apiHandlers, ensure you update to @cloudflare/workers-oauth-provider v0.0.4 or later.

### Testing with MCP Clients
While most MCP clients have not yet adopted the new Streamable HTTP transport, you can start testing it today using `mcp-remote`, an adapter that lets MCP clients that otherwise only support local connections work with remote MCP servers.