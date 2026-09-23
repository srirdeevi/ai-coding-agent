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


        # -----------------------------------------
        # Collect evidence
        # -----------------------------------------

        for item in observations:

            # -----------------------------------------
            # read_file result
            # -----------------------------------------

            if (
                    "file" in item
                    and
                    "content" in item
            ):

                content = item["content"]
                file_name = item["file"]


                # A successfully read source file
                # containing code is implementation evidence.

                if (
                        "class " in content
                        or
                        "def " in content
                ):

                    implementation_files.append(
                        file_name
                    )


            # -----------------------------------------
            # analyzer result
            # -----------------------------------------

            if "analysis" in item:

                analysis = item["analysis"]


                classes.extend(
                    analysis.get(
                        "classes",
                        []
                    )
                )


                functions.extend(
                    analysis.get(
                        "functions",
                        []
                    )
                )


            # -----------------------------------------
            # search result
            # -----------------------------------------

            if "files" in item:

                references.extend(
                    item["files"]
                )


        # -----------------------------------------
        # Remove duplicates
        # -----------------------------------------

        implementation_files = list(
            dict.fromkeys(
                implementation_files
            )
        )


        classes = list(
            dict.fromkeys(
                classes
            )
        )


        functions = list(
            dict.fromkeys(
                functions
            )
        )


        references = list(
            dict.fromkeys(
                references
            )
        )


        # -----------------------------------------
        # Evidence-grounded answer
        # -----------------------------------------

        if implementation_files:

            answer = (
                    "The implementation was found in "
                    + ", ".join(
                implementation_files
            )
                    + "."
            )


            if classes:

                answer += (
                        " The "
                        + ", ".join(classes)
                        + " class"
                        + (
                            "es"
                            if len(classes) > 1
                            else ""
                        )
                        + " "
                        + (
                            "contain"
                            if len(classes) > 1
                            else "contains"
                        )
                        + " the relevant implementation."
                )


            if functions:

                answer += (
                        " Relevant function"
                        + (
                            "s are "
                            if len(functions) > 1
                            else " is "
                        )
                        + ", ".join(functions)
                        + "."
                )


        else:

            answer = (
                "No implementation matching the question "
                "was found in the repository based on "
                "the searches performed."
            )


        # -----------------------------------------
        # Return structured result
        # -----------------------------------------

        return {
            "question": question,
            "answer": answer,
            "implementation_files": implementation_files,
            "classes": classes,
            "functions": functions
        }
