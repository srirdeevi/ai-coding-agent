import ast


class PythonAnalyzer:


    def analyze(self, code):

        tree = ast.parse(code)

        result = {
            "classes": [],
            "functions": [],
            "imports": []
        }


        for node in ast.walk(tree):

            if isinstance(node, ast.ClassDef):

                result["classes"].append(
                    node.name
                )


            elif isinstance(node, ast.FunctionDef):

                result["functions"].append(
                    node.name
                )


            elif isinstance(node, ast.Import):

                for name in node.names:
                    result["imports"].append(
                        name.name
                    )


            elif isinstance(node, ast.ImportFrom):

                result["imports"].append(
                    node.module
                )


        return result
