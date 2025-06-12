# Leonardo MCP Server

A Model Context Protocol (MCP) server for Leonardo AI, supporting both HTTP and stdio modes.

## Features
- Exposes Leonardo AI image generation and model management via MCP
- Supports both HTTP and stdio transports

## Installation

1. **Clone the repository:**
   ```sh
   git clone <this-repo-url>
   cd leonardo-mcp-server
   ```
2. **Install dependencies:**
   ```sh
   uv pip install -r requirements.txt  # or use `uv pip install .` if you have uv
   ```
   Or, if you use [uv](https://github.com/astral-sh/uv):
   ```sh
   uv venv .venv
   source .venv/bin/activate
   uv pip install .
   ```

## Usage

### With `uvx` (recommended)

You can run the server using [uvx](https://github.com/modelcontextprotocol/uvx):

```sh
uvx @leonardo-mcp-server --mode http   # HTTP mode (default)
uvx @leonardo-mcp-server --mode stdio  # stdio mode
```

Or set the environment variable:

```sh
MCP_MODE=stdio uvx @leonardo-mcp-server
```

### Directly with Python

```sh
python main.py http   # HTTP mode (default)
python main.py stdio  # stdio mode
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
uvx @leonardo-mcp-server --mode http
# or
python main.py http
```

If your client is remote (e.g., ChatGPT Playground), you must expose your local server to the internet. You can use [ngrok](https://ngrok.com/) or a similar tunneling tool:

```sh
ngrok http 8080
```

Copy the public URL from ngrok and use it as the endpoint in your client.

### Stdio Mode (for local clients)

Start the server in stdio mode:

```sh
uvx @leonardo-mcp-server --mode stdio
# or
python main.py stdio
```

## Environment Variables
- `LEONARDO_API_KEY` (required): Your Leonardo AI API key.

## Development
- Edit `main.py` to add or modify MCP tools.
- See [python-sdk documentation](https://github.com/modelcontextprotocol/python-sdk) for more info.

## License
MIT
