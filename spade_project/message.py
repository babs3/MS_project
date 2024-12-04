from spade.behaviour import PeriodicBehaviour
import socket
import zmq.asyncio
import asyncio


async def async_message(method, topic, agent_name, latitude, longitude, destination_latitude, destination_longitude, resource):
    context = zmq.asyncio.Context()
    socket = context.socket(getattr(zmq,method))
    socket.connect("tcp://localhost:65432")  # Connect to the broker

    print(f"Agent {resource} is sending messages...")
    try:
        await asyncio.sleep(1)  # Allow time for connection setup
        while True:

            # Define the step size for each movement
            step_size = 0.0005  # Approximately 50 meters

            # Calculate the direction vector to the destination
            delta_lat = destination_latitude - latitude
            delta_lng = destination_longitude - longitude

            # Calculate the distance to the destination
            distance = (delta_lat**2 + delta_lng**2)**0.5

            if distance > step_size:
                # Normalize the direction vector and move by the step size
                direction_lat = delta_lat / distance
                direction_lng = delta_lng / distance

                latitude += direction_lat * step_size
                longitude += direction_lng * step_size
            else:
                # Stop at the destination if within step size
                latitude = destination_latitude
                longitude = destination_longitude
                print(f"Bike {agent_name} has reached the destination!")
                #await asyncio.sleep(3)  # Pause for 3 seconds before next action
                return  # Stop moving further
            
            print()
            

            #message = "location_updates,Agent is at (lat, lng)"
            message = topic + ',' + agent_name + ',' + str(latitude) + ',' + str(longitude) + ',' + str(resource)
            await socket.send_string(message)
            print(f"Agent {resource} sent message: {message}")
            await asyncio.sleep(5)  # Send every 5 seconds
    except asyncio.CancelledError:
        print(f"Agent {resource} is shutting down...")
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