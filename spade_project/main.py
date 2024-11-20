# main.py
import pandas as pd
from station_agent import StationAgent
from bike_agent import BikeAgent
from manager_agent import ManagerAgent
import matplotlib.pyplot as plt
import asyncio
import matplotlib.animation as animation

# Shared data structure to store bike positions
bike_positions = {}


async def main():
    # Load station data
    stations_data = pd.DataFrame({
        'station_id': [0, 1],
        'station_name': ['station_0', 'station_1'],
        'lat': [40.7128, 40.7064],
        'lng': [-74.0060, -74.0099]
    })

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

    # Set up the plot
    fig, ax = plt.subplots(figsize=(8, 6))
    ax.scatter(stations_data['lng'], stations_data['lat'], color='blue', label='Stations')
    for _, row in stations_data.iterrows():
        ax.text(row['lng'], row['lat'], row['station_name'], fontsize=9, ha='right')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.set_title('Bike Stations and Bikes')
    ax.set_xlim(min(stations_data['lng']) - 0.01, max(stations_data['lng']) + 0.01)
    ax.set_ylim(min(stations_data['lat']) - 0.01, max(stations_data['lat']) + 0.01)

    bikes_plot, = ax.plot([], [], 'ro', label='Bikes')  # Red dots for bikes
    ax.legend()

    # Resize the window
    manager = plt.get_current_fig_manager()
    manager.resize(*manager.window.maxsize())  # Maximize window size
    # Alternatively, for full screen:
    # manager.full_screen_toggle()

    # Function to update the plot
    def update_plot(frame):
        if bike_positions:
            print("Updating plot with bike positions:", bike_positions)  # Debugging
            lons, lats = zip(*bike_positions.values())
            bikes_plot.set_data(lons, lats)
        return bikes_plot,

    # Create the animation
    ani = animation.FuncAnimation(
        fig, 
        update_plot, 
        interval=1000, 
        save_count=1000,  # Set a reasonable number for caching, or disable it as below
        cache_frame_data=False  # Explicitly disable caching of frame data
    )

    # Show the plot
    plt.show()


    # Run until interrupted
    try:
        while True:
            await asyncio.sleep(1)  # Keep the event loop alive
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
