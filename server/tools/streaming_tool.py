import asyncio
from typing import Literal
from mcp import ServerSession
from mcp.server.fastmcp import Context
from pydantic import BaseModel

from .. import mcp_server
from .types import ToolCallResultChunk


class Detail(BaseModel):
    status: Literal["running", "finished"]
    message: str


Chunk = ToolCallResultChunk[Detail]


@mcp_server.tool()
async def streaming_tool(ctx: Context[ServerSession, None]) -> Chunk:
    """Execute a task with progress updates."""
    total = 10
    for i in range(total):
        await ctx.report_progress(
            progress=i,
            total=total,
            message=f" {i}",
        )
        await ctx.report_progress(
            progress=i + 0.5,
            total=total,
            message=Chunk(
                status="running",
                result_str=f" {i}.5",
            ).model_dump_json(),
        )
        await ctx.report_progress(
            progress=i + 0.75,
            total=total,
            message=Chunk(
                status="running",
                result_str=f" {i}.75",
                detail=Detail(
                    status="running",
                    message=f"Halfway through step {i}",
                ),
            ).model_dump_json(),
        )

    # 如果不延迟的话，会导致最后几个 progress 消息无法送达
    await asyncio.sleep(0.2)

    return Chunk(
        status="success",
        result_str=f" {total}",
        detail=Detail(status="finished", message="All steps completed"),
    )
