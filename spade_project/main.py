# main.py
import pandas as pd
from station_agent import StationAgent
from bike_agent import BikeAgent
from manager_agent import ManagerAgent
import matplotlib.pyplot as plt
import asyncio
import matplotlib.animation as animation
from common import bike_positions, stations_data

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Load the bike and station icons 
bike_icon = mpimg.imread('spade_project/images/bike_icon.png')  # Path to your bike icon image
station_icon = mpimg.imread('spade_project/images/station_icon.png')  # Path to your station icon image

# Set up the plot
fig, ax = plt.subplots(figsize=(8, 6))

# Plot the line connecting stations
station_0 = stations_data[stations_data['station_name'] == 'station_0']
station_1 = stations_data[stations_data['station_name'] == 'station_1']

# Extract coordinates for the line
path_lngs = [station_0['lng'].values[0], station_1['lng'].values[0]]
path_lats = [station_0['lat'].values[0], station_1['lat'].values[0]]

# Draw the line
ax.plot(path_lngs, path_lats, linestyle='-', color='gray', label='Path Between Stations')


# Add station icons
for _, row in stations_data.iterrows():
    station_icon_extent = (
        row['lng'] - 0.0008, row['lng'] + 0.0008,  # Adjust extent for station size
        row['lat'] - 0.0008, row['lat'] + 0.0008
    )
    ax.imshow(station_icon, extent=station_icon_extent, zorder=2)

# Annotate station names
for _, row in stations_data.iterrows():
    ax.text(row['lng'], row['lat'], row['station_name'], fontsize=9, ha='right')

# Label axes and title
ax.set_xlabel('Longitude')
ax.set_ylabel('Latitude')
ax.set_title('Bike Stations and Bikes')

# Set limits
ax.set_xlim(min(stations_data['lng']) - 0.01, max(stations_data['lng']) + 0.01)
ax.set_ylim(min(stations_data['lat']) - 0.01, max(stations_data['lat']) + 0.01)

# Add legend
ax.legend()

# Track bike icon objects
bike_icons = []

# Function to update the plot with new bike positions
def update_plot():
    global bike_icons

    # Remove previous bike icons
    for icon in bike_icons:
        icon.remove()
    bike_icons.clear()

    # Add updated bike icons
    if bike_positions:
        for lng, lat in bike_positions.values():
            bike_icon_extent = (lng - 0.0005, lng + 0.0005, lat - 0.0005, lat + 0.0005)
            icon = ax.imshow(bike_icon, extent=bike_icon_extent, zorder=2)
            bike_icons.append(icon)

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
