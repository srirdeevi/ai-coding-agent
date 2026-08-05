import json
import re

from llm import LLM


class Planner:


    def __init__(self):

        self.llm = LLM()



    def create_plan(self, question):

        prompt = f"""
You are an AI coding agent planner.

Your job is to decide which tool should be used.

User question:

{question}


Available tools:

1. search_code
   - Finds files containing a keyword

2. read_file
   - Reads the contents of a file

3. analyze_file
   - Extracts classes, functions, and imports from a file


Return ONLY JSON.

Do not write explanations.
Do not use markdown.
Do not add ```.

Example:

{{
    "tool": "search_code",
    "input": "authentication"
}}

"""


        response = self.llm.ask(prompt)


        print("\n========== LLM RESPONSE ==========")
        print(response)
        print("==================================\n")


        return self.parse_json(response)



    def parse_json(self, response):

        # First attempt:
        # direct JSON

        try:

            return json.loads(response)

        except json.JSONDecodeError:

            pass



        # Remove markdown formatting

        cleaned = response.replace(
            "```json",
            ""
        )

        cleaned = cleaned.replace(
            "```",
            ""
        )

        cleaned = cleaned.strip()



        # Second attempt

        try:

            return json.loads(cleaned)

        except json.JSONDecodeError:

            pass



        # Extract JSON object from text

        match = re.search(
            r"\{.*?\}",
            cleaned,
            re.DOTALL
        )


        if match:

            json_text = match.group()

            return json.loads(json_text)



        raise Exception(
            "Planner failed: LLM did not return JSON"
        )
