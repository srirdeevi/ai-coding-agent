from .repository import Repository
from .analyzer import PythonAnalyzer
from .planner import Planner
from .executor import AgentExecutor
from .tools.default_tools import create_default_registry



class CodingAgent:


    def __init__(self, project_path):

        self.repository = Repository(
            project_path
        )

        self.analyzer = PythonAnalyzer()


        self.tool_registry = create_default_registry(
            self.repository
        )


        self.planner = Planner(
            self.tool_registry
        )


        self.executor = AgentExecutor(
            self.planner,
            self.tool_registry
        )



    async def answer(self, question):

        print("\nUser Question:")
        print(question)


        result = await self.executor.run(
            question
        )


        print("\nAgent Result:")
        print(result)


        return result
