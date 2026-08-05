class AgentLoop:

    def __init__(
            self,
            planner,
            executor
    ):
        ...


    async def run(
            self,
            question
    ):

        for step in range(5):

            plan = planner.create_plan(
                question
            )

            result = executor.execute(
                plan
            )

            observe(result)

            decide_if_done()
