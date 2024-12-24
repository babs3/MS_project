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
            #ride_duration = pd.Timedelta(agent.ride_duration)
            
            if agent.start_time <= current_time <= agent.end_time:
                print(f"Agent {agent.agent_name} is moving...")

                # Move the agent: update the current station

            elif current_time > agent.end_time:
                print(f"Bike {agent.agent_name} has reached the destination!")
                
                message = topic + ',' + agent.agent_name + ',' + str(agent.end_station)
                await socket.send_string(message)
                print(f"Agent {agent.jid.resource} sent message: {message}")
                
                await agent.stop()
                print(f"Agent {agent.jid.resource} stopped.")
                return  # Stop moving further
            
            await asyncio.sleep(2) # Send every 2 seconds
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