from .registry import ToolRegistry
from .mcp_rag_tool import MCPRAGSearchTool
from .repository_tools import (
    SearchCodeTool,
    ReadFileTool,
    AnalyzeFileTool,
)


def create_default_registry(repository):

    registry = ToolRegistry()


    # MCP / RAG tool
    registry.register(
        MCPRAGSearchTool()
    )


    # Repository tools
    registry.register(
        SearchCodeTool(repository)
    )

    registry.register(
        ReadFileTool(repository)
    )

    registry.register(
        AnalyzeFileTool()
    )


    return registry
