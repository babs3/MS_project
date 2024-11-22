# main.py
from station_agent import StationAgent
from bike_agent import BikeAgent
from manager_agent import ManagerAgent
import asyncio
from plot_visualization import get_updated_bike_positions_figure
from utils import bike_positions, stations_data, trips_data


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

    # Initialize BikeAgents (one for each trip)
    bike_agents = []
    for _, trip in trips_data.iterrows():
        bike_jid = "bike@jabbim.com/" + trip['ride_id']
        bike_agent = BikeAgent(
                        bike_jid, 
                        "bike", 
                        trip['start_station_id'], 
                        station_coords[trip['start_station_id']]['lat'], 
                        station_coords[trip['start_station_id']]['lng'], 
                        station_coords[trip['end_station_id']]['lat'], 
                        station_coords[trip['end_station_id']]['lng'], 
                        manager_jid)
        bike_agents.append(bike_agent)

    # Start BikeAgents
    for bike in bike_agents:
        await bike.start()

    # Main loop to update positions periodically
    try:
        while True:
            # Use the standalone function to update the bike positions
            updated_fig = get_updated_bike_positions_figure()
            # You can add logic to save or inspect `updated_fig` if needed
            await asyncio.sleep(1)  # Wait before updating again
    except KeyboardInterrupt:
        print("Simulation stopped by user.")
    finally:
        # Stop all agents gracefully
        for bike in bike_agents:
            await bike.stop()
        for agent in station_agents:
            await agent.stop()
        await manager_agent.stop()

if __name__ == "__main__":
    asyncio.run(main())
