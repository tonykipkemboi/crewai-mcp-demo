To add OAuth to a remote MCP server on Cloudflare, follow these steps:

1. **Create and Deploy Your MCP Server**:
   Run the following command to create a new MCP server:
   
   ```sh
   npm create cloudflare@latest
   ```
   Move into your project folder:
   
   ```sh
   cd my-mcp-server-github-auth
   ```
   Deploy the MCP server:
   
   ```sh
   npx wrangler@latest deploy
   ```

2. **Set Up OAuth Provider**:
   In your `src/index.ts`, set the `defaultHandler` to the relevant OAuth handler. For example, if using GitHub as the OAuth provider, it would look like this:

   ```ts
   import GitHubHandler from "./github-handler";

   export default new OAuthProvider({
       apiRoute: "/sse",
       apiHandler: MyMCP.Router,
       defaultHandler: GitHubHandler,
       authorizeEndpoint: "/authorize",
       tokenEndpoint: "/token",
       clientRegistrationEndpoint: "/register",
   });
   ```

3. **Create Your OAuth App**:
   You need to create OAuth client apps in your chosen OAuth provider (e.g., GitHub). Obtain the client ID and secret, and configure them in your MCP server settings.

4. **Handling Authentication and Authorization**:
   Your MCP Server can handle authorization itself while relying on an external authentication service to authenticate users. You will implement your authentication handler either manually or using a service like the Cloudflare Workers OAuth Provider Library.

5. **Using Third-party OAuth Provider**:
   If using a third-party OAuth provider like GitHub, Google, or Auth0, ensure your `OAuthProvider` is configured with your custom handler that implements the OAuth flow. This may look similar to:

   ```ts
   import MyAuthHandler from "./auth-handler";

   export default new OAuthProvider({
       apiRoute: "/mcp",
       apiHandler: MyMCPServer.Router,
       defaultHandler: MyAuthHandler,
       authorizeEndpoint: "/authorize",
       tokenEndpoint: "/token",
       clientRegistrationEndpoint: "/register",
   });
   ```

6. **Authorize Users**:
   Set up processes for users to log in and authorize access through the OAuth provider. This typically involves redirecting users to the OAuth authorization URL, handling the callback with an authorization code, and exchanging the code for an access token to grant the MCP client access.

Refer to the [official Cloudflare documentation](https://developers.cloudflare.com/agents/guides/remote-mcp-server/#add-authentication) for a detailed walkthrough and example implementations.