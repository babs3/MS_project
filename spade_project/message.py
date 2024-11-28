from spade.behaviour import PeriodicBehaviour
import socket
import zmq.asyncio
import asyncio


async def async_message(method, topic, payload, resource):
    context = zmq.asyncio.Context()
    socket = context.socket(getattr(zmq,method))
    socket.connect("tcp://localhost:65432")  # Connect to the broker

    print(f"Agent {resource} is sending messages...")
    try:
        await asyncio.sleep(1)  # Allow time for connection setup
        while True:
            #message = "location_updates,Agent is at (lat, lng)"
            message = topic + ',' + payload + ',' + str(resource)
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