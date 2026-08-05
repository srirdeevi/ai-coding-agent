import asyncio

from .agent import CodingAgent


async def main():

    agent = CodingAgent(
        "sample_project"
    )


    result = await agent.answer(
        "Where is authentication implemented?"
    )


    print("\nFinal Answer:")
    print(result)



if __name__ == "__main__":

    asyncio.run(main())
