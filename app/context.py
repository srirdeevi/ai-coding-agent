from .repository import Repository


class RepositoryContext:


    def __init__(self, repository):

        self.repository = repository


    def build(self):

        context = ""

        files = self.repository.list_files()


        for file in files:

            context += f"""

FILE:
{file}

CONTENT:
{self.repository.read_file(file)}

----------------------

"""

        return context
