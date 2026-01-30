import asyncio
from datetime import datetime
import json

from config import MCP_SERVER_URL

from .callbacks import logging_callback, progress_callback, elicitation_callback

from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client


async def main():
    # Connect to a streamable HTTP server
    async with streamable_http_client(MCP_SERVER_URL + "/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        # Create a session using the client streams
        async with ClientSession(
            read_stream,
            write_stream,
            logging_callback=logging_callback,
            elicitation_callback=elicitation_callback,
        ) as session:
            # Initialize the connection
            await session.initialize()

            # List available tools
            tools = await session.list_tools()
            print(f"Available tools: {[tool.name for tool in tools.tools]}")

            for tool in tools.tools:
                print("=" * 80)
                print(f"Tool name: {tool.name}")
                print(f"Tool description: {tool.description}")
                print("  input schema  ".center(100, "-"))
                print(json.dumps(tool.inputSchema, indent=2))
                print("  output schema ".center(100, "-"))
                print(json.dumps(tool.outputSchema, indent=2))
                print("-" * 100)
                print()

            print("=" * 80)
            print("=" * 80)

            result = await session.call_tool(
                "get_weather", arguments={"city": "New York", "time": datetime.now()}
            )
            print(result.model_dump_json(indent=2))

            await session.call_tool(
                "long_running_task",
                arguments={"task_name": "Sample Task", "steps": 10},
                progress_callback=progress_callback,
            )

            print("=" * 80)
            print("=" * 80)

            result = await session.call_tool(
                "number_guessing_game",
                arguments={"max_number": 100, "max_attempts": 5},
            )
            print(result.model_dump_json(indent=2))


if __name__ == "__main__":
    asyncio.run(main())
