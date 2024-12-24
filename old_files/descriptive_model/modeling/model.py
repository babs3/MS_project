import mesa
import numpy as np
from agents import MyAgent


class MyModel(mesa.Model):
    def __init__(self, n_agents):
        super().__init__()
        self.grid = mesa.space.MultiGrid(10, 10, torus=True)
        for _ in range(n_agents):
            initial_age = self.random.randint(0, 80)
            a = MyAgent(self, initial_age)
            coords = (self.random.randrange(0, 10), self.random.randrange(0, 10))
            self.grid.place_agent(a, coords)
        self.datacollector = mesa.DataCollector(
                model_reporters={"mean_age": lambda m: m.agents.agg("age", np.mean)},
                agent_reporters={"age": "age"}
            )

    def step(self):
        self.agents.shuffle_do("step")
        self.datacollector.collect(self)


import mesa.visualization

def agent_portrayal(agent):
    portrayal = {"Shape": "circle",
                 "Filled": "true",
                 "Layer": 0,
                 "Color": "red",
                 "r": 0.5}
    return portrayal

grid = mesa.visualization.CanvasGrid(agent_portrayal, 10, 10, 500, 500)
server = mesa.visualization.ModularServer(MyModel,
                       [grid],
                       "My Model",
                       {'n_agents': 10})
server.launch()