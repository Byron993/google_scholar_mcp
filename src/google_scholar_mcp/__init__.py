"""Google Scholar MCP Server"""

from mcp.server.fastmcp import FastMCP
from pydantic import Field

from .core import search_scholar

mcp = FastMCP("scholar-search", log_level="ERROR")


@mcp.tool(
    name="谷歌学术搜索",
    description="搜索谷歌学术并返回相关论文信息，包括标题、作者、期刊、年份和摘要",
)
async def search_google_scholar(
    query: str = Field(description="搜索关键词"),
    num_results: int = Field(default=5, description="返回的结果数量，默认为5"),
) -> str:
    return await search_scholar(query, num_results)


def main():
    """启动MCP服务器"""
    mcp.run(transport="stdio")
