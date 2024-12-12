import spade
from spade.agent import Agent
from spade import wait_until_finished
from behavior import CreateMessageBehaviour
import asyncio
import zmq
import threading
from bike_agent import BikeAgent
from station_agent import StationAgent
from utils import add_or_update_bike, bike_positions, stations_data, trips_data, rides_data
from plot_visualization import get_updated_bike_positions_figure
   
def zmq_listener(socket, dict):
    while True:
        try:
            message = socket.recv_string()  # Block until message arrives
            print(f"Received message: {message}")
            node, payload, resource = message.split(",", 2)  # Split into topic and payload
            dict_keys = dict.keys()
            #if(dict_keys) :
            if resource not in dict_keys:
                dict[resource] = payload    
            
            #payload = payload + ' ' + resource
            #message_queue.put((node.strip(), payload.strip()))  # Push message to the queue
            for key , _ in dict.items():
                print("--> " + key + " : " + dict[key])
            
        except zmq.ZMQError as e:
            print(f"ZeroMQ Error: {e}")
            break
        except Exception as e:
            print(f"Error: {e}")
            
async def main():
    
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:65433")  # Bind to port 5555

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
    for idx, ride in rides_data.iterrows():
        bike_jid = "bike@jabbim.com/" + str(idx) #trip['ride_id']
        bike_agent = BikeAgent(
                        bike_jid, 
                        "bike",
                        ride['started_at'], 
                        ride['start_station_id'], 
                        station_coords[ride['start_station_id']]['lat'], 
                        station_coords[ride['start_station_id']]['lng'], 
                        station_coords[ride['end_station_id']]['lat'], 
                        station_coords[ride['end_station_id']]['lng'],
                        ride['ride_duration']
                        )
        bike_agents.append(bike_agent)

        add_or_update_bike(idx, station_coords[ride['start_station_id']]['lat'], station_coords[ride['start_station_id']]['lng'])

    # Start BikeAgents
    for bike in bike_agents:
        await bike.start(auto_register=True)
    
    #agent = BikeAgent("ms_proj@macaw.me/0", "1234") # resource = 0
    #await agent.start(auto_register=True)
    #agent1 = BikeAgent("ms_proj@macaw.me/1", "1234") # resource = 1
    #await agent1.start(auto_register=True)
    
    message_dict = dict()
    
    zmq_thread = threading.Thread(target=zmq_listener, args=(socket, message_dict))
    zmq_thread.daemon = True  # Ensures thread exits when the program exits
    zmq_thread.start()
    
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
    

if __name__ == "__main__":
    spade.run(main()) 
