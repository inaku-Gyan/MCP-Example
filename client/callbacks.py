from mcp.types import (
    LoggingMessageNotificationParams,
    ErrorData,
    ElicitRequestParams,
    ElicitResult,
)
from mcp import ClientSession
from mcp.shared.context import RequestContext
from typing import Any


INDENT = "\t"


async def logging_callback(
    params: LoggingMessageNotificationParams,
) -> None:
    logger_name = f"[{params.logger}] " if params.logger else ""
    print(f"[logging_callback] {logger_name}{params.level}: {params.data}")


async def progress_callback(progress: float, total: float | None, message: str | None):
    print(f"[progress_callback] {progress} / {total}")
    print(f"{INDENT}message: {message}")


async def elicitation_callback(
    context: RequestContext[ClientSession, Any],
    params: ElicitRequestParams,
) -> ElicitResult | ErrorData:
    print("[elicitation_callback]")
    print(f"{INDENT}{context}")
    print(f"{INDENT}{params = }")

    # For demonstration purposes, we will return a fixed value.
    # In a real scenario, you would collect user input here.
    value = 42  # Example fixed integer value

    print(f"{INDENT}responding with value: {value}")

    return ElicitResult(action="accept", content={"value": value})
