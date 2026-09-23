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

        context = context or []


        # -----------------------------------------
        # Rule-based planning
        # -----------------------------------------

        plan = self.rule_based_plan(
            question,
            context
        )


        if plan:

            return plan


        # -----------------------------------------
        # LLM planning
        # -----------------------------------------

        prompt = f"""
You are an AI coding agent planner.

Return only JSON.

Choose exactly one tool.

Available tools:

search_code
read_file
analyze_file
rag_search

Question:

{question}

Previous agent history:

{json.dumps(context, indent=2)}

Important rules:

- Do not repeat the same tool with the same input.
- If search_code returned no files, use a different search term.
- If a file was successfully read, use analyze_file.
- If relevant files were found, use read_file.
- Do not invent file names.
- Do not use read_file unless the file was returned by search_code.
- Choose only one tool.

Format:

{{
"tool": "tool_name",
"input": "value"
}}
"""


        response = self.llm.ask(
            prompt
        )


        print(
            "\n========== LLM RESPONSE =========="
        )

        print(response)

        print(
            "==================================\n"
        )


        return self.parse_json(
            response
        )


    def rule_based_plan(
            self,
            question,
            context
    ):

        # -----------------------------------------
        # No previous history
        # -----------------------------------------

        if not context:

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


        # -----------------------------------------
        # Inspect the latest observation
        # -----------------------------------------

        last = context[-1]

        last_result = last.get(
            "result",
            {}
        )


        # -----------------------------------------
        # Previous search
        # -----------------------------------------

        if "files" in last_result:

            files = last_result["files"]


            # Search found files
            if files:

                for file_path in files:

                    if not self.action_was_used(
                            context,
                            "read_file",
                            file_path
                    ):

                        return {
                            "tool": "read_file",
                            "input": file_path
                        }


            # Search found nothing
            else:

                alternative = self.find_alternative_keyword(
                    question,
                    context
                )


                if alternative:

                    return {
                        "tool": "search_code",
                        "input": alternative
                    }


                # No alternative search terms remain.
                return {
                    "tool": "rag_search",
                    "input": question
                }


        # -----------------------------------------
        # Previous file read
        # -----------------------------------------

        if "content" in last_result:

            content = last_result["content"]

            if content:

                if not self.action_was_used(
                        context,
                        "analyze_file",
                        content
                ):

                    return {
                        "tool": "analyze_file",
                        "input": content
                    }


        # -----------------------------------------
        # Previous analysis
        # -----------------------------------------

        if "analysis" in last_result:

            return None


        # -----------------------------------------
        # Previous error
        # -----------------------------------------

        if "error" in last_result:

            alternative = self.find_alternative_keyword(
                question,
                context
            )


            if alternative:

                return {
                    "tool": "search_code",
                    "input": alternative
                }


            return {
                "tool": "rag_search",
                "input": question
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
            "transaction",
            "billing",
            "checkout",
            "purchase",

            "user",
            "account",
            "profile"
        ]


        for word in keywords:

            if word in question:

                return word


        return question


    def find_alternative_keyword(
            self,
            question,
            context
    ):

        """
        Find a different search term that has not
        already been attempted.
        """

        q = question.lower()


        keyword_map = {

            "payment": [
                "transaction",
                "billing",
                "checkout",
                "purchase"
            ],

            "transaction": [
                "payment",
                "billing",
                "purchase"
            ],

            "authentication": [
                "login",
                "authenticate",
                "credential",
                "authorization"
            ],

            "login": [
                "authentication",
                "authenticate",
                "credential"
            ],

            "database": [
                "db",
                "connection",
                "repository"
            ],

            "user": [
                "account",
                "profile",
                "customer"
            ]
        }


        candidates = []


        for key, alternatives in keyword_map.items():

            if key in q:

                candidates.extend(
                    alternatives
                )


        attempted = set()


        # Collect search terms from actual
        # planner history.

        for item in context:

            plan = item.get(
                "plan",
                {}
            )


            if plan.get("tool") == "search_code":

                search_input = plan.get(
                    "input"
                )

                if search_input:

                    attempted.add(
                        search_input
                    )


        for candidate in candidates:

            if candidate not in attempted:

                return candidate


        return None


    def action_was_used(
            self,
            context,
            tool,
            tool_input
    ):

        """
        Determine whether the exact same
        tool/input combination was already used.
        """

        for item in context:

            plan = item.get(
                "plan",
                {}
            )


            if (
                    plan.get("tool") == tool
                    and
                    plan.get("input") == tool_input
            ):

                return True


        return False


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
