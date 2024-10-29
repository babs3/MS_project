# main.py
import pandas as pd
from station_agent import StationAgent
import matplotlib.pyplot as plt
import asyncio

# Load station data
stations_data = pd.DataFrame({
    'station_id': [1, 2, 3],
    'station_name': ['Station A', 'Station B', 'Station C'],
    'lat': [40.7128, 40.7064, 40.7311],
    'lng': [-74.0060, -74.0099, -73.9934]
})

# Visualize stations
plt.scatter(stations_data['lng'], stations_data['lat'], color='blue')
for _, row in stations_data.iterrows():
    plt.text(row['lng'], row['lat'], row['station_name'], fontsize=9, ha='right')
plt.xlabel('Longitude')
plt.ylabel('Latitude')
plt.title('Bike Stations')
plt.show()

# Asynchronous function to manage agents
async def manage_agents():
    # Initialize agents for each station
    agents = []
    for _, station in stations_data.iterrows():
        station_agent = StationAgent(
            station['station_name'] + "@localhost",  # Placeholder ID
            "password"  # Placeholder password
        )
        agents.append(station_agent)

    # Start agents
    for agent in agents:
        await agent.start()

    # Keep agents running until user presses Enter
    try:
        await asyncio.get_running_loop().run_in_executor(None, input, "Press Enter to stop...")
    finally:
        # Stop all agents gracefully
        for agent in agents:
            await agent.stop()

# Run the asynchronous function
asyncio.run(manage_agents())
