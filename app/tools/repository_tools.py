from typing import Any

from .base import Tool

from ..repository import Repository
from ..analyzer import PythonAnalyzer


class SearchCodeTool(Tool):

    name = "search_code"

    description = """
    Search the repository for files containing a keyword.
    Input should be a search keyword.
    """

    def __init__(self, repository: Repository):

        self.repository = repository


    async def execute(self, keyword: str) -> Any:

        files = self.repository.search_code(
            keyword
        )

        return {
            "files": files
        }



class ReadFileTool(Tool):

    name = "read_file"

    description = """
    Read the contents of a source code file.
    Input should be a file path.
    """

    def __init__(self, repository: Repository):

        self.repository = repository


    async def execute(
            self,
            file_path: str
    ) -> Any:

        available_files = self.repository.list_files()


        if file_path not in available_files:

            return {
                "error": "File does not exist",
                "requested_file": file_path,
                "available_files": available_files
            }


        content = self.repository.read_file(
            file_path
        )


        return {
            "file": file_path,
            "content": content
        }



class AnalyzeFileTool(Tool):

    name = "analyze_file"

    description = """
    Analyze source code and extract classes,
    functions, and imports.
    Input should be source code.
    """

    def __init__(self):

        self.analyzer = PythonAnalyzer()


    async def execute(self, code: str) -> Any:

        result = self.analyzer.analyze(
            code
        )

        return {
            "analysis": result
        }
