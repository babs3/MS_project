import mesa

class MyAgent(mesa.Agent):
    agent_id = 0
    def __init__(self, model, age):
        super().__init__(MyAgent.agent_id,model)
        self.age = age
        MyAgent.agent_id += 1

    def step(self):
        self.age += 1
        print(f"Agent {self.unique_id} now is {self.age} years old")
        # Whatever else the agent does when activated