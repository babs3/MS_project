import zmq.asyncio
import asyncio

async def broker():
    context = zmq.asyncio.Context()
    socket = context.socket(zmq.SUB)
    socket.bind("tcp://*:65432")  # Bind to a specific port
    socket.setsockopt_string(zmq.SUBSCRIBE, "location_updates")  # Subscribe to the topic

    print("Broker is running and waiting for messages...")
    try:
        while True:
            message = await socket.recv_string()
            print(f"Received message: {message}")
    except asyncio.CancelledError:
        print("Broker is shutting down...")
    finally:
        socket.close()
        context.term()

if __name__ == "__main__":
    try:
        asyncio.run(broker())
    except KeyboardInterrupt:
        print("Broker stopped.")
