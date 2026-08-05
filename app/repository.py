from pathlib import Path


class Repository:

    def __init__(self, project_path):
        self.project_path = Path(project_path)


    def list_files(self):

        files = []

        for file in self.project_path.rglob("*"):

            if file.is_file():

                files.append(str(file.relative_to(self.project_path)))

        return sorted(files)


    def read_file(self, filename):

        file_path = self.project_path / filename

        if not file_path.exists():
            raise FileNotFoundError(
                f"{filename} does not exist"
            )

        return file_path.read_text()

    def search_code(self, keyword):

        matches = []

        for file in self.project_path.rglob("*"):

            if file.is_file():

                try:
                    content = file.read_text()

                    if keyword.lower() in content.lower():

                        matches.append(
                            str(file.relative_to(self.project_path))
                        )

                except Exception:
                    pass

        return matches
