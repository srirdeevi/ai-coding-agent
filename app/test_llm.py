from llm import LLM


llm = LLM()


response = llm.ask(
    "Return only this JSON: {\"status\":\"working\"}"
)


print(response)
