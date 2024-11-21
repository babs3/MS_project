# main.py
from plot_visualization import update_plot
from station_agent import StationAgent
from bike_agent import BikeAgent
from manager_agent import ManagerAgent
import matplotlib.pyplot as plt
import asyncio
from common import bike_positions, stations_data

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
