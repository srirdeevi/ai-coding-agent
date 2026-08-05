import json
import re

from .llm import LLM


class Planner:


    def __init__(
            self,
            tool_registry
    ):

        self.llm = LLM()
        self.tool_registry = tool_registry



    def create_plan(
            self,
            question,
            context=None
    ):


        # First try rule-based planning
        plan = self.rule_based_plan(
            question,
            context
        )


        if plan:

            return plan



        # Otherwise ask LLM

        prompt = f"""
Return only JSON.

Choose one tool.

Available tools:

search_code
read_file
analyze_file
rag_search


Question:

{question}


Format:

{{
"tool":"tool_name",
"input":"value"
}}
"""


        response = self.llm.ask(
            prompt
        )


        print("\n========== LLM RESPONSE ==========")
        print(response)
        print("==================================\n")


        return self.parse_json(
            response
        )



    def rule_based_plan(
            self,
            question,
            context
    ):


        # First check previous observations
        # before looking at the question

        if context:

            last = context[-1]


            if "files" in last:

                files = last["files"]


                if files:

                    return {
                        "tool": "read_file",
                        "input": files[0]
                    }



            if "content" in last:

                return {
                    "tool": "analyze_file",
                    "input": last["content"]
                }



        q = question.lower()



        if (
                "where" in q
                or "implemented" in q
                or "find" in q
                or "location" in q
        ):

            return {
                "tool": "search_code",
                "input": self.extract_keyword(q)
            }



        return None



    def extract_keyword(
            self,
            question
    ):


        keywords = [
            "authentication",
            "login",
            "database",
            "payment",
            "user"
        ]


        for word in keywords:

            if word in question:

                return word


        return question



    def parse_json(
            self,
            response
    ):


        try:

            data = json.loads(
                response
            )


        except Exception:

            match = re.search(
                r"\{.*\}",
                response,
                re.DOTALL
            )


            if not match:

                raise Exception(
                    "Planner failed"
                )


            data = json.loads(
                match.group()
            )


        if (
                "tool" in data
                and "input" in data
        ):

            return data


        raise Exception(
            f"Invalid planner output: {data}"
        )
