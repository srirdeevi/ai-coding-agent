class AgentLoop:


    def __init__(
            self,
            executor,
            max_steps=5
    ):

        self.executor = executor
        self.max_steps = max_steps



    async def run(
            self,
            question
    ):

        print("\n# Starting Agent Loop")


        observations = []

        steps = []


        for step in range(self.max_steps):

            print(
                f"\nAgent Step: {step + 1}"
            )


            result = await self.executor.run(
                question,
                observations
            )


            print("\nResult:")
            print(result)


            steps.append(
                result.get(
                    "plan",
                    {}
                )
            )


            observations.append(
                result["result"]
            )


            if self.should_stop(result):

                break



        return {

            "question": question,

            "steps": steps,

            "observations": observations

        }

    def should_stop(
            self,
            result
    ):


        if not isinstance(result, dict):
            return False


        data = result.get(
            "result",
            {}
        )


        # Stop after code analysis

        if "analysis" in data:

            return True


        return False
