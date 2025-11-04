import asyncio
import random
from datetime import datetime, timezone

from mcp import ServerSession

from config import MCP_SERVER_PORT

from mcp.server.fastmcp import Context, FastMCP

# Stateful server (maintains session state)
mcp = FastMCP("StatefulServer", port=MCP_SERVER_PORT)

# Other configuration options:
# Stateless server (no session persistence)
# mcp = FastMCP("StatelessServer", stateless_http=True)

# Stateless server (no session persistence, no sse stream with supported client)
# mcp = FastMCP("StatelessServer", stateless_http=True, json_response=True)


@mcp.tool()
def get_current_time() -> str:
    """Return the current server time as a string."""
    return datetime.now(timezone.utc).isoformat()


@mcp.tool()
def roll_a_dice(sides: int = 6) -> int:
    """Roll a dice with a specified number of sides and return the result."""
    return random.randint(1, sides)


@mcp.tool()
async def get_weather(city: str, time: datetime, ctx: Context) -> str:
    await ctx.info("Calling get_weather tool")
    await ctx.info(f"city: {city}; {type(time) = }, {time = }")
    await asyncio.sleep(0.1)  # Simulate network delay
    return "Sunny with a chance of rain"


@mcp.tool()
async def long_running_task(
    task_name: str, ctx: Context[ServerSession, None], steps: int = 5
) -> str:
    """Execute a task with progress updates."""
    await ctx.info(f"Starting: {task_name}")

    for i in range(steps):
        progress = (i + 1) / steps
        await ctx.report_progress(
            progress=progress,
            total=1.0,
            message=f"Step {i + 1}/{steps}",
        )
        await ctx.debug(f"Completed step {i + 1}")

    return f"Task '{task_name}' completed"


# Run server with streamable_http transport
if __name__ == "__main__":
    mcp.run(transport="streamable-http")
