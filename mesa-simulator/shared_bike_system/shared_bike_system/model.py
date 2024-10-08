import mesa

from .agents import Bike

class SharedMobilityModel(mesa.Model):

    height = 20
    width = 20

    initial_bike = 10

    def __init__(self, width=20, height=20, initial_bike = 10):
        super().__init__()
        # Set parameters
        self.width = width
        self.height = height
        self.initial_bike = initial_bike

        self.grid = mesa.space.MultiGrid(self.width, self.height, torus=True)

        # Data collection to track the number of vehicles
        collectors = {
            "Bikes": lambda m: len(m.agents_by_type[Bike]),
        }
        self.datacollector = mesa.DataCollector(collectors)


        # Create bike
        for i in range(self.initial_bike):
            battery_level = self.random.randint(50, 100)
            bike = Bike(self, True, battery_level)

            # Place agents randomly on the grid
            x = self.random.randrange(self.width)
            y = self.random.randrange(self.height)
            self.grid.place_agent(bike, (x, y))

        self.running = True
        self.datacollector.collect(self)
    
    def step(self):
        self.random.shuffle(self.agent_types)
        for agent_type in self.agent_types:
            self.agents_by_type[agent_type].do("step")

        # collect data
        self.datacollector.collect(self)

    def run_model(self, step_count=200):
        for i in range(step_count):
            self.step()