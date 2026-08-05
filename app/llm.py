import ollama


class LLM:

    def ask(self, prompt):

        response = ollama.chat(

            model="tinyllama:latest",

            messages=[
                {
                    "role": "user",
                    "content": prompt
                }
            ]

        )

        return response["message"]["content"]
