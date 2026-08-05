class AgentState:


    def __init__(self, question):

        self.question = question

        self.steps = []

        self.observations = []

        self.finished = False



    def add_step(
            self,
            plan,
            result
    ):

        self.steps.append(plan)

        self.observations.append(result)



    def last_observation(self):

        if self.observations:

            return self.observations[-1]

        return None
