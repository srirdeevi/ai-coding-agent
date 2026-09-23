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

        context = []

        reflection = {
            "stop": False,
            "reason": "Agent has not started."
        }

        for step in range(self.max_steps):

            print(
                f"\nAgent Step: {step + 1}"
            )

            try:

                result = await self.executor.run(
                    question,
                    context
                )

            except Exception as error:

                print("\nTool Execution Error:")
                print(error)

                failure = {
                    "error": str(error)
                }

                context.append(
                    {
                        "plan": context[-1]["plan"]
                        if context
                        else {},
                        "result": failure
                    }
                )

                reflection = self.reflect(
                    failure
                )

                print("\nReflection:")
                print(reflection)

                if reflection["stop"]:
                    break

                print(
                    "\n# Agent will attempt recovery"
                )

                continue


            print("\nResult:")
            print(result)


            plan = result.get(
                "plan",
                {}
            )

            observation = result.get(
                "result",
                {}
            )


            # Store both the action and its result.
            #
            # This is the agent's working memory.

            context.append(
                {
                    "plan": plan,
                    "result": observation
                }
            )


            reflection = self.reflect(
                observation
            )

            print("\nReflection:")
            print(reflection)


            if reflection["stop"]:

                print(
                    "\n# Agent has enough evidence"
                )

                break


            print(
                "\n# Agent needs more evidence"
            )


        return {

            "question": question,

            "steps": [
                item["plan"]
                for item in context
                if "plan" in item
            ],

            "observations": [
                item["result"]
                for item in context
                if "result" in item
            ],

            "context": context,

            "reflection": reflection

        }


    def reflect(
            self,
            observation
    ):

        """
        Evaluate the latest observation and determine
        whether the agent should stop or continue.
        """

        if not isinstance(
                observation,
                dict
        ):

            return {
                "stop": False,
                "reason": "Invalid observation."
            }


        # -----------------------------------------
        # Tool execution failure
        # -----------------------------------------

        if "error" in observation:

            return {
                "stop": False,
                "reason": (
                    "The previous tool execution failed. "
                    "The agent should recover."
                )
            }


        # -----------------------------------------
        # Code analysis completed
        # -----------------------------------------

        if "analysis" in observation:

            analysis = observation.get(
                "analysis"
            )

            if analysis:

                return {
                    "stop": True,
                    "reason": (
                        "Source code was successfully "
                        "analyzed."
                    )
                }


        # -----------------------------------------
        # File successfully read
        # -----------------------------------------

        if "content" in observation:

            content = observation.get(
                "content"
            )

            if content:

                return {
                    "stop": False,
                    "reason": (
                        "Source code was retrieved. "
                        "Further analysis is required."
                    )
                }


        # -----------------------------------------
        # Search results
        # -----------------------------------------

        if "files" in observation:

            files = observation.get(
                "files"
            )

            if files:

                return {
                    "stop": False,
                    "reason": (
                        "Relevant files were found. "
                        "A source file should be inspected."
                    )
                }


            return {
                "stop": False,
                "reason": (
                    "No matching files were found. "
                    "The agent should try another strategy."
                )
            }


        # -----------------------------------------
        # Unknown observation
        # -----------------------------------------

        return {
            "stop": False,
            "reason": (
                "More evidence is required before "
                "answering."
            )
        }
