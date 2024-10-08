from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from shared_bike_system.model import SharedMobilityModel

# Function to visualize the agents
def agent_portrayal(agent):
    if agent is None:
        return
    
    portrayal = {}

    if agent.battery_level > 50:
        portrayal["Color"] = ["#00FF00", "#00CC00", "#009900"]
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = True
        portrayal["r"] = 0.8
        portrayal["Layer"] = 0
    else:
        portrayal["Color"] = ["#FF0000", "#CC0000", "#990000"]
        portrayal["Shape"] = "circle"
        portrayal["Filled"] = True
        portrayal["r"] = 0.8
        portrayal["Layer"] = 0
    return portrayal

# Set up the grid for visualization
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

# add chart element here later

# Our model parameters
model_params = {
    "width": 10, 
    "height": 10, 
    "initial_bike": 10
}

# Set up the server for running the visualization
server = ModularServer(
    SharedMobilityModel,  # Your model class
    [grid],  # List of visual components (e.g., the grid)
    "Shared Mobility Model",  # Title for the visualization window
    model_params  # Pass model parameters as a dictionary
)

server.port = 8521  # Default port
