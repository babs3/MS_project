import mesa
import pandas as pd
from mesa.time import RandomActivation

from .agents import Bike, StationAgent

# Step 1: Load CSV with lat/lng values
df = pd.read_csv("./dataset/all_stations.csv")

class SharedMobilityModel(mesa.Model):

    initial_bike = 10

    def __init__(self, width, height, initial_bike = 10):
        super().__init__()
        # Set parameters
        self.initial_bike = initial_bike

        self.grid = mesa.space.MultiGrid(width, height, torus=True)
        self.schedule = RandomActivation(self)

        # Data collection to track the number of vehicles
        collectors = {
            "Bikes": lambda m: len(m.agents_by_type[Bike]),
        }
        self.datacollector = mesa.DataCollector(collectors)

        # Create bikes
        for i in range(self.initial_bike):
            battery_level = self.random.randint(50, 100)
            bike = Bike(self, True, battery_level)

            # Place agents randomly on the grid
            x = self.random.randrange(width)
            y = self.random.randrange(height)
            self.grid.place_agent(bike, (x, y))

        # Create station agents from the CSV
        for idx, row in df.iterrows():
            agent = StationAgent(idx, self, row['lat'], row['lng'])
            self.grid.place_agent(agent, (agent.grid_x, agent.grid_y))
            self.schedule.add(agent)

        self.running = True
        self.datacollector.collect(self)
    
    def step(self):
        self.random.shuffle(self.agent_types)
        for agent_type in self.agent_types:
            self.agents_by_type[agent_type].do("step")

        # collect data
        self.datacollector.collect(self)
        
        # used in BikeStationModel
        #self.schedule.step()
        

    def run_model(self, step_count=200):
        for i in range(step_count):
            self.step()