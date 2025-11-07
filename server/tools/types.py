from typing import Generic, Literal, TypeVar

from pydantic import BaseModel


__all__ = ["ToolCallResultChunk"]

DetailT = TypeVar("DetailT", bound=BaseModel)


# Pydantic-v2 BaseModel 只支持 Generic + TypeVar 的方式
class ToolCallResultChunk(BaseModel, Generic[DetailT]):
    """
    工具标准返回格式。

    注意：所有工具调用都返回异步生成器，该格式是生成器的单个 chunk。
    """

    status: Literal["running", "success", "error", "aborted"]
    """当前工具执行状态"""

    result_str: str | None = None
    """发送给 LLM 的工具调用结果"""

    detail: DetailT | None = None
    """详细信息，用于前端渲染给用户看"""
