# Leonardo MCP Server

A Model Context Protocol (MCP) server for Leonardo AI, supporting both `HTTP` and `stdio` modes.

## Features
- Create image generation jobs with Leonardo AI
- See available models
- Check the status of image generation jobs
- Get all the user's image generation jobs
- Supports both `HTTP` and `stdio` transports

## Installation

[//]: # (Instructions for different clients)
### JSON Config
Support for Claude Desktop, Cursor and other MCP clients that use JSON config files.

[//]: # (Note, warning, tip)

> [!IMPORTANT]  
> You will need to [generate a Leonardo API key](https://docs.leonardo.ai/docs/create-your-api-key) and set it in the environment variable `LEONARDO_API_KEY` before running the server.


```json
{
  "mcpServers": {
    "leonardo-mcp-server": {
      "command": "uvx",
      "args": [
        "--from",
        "git+https://github.com/ish-joshi/leonardo-mcp-server",
        "leonardo-mcp-server",
        "stdio"
      ],
      "env": {
        "LEONARDO_API_KEY": "YOUR_LEONARDO_API_KEY"
      }
    }
  }
}
```

## Running Modes

This server supports two modes:

- **HTTP mode** (default):
  - Suitable for remote clients (e.g., ChatGPT Playground, browser-based tools).
  - The server runs an HTTP endpoint. You must expose it to the internet if your client is remote.
- **Stdio mode**:
  - Suitable for local clients that communicate over standard input/output (stdio).
  - No network port is opened.

### HTTP Mode (for remote clients)

Start the server in HTTP mode (default):

```sh
uvx --from git+https://github.com/ish-joshi/leonardo-mcp-server leonardo-mcp-server
```

If your client is remote (e.g., ChatGPT Playground), you must expose your local server to the internet. You can use [ngrok](https://ngrok.com/) or a similar tunneling tool:

```sh
ngrok http 8080
```

Copy the public URL from ngrok and use it as the endpoint in your client.

### Stdio Mode (for local clients)

Start the server in stdio mode:

```sh
uvx --from git+https://github.com/ish-joshi/leonardo-mcp-server leonardo-mcp-server stdio
```

## Environment Variables
- `LEONARDO_API_KEY` (required): Your Leonardo AI API key.

## Development
- Edit `main.py` to add or modify MCP tools.
- Run using `python main.py` and test with a compatible MCP client. I prefer to use [5ire](https://5ire.app/) MCP client for testing.
- See [python-sdk documentation](https://github.com/modelcontextprotocol/python-sdk) for more info.
