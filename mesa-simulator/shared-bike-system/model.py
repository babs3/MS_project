from mesa import Model
from mesa.time import RandomActivation
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector

from mesa import Agent

class VehicleAgent(Agent):
    def __init__(self, unique_id, model, battery_level):
        super().__init__(unique_id, model)
        self.battery_level = battery_level  # Define agent-specific properties

    def step(self):
        # Actions performed in each simulation step
        if self.battery_level > 0:
            self.move()
            self.battery_level -= 1  # Decrease battery level
        else:
            self.charge()

    def move(self):
        # Define how vehicles move (for example, random movement)
        possible_moves = self.model.grid.get_neighborhood(
            self.pos, moore=True, include_center=False
        )
        new_position = self.random.choice(possible_moves)
        self.model.grid.move_agent(self, new_position)

    def charge(self):
        # Example of charging logic
        self.battery_level = 100


class SharedMobilityModel(Model):
    def __init__(self, width, height, N):
        self.num_agents = N
        self.grid = MultiGrid(width, height, True)  # Create a 2D grid
        self.schedule = RandomActivation(self)  # Define the scheduling of agent actions

        # Create agents
        for i in range(self.num_agents):
            battery_level = self.random.randint(50, 100)
            agent = VehicleAgent(i, self, battery_level)
            self.schedule.add(agent)

            # Place agents randomly on the grid
            x = self.random.randrange(self.grid.width)
            y = self.random.randrange(self.grid.height)
            self.grid.place_agent(agent, (x, y))

        # Data collection to track the number of vehicles
        self.datacollector = DataCollector(
            agent_reporters={"Battery Level": "battery_level"}
        )

    def step(self):
        # Advance the model by one step
        self.datacollector.collect(self)  # Collect data before step
        self.schedule.step()
