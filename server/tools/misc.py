import asyncio
import random
from datetime import datetime, timezone

from mcp import ServerSession
from mcp.server.fastmcp import Context

from .. import mcp_server


@mcp_server.tool()
def get_current_time() -> str:
    """Return the current server time as a string."""
    return datetime.now(timezone.utc).isoformat()


@mcp_server.tool()
def roll_a_dice(sides: int = 6) -> int:
    """Roll a dice with a specified number of sides and return the result."""
    return random.randint(1, sides)


@mcp_server.tool(structured_output=False)
async def get_weather(city: str, time: datetime, ctx: Context) -> str:
    await ctx.info("Calling get_weather tool")
    await ctx.info(f"city: {city}; {type(time) = }, {time = }")
    await asyncio.sleep(0.1)  # Simulate network delay
    print(f"Received get_weather call: city={city}, time={time}")
    return "Sunny with a chance of rain"


@mcp_server.tool(structured_output=False)
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
