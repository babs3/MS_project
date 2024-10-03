# Import the model
from model import SharedMobilityModel

# Create an instance of the model
model = SharedMobilityModel(10, 10, 20)  # 10x10 grid, 20 vehicles

# Run the model for 50 steps
for i in range(50):
    model.step()

# Access the collected data
data = model.datacollector.get_agent_vars_dataframe()
print(data)

