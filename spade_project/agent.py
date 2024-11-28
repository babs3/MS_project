import spade
from spade.agent import Agent
from spade import wait_until_finished
from behavior import CreateMessageBehaviour
import asyncio
import zmq
import threading

class BikeAgent(Agent):

    async def setup(self):
        print(f"{self.jid} ready!")
        self.add_behaviour(CreateMessageBehaviour(period=5))  # Run every 5 seconds
        
def zmq_listener(socket, dict):
    while True:
        try:
            message = socket.recv_string()  # Block until message arrives
            print(f"Received message: {message}")
            node, payload, resource = message.split(",", 2)  # Split into topic and payload
            dict_keys = dict.keys()
            if(dict_keys) :
                if resource not in dict_keys:
                     dict[resource] = payload    
            
            
            #payload = payload + ' ' + resource
            #message_queue.put((node.strip(), payload.strip()))  # Push message to the queue
            for key , _ in dict.items():
                print(key)
            
        except zmq.ZMQError as e:
            print(f"ZeroMQ Error: {e}")
            break
        except Exception as e:
            print(f"Error: {e}")
            
async def main():
    
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:65433")  # Bind to port 5555
    
    agent = BikeAgent("ms_proj@macaw.me/0", "1234")
    await agent.start(auto_register=True)
    agent1 = BikeAgent("ms_proj@macaw.me/1", "1234")
    await agent1.start(auto_register=True)
    
    message_dict = dict()
    
    zmq_thread = threading.Thread(target=zmq_listener, args=(socket, message_dict))
    zmq_thread.daemon = True  # Ensures thread exits when the program exits
    zmq_thread.start()
    
    try:
        await asyncio.gather(
            spade.wait_until_finished(agent),
            spade.wait_until_finished(agent1),
        )
    finally:
        # Stop the agents cleanly
        await agent.stop()
        await agent1.stop()
    

if __name__ == "__main__":
    spade.run(main())
    



        

    
    
