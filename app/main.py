from repository import Repository
from context import RepositoryContext
from analyzer import PythonAnalyzer
from agent import CodingAgent



repo = Repository("../sample_project")
# code = repo.read_file("auth.py")
code = repo.read_file("app.py")
agent = CodingAgent(
    "../sample_project"
)

context_builder = RepositoryContext(repo)


context = context_builder.build()


print(context)


result = repo.search_code("login")


print("Search Results")
print("----------------")


for file in result:
    print(file)

analyzer = PythonAnalyzer()


result1 = analyzer.analyze(code)


print(result1)

# coding agent

agent = CodingAgent(
    "../sample_project"
)


agent.answer(
    "Where is authentication implemented?"
)
