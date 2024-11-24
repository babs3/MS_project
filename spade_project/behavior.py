from spade.behaviour import PeriodicBehaviour
import socket
import zmq.asyncio
import asyncio

class CreateMessageBehaviour(PeriodicBehaviour):
    async def run(self):
        context = zmq.asyncio.Context()
        socket = context.socket(zmq.PUB)
        socket.connect("tcp://localhost:65432")  # Connect to the broker

        print("Agent is sending messages...")
        try:
            await asyncio.sleep(1)  # Allow time for connection setup
            while True:
                message = "location_updates,Agent is at (lat, lng)"
                await socket.send_string(message)
                print(f"Agent sent message: {message}")
                await asyncio.sleep(5)  # Send every 5 seconds
        except asyncio.CancelledError:
            print("Agent is shutting down...")
        finally:
            socket.close()
            context.term()

        

            