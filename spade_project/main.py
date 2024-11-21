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
        station_jid = "station@jabbim.com/" + station['station_name']
        station_agent = StationAgent(station_jid, "station")  # Replace with actual password
        station_agents.append(station_agent)
    
    # Start StationAgents
    for agent in station_agents:
        await agent.start()

    # Map station IDs to their coordinates (lat, lng)
    station_coords = stations_data.set_index('station_id')[['lat', 'lng']].to_dict(orient='index')

    # Initialize BikeAgents
    bikes = [
        BikeAgent(
            "bike@jabbim.com/bike_0", 
            "bike", 
            "station@jabbim.com/Buckingham Fountain", 
            station_coords[2.0]['lat'], 
            station_coords[2.0]['lng'], 
            manager_jid
        ),
        BikeAgent(
            "bike@jabbim.com/bike_1", 
            "bike", 
            "station@jabbim.com/Shedd Aquarium", 
            station_coords[2.0]['lat'], 
            station_coords[2.0]['lng'], 
            manager_jid
        ),
        BikeAgent(
            "bike@jabbim.com/bike_2", 
            "bike", 
            "station@jabbim.com/Burnham Harbor", 
            station_coords[4.0]['lat'], 
            station_coords[4.0]['lng'], 
            manager_jid
        )
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
