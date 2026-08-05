from .repository import Repository
from .analyzer import PythonAnalyzer
from .planner import Planner
from .executor import AgentExecutor
from .tools.default_tools import create_default_registry
from .agent_loop import AgentLoop
from .answer import AnswerGenerator



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



        self.agent_loop = AgentLoop(
            self.executor
        )

        self.answer_generator = AnswerGenerator()



    async def answer(self, question):

        print("\nUser Question:")
        print(question)


        # result = await self.executor.run(
        #     question
        # )

        result = await self.agent_loop.run(
            question
        )

        final_answer = self.answer_generator.generate(
            question,
            result["observations"]
        )

        return final_answer
