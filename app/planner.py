import json
import re

from .llm import LLM


class Planner:

    def __init__(self, tool_registry):

        self.llm = LLM()
        self.tool_registry = tool_registry


    def get_tool_description(self):

        tools = []

        for tool in self.tool_registry.list_tools():

            tools.append(
                f"""
Tool Name:
{tool.name}

Description:
{tool.description}
"""
            )

        return "\n".join(tools)



    def create_plan(self, question):

        available_tools = self.get_tool_description()


        prompt = f"""
You are a tool selection engine for an AI coding agent.

Your ONLY job is to select the correct tool.

User question:

{question}


Available tools:

{available_tools}


Tool selection rules:

1. If the user asks:
- Where is something implemented?
- Where is a feature located?
- Find code related to something

Use:

search_code


2. If the user asks:
- Explain a specific file
- Show the contents of a file

Use:

read_file


3. If the user asks:
- Analyze code structure
- Find classes, functions, imports

Use:

analyze_file


4. If additional enterprise knowledge or documentation is required:

Use:

rag_search



Return ONLY valid JSON.

Required format:

{{
    "tool": "tool_name",
    "input": "tool_input"
}}


Examples:


Question:
Where is authentication implemented?

Response:

{{
    "tool": "search_code",
    "input": "authentication"
}}


Question:
Explain auth.py

Response:

{{
    "tool": "read_file",
    "input": "auth.py"
}}


Question:
Analyze this code

Response:

{{
    "tool": "analyze_file",
    "input": "source code"
}}


Important:
- Do not explain.
- Do not summarize.
- Do not rewrite.
- Do not add markdown.
- JSON only.
"""


        response = self.llm.ask(prompt)


        print("\n========== LLM RESPONSE ==========")
        print(response)
        print("==================================\n")


        plan = self.parse_json(response)


        # Validate tool selection

        allowed_tools = [
            tool.name
            for tool in self.tool_registry.list_tools()
        ]


        if plan.get("tool") not in allowed_tools:

            raise Exception(
                f"Invalid tool selected: {plan.get('tool')}"
            )


        return plan



    def parse_json(self, response):

        response = response.strip()


        # Direct JSON

        try:

            return json.loads(response)

        except json.JSONDecodeError:

            pass



        # Extract JSON object

        match = re.search(
            r"\{[\s\S]*?\}",
            response
        )


        if match:

            json_text = match.group()


            try:

                return json.loads(json_text)

            except json.JSONDecodeError:

                pass



        raise Exception(
            f"""
Planner failed: LLM did not return valid JSON.

LLM Response:

{response}
"""
        )
