import ollama


class LLM:


    def ask(self, prompt):

        response = ollama.chat(

            model="tinyllama:latest",

            messages=[

                {
                    "role": "system",
                    "content": """
You are a strict AI agent planner.

Your only job is to select a tool.

Return valid JSON only.

Never explain.
Never summarize.
Never add markdown.
"""
                },

                {
                    "role": "user",
                    "content": prompt
                }

            ],

            format="json"

        )


        return response["message"]["content"]
