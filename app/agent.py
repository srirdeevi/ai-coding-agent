from repository import Repository
from analyzer import PythonAnalyzer


class CodingAgent:


    def __init__(self, project_path):

        self.repository = Repository(project_path)
        self.analyzer = PythonAnalyzer()



    def answer(self, question):

        print("\nUser Question:")
        print(question)


        if "authentication" in question.lower():

            files = self.repository.search_code(
                "auth"
            )

            print("\nRelevant Files:")

            for file in files:
                print(file)


            for file in files:

                code = self.repository.read_file(file)

                analysis = self.analyzer.analyze(code)


                print("\nAnalysis:")
                print(file)
                print(analysis)


        else:

            print(
                "I need more information."
            )
