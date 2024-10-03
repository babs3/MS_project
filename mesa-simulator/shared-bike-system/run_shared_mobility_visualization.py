from mesa.visualization.modules import CanvasGrid
from mesa.visualization.ModularVisualization import ModularServer
from model import SharedMobilityModel  # Import your model

# Function to visualize the agents
def agent_portrayal(agent):
    if agent.battery_level > 0:
        portrayal = {"Shape": "circle", "Color": "green", "r": 0.8}
    else:
        portrayal = {"Shape": "circle", "Color": "red", "r": 0.8}
    return portrayal

# Set up the grid for visualization
grid = CanvasGrid(agent_portrayal, 10, 10, 500, 500)

# Set up the server for running the visualization
server = ModularServer(
    SharedMobilityModel,  # Your model class
    [grid],  # List of visual components (e.g., the grid)
    "Shared Mobility Model",  # Title for the visualization window
    {"width": 10, "height": 10, "N": 20}  # Pass model parameters as a dictionary
)

server.port = 8521  # Default port
server.launch()
