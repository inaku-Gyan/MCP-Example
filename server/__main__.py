from . import mcp_server

from . import tools as _

del _

# Run server with streamable_http transport
if __name__ == "__main__":
    mcp_server.run(transport="streamable-http")
