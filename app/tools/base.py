from abc import ABC, abstractmethod
from typing import Any


class Tool(ABC):
    """
    Base contract for all agent tools.
    """

    name: str
    description: str

    @abstractmethod
    async def execute(self, **kwargs) -> Any:
        """
        Execute the tool.
        """
        pass
