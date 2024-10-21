import mesa
import pandas as pd

from .random_walk import RandomWalker
from mesa import Agent, Model


# Step 1: Load CSV with lat/lng values
df = pd.read_csv("./dataset/all_stations.csv")

# Step 2: Normalize lat/lng to grid coordinates
def normalize_lat_lng(lat, lng, grid_width, grid_height, padding=0):
    # Get the min and max values for latitude and longitude
    lat_min, lat_max = df['lat'].min(), df['lat'].max()
    lng_min, lng_max = df['lng'].min(), df['lng'].max()

    # Apply padding to distribute points more evenly across the grid
    lat_range = lat_max - lat_min
    lng_range = lng_max - lng_min

    lat_min -= padding * lat_range
    lat_max += padding * lat_range
    lng_min -= padding * lng_range
    lng_max += padding * lng_range

    # Normalize lat/lng to the grid size, spreading the stations out more
    grid_x = int((lng - lng_min) / (lng_max - lng_min) * (grid_width - 1))
    grid_y = int((lat - lat_min) / (lat_max - lat_min) * (grid_height - 1))

    return grid_x, grid_y


class StationAgent(Agent):
    def __init__(self, unique_id, model, lat, lng):
        super().__init__(unique_id, model)
        self.type = "station"
        self.lat = lat
        self.lng = lng
        self.grid_x, self.grid_y = normalize_lat_lng(lat, lng, model.grid.width, model.grid.height)

    def step(self):
        pass


class Bike(RandomWalker):
    """
    A bike that is driven by a person.

    The init is the same as the RandomWalker.
    """

    battery_level = 100

    def __init__(self, model, moore, battery_level=100):
        super().__init__(model, moore=moore)
        self.type = "bike"  
        self.battery_level = battery_level

    def step(self):
        """
        A model step. Move, ... .
        """

        # a bike can only move if it has battery
        if self.battery_level >= 1:
            self.random_move()
            self.battery_level -= 1



            

