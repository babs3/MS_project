# main.py
import pandas as pd
from station_agent import StationAgent
from bike_agent import BikeAgent
from manager_agent import ManagerAgent
import matplotlib.pyplot as plt
import asyncio
import matplotlib.animation as animation
from common import bike_positions, stations_data

# Set up the plot
fig, ax = plt.subplots(figsize=(10, 6))
ax.scatter(stations_data['lng'], stations_data['lat'], color='blue', label='Stations')
for _, row in stations_data.iterrows():
    ax.text(row['lng'], row['lat'], row['station_name'], fontsize=9, ha='right')
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Bike Stations and Bikes')
ax.set_xlim(min(stations_data['lng']) - 0.01, max(stations_data['lng']) + 0.01)
ax.set_ylim(min(stations_data['lat']) - 0.01, max(stations_data['lat']) + 0.01)

# Plot for bikes (empty at first)
bikes_plot, = ax.plot([], [], 'ro', label='Bikes')  # Red dots for bikes
ax.legend()

# Maximize the Matplotlib window
#manager = plt.get_current_fig_manager()
#manager.window.showMaximized()  # Maximize window to full screen

# Function to update the plot with new bike positions
def update_plot():
    if bike_positions:
        #print("Updating plot...")
        lons, lats = zip(*bike_positions.values())  # Get longitudes and latitudes
        bikes_plot.set_data(lons, lats)  # Update the data for bikes on the plot
        plt.draw()  # Redraw the plot



async def main():
    
    # Initialize ManagerAgent
    manager_jid = "ms_project@jabbim.com"
    manager_password = "ms_project"  # Replace with actual password
    manager_agent = ManagerAgent(manager_jid, manager_password, bike_positions)
    await manager_agent.start()

    # Initialize StationAgents
    station_agents = []
    for _, station in stations_data.iterrows():
        station_jid = f"{station['station_name']}@jabbim.com"
        station_agent = StationAgent(station_jid, "station")  # Replace with actual password
        station_agents.append(station_agent)
    
    # Start StationAgents
    for agent in station_agents:
        await agent.start()

    # Initialize BikeAgents
    bikes = [
        BikeAgent("bike_0@jabbim.com", "bike", "station_0@jabbim.com", 40.7128, -74.0060, manager_jid),
        BikeAgent("bike_1@jabbim.com", "bike", "station_0@jabbim.com", 40.7128, -74.0060, manager_jid),
        BikeAgent("bike_2@jabbim.com", "bike", "station_1@jabbim.com", 40.7064, -74.0099, manager_jid)
    ]

    # Start BikeAgents
    for bike in bikes:
        await bike.start()

    # Main loop to update positions periodically
    try:
        while True:
            update_plot()  # Manually update the plot
            plt.pause(1)  # Pause to allow the plot to update every 1 second
            await asyncio.sleep(1)  # Wait before updating again
    except KeyboardInterrupt:
        print("Simulation stopped by user.")
    finally:
        # Stop all agents gracefully
        for bike in bikes:
            await bike.stop()
        for agent in station_agents:
            await agent.stop()
        await manager_agent.stop()

if __name__ == "__main__":
    asyncio.run(main())
