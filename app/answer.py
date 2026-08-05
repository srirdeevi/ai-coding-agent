class AnswerGenerator:


    def generate(
            self,
            question,
            observations
    ):

        implementation_files = []
        references = []

        classes = []
        functions = []


        for item in observations:


            # read_file result
            if "file" in item and "content" in item:

                content = item["content"]
                file_name = item["file"]


                # if source defines classes/functions,
                # consider it implementation
                if (
                        "class " in content
                        or "def " in content
                ):

                    implementation_files.append(
                        file_name
                    )


            # analyzer result
            if "analysis" in item:

                analysis = item["analysis"]

                classes.extend(
                    analysis.get("classes", [])
                )

                functions.extend(
                    analysis.get("functions", [])
                )


            # search result
            if "files" in item:

                references.extend(
                    item["files"]
                )


        implementation_files = list(
            set(implementation_files)
        )


        return {
            "question": question,
            "answer": (
                    "Authentication is implemented in "
                    + ", ".join(implementation_files)
            ),
            "implementation_files": implementation_files,
            "classes": classes,
            "functions": functions
        }
