class AgentExecutor:


    def __init__(
            self,
            planner,
            tool_registry
    ):

        self.planner = planner
        self.tool_registry = tool_registry



    async def run(
            self,
            question,
            context=None
    ):


        plan = self.planner.create_plan(
            question,
            context
        )


        print("\nPlan:")
        print(plan)


        tool_name = plan.get(
            "tool"
        )


        tool_input = plan.get(
            "input"
        )


        tool = self.tool_registry.get(
            tool_name
        )


        if tool is None:

            raise Exception(
                f"Tool not found: {tool_name}"
            )


        result = await tool.execute(
            tool_input
        )


        return {
            "plan": plan,
            "result": result
        }
