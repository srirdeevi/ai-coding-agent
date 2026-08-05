from typing import Dict

from .base import Tool


class ToolRegistry:
    """
    Registry that manages available agent tools.
    """

    def __init__(self):
        self._tools: Dict[str, Tool] = {}

    def register(self, tool: Tool):
        """
        Add a tool to the registry.
        """
        self._tools[tool.name] = tool

    def get(self, name: str):
        """
        Retrieve a tool by name.
        """
        return self._tools.get(name)

    def list_tools(self):
        """
        Return all available tools.
        """
        return list(self._tools.values())
