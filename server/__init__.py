from mcp.server.fastmcp import FastMCP

from config import MCP_SERVER_PORT

# Stateful server (maintains session state)
mcp_server = FastMCP("LocalDevMCPServer", port=MCP_SERVER_PORT)

# Other configuration options:
# Stateless server (no session persistence)
# mcp_server = FastMCP("StatelessServer", port=MCP_SERVER_PORT, stateless_http=True)

# Stateless server (no session persistence, no sse stream with supported client)
# mcp_server = FastMCP("StatelessServer", stateless_http=True, json_response=True)

del FastMCP, MCP_SERVER_PORT

__all__ = ["mcp_server"]
