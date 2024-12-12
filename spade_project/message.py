import pandas as pd
from spade.behaviour import PeriodicBehaviour
import socket
import zmq.asyncio
import asyncio
from utils import delete_bike


async def async_message(method, topic, agent):
    context = zmq.asyncio.Context()
    socket = context.socket(getattr(zmq,method))
    socket.connect("tcp://localhost:65432")  # Connect to the broker

    print(f"Agent {agent.jid.resource} is sending messages...")
    try:
        await asyncio.sleep(1)  # Allow time for connection setup
        while True:

            current_time = pd.Timestamp.now()
            ride_duration = pd.Timedelta(agent.ride_duration)
            # Update coordinates if agent's end time is less than current end time
            
            if agent.start_time <= current_time:
                print(f"Agent {agent.agent_name} is moving...")

                # Calculate the direction vector to the destination
                delta_lat = agent.destination_latitude - agent.latitude
                delta_lng = agent.destination_longitude - agent.longitude

                # Calculate the distance to the destination
                distance = (delta_lat**2 + delta_lng**2)**0.5

                if distance > agent.step_size:
                    # Normalize the direction vector and move by the step size
                    direction_lat = delta_lat / distance
                    direction_lng = delta_lng / distance

                    agent.latitude += direction_lat * agent.step_size
                    agent.longitude += direction_lng * agent.step_size
                else:
                    # Stop at the destination if within step size
                    agent.latitude = agent.destination_latitude
                    agent.longitude = agent.destination_longitude
                    print(f"Bike {agent.agent_name} has reached the destination!")
                    delete_bike(agent.agent_name)
                    await agent.stop()
                    return  # Stop moving further
                                
                message = topic + ',' + agent.agent_name + ',' + str(agent.latitude) + ',' + str(agent.longitude) + ',' + str(agent.jid.resource)
                await socket.send_string(message)
                print(f"Agent {agent.jid.resource} sent message: {message}")
            await asyncio.sleep(2)  # Send every ? seconds
    except asyncio.CancelledError:
        print(f"Agent {agent.jid.resource} is shutting down...")
    finally:
        socket.close()
        context.term()
        
async def async_message_sub(method, topic, payload, resource):
    context = zmq.asyncio.Context()
    socket = context.socket(getattr(zmq,method))
    socket.connect("tcp://localhost:65433")  # Connect to the broker

    print(f"Sub Client {resource} is sending messages...")
    try:
        await asyncio.sleep(1)  # Allow time for connection setup
        while True:
            #message = "location_updates,Agent is at (lat, lng)"
            message = topic + ',' + payload + ',' + str(resource)
            await socket.send_string(message)
            print(f"Message {resource} sent message: {message}")
            await asyncio.sleep(5)  # Send every 5 seconds
    except asyncio.CancelledError:
        print(f"Connection is shutting down...")
    finally:
        socket.close()
        context.term()