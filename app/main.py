import asyncio

from .agent import CodingAgent



async def main():

    agent = CodingAgent(
        "sample_project"
    )


    await agent.answer(
        "Where is authentication implemented?"
    )



if __name__ == "__main__":

    asyncio.run(main())
