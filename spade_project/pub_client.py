import asyncio
import slixmpp
import zmq
import threading
import time
import queue
from slixmpp import Message
from slixmpp.exceptions import IqError

from utils import add_or_update_bike


class Broker(slixmpp.ClientXMPP):
    def __init__(self, jid, password):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.add_event_handler("session_start", self.start)
        

    async def start(self, event):
        self.send_presence()
        print("Broker connected to XMPP server and ready!")
        await self.get_roster()
        
        self.register_plugin('xep_0060')  # Enable PubSub
        
        
    
    def publish_message(self, node, message):
        #pubsub_service = f"pubsub.{self.boundjid.domain}"
        print(node)
        try:
            msg = Message()
            # You can add attributes like 'to', 'type', etc., here if needed
            msg['body'] = message
            self.plugin['xep_0060'].publish(self.boundjid.bare, node, payload=msg)
            print(f"- Published message to node '{node}': {message}")
        except Exception as e:
            print(f"Failed to publish message: {e}")
            
def zmq_listener(socket, message_queue):
    while True:
        try:
            message = socket.recv_string()  # Block until message arrives
            print(f"Received message: {message}")
            #message = topic + ',' + agent_name + ',' + str(latitude) + ',' + str(longitude) + ',' + str(resource)
            topic, agent_name, latitude, longitude, resource = message.split(",", 4)  # Split into topic and payload
            
            payload = agent_name + ',' + latitude + ',' + longitude
            # update bike_positions
            add_or_update_bike(agent_name, float(latitude), float(longitude))
            message_queue.put((topic.strip(), payload.strip()))  # Push message to the queue: Messages are added to a queue to be processed by the manager
            
        except zmq.ZMQError as e:
            print(f"ZeroMQ Error: {e}")
            break
        except Exception as e:
            print(f"Error: {e}")

async def manager():
    # Initialize the ZeroMQ context
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:65432")  # Bind to port 5555

    # Initialize the XMPP broker
    xmpp_broker = Broker("ms_proj@macaw.me", "1234") # Connects to the XMPP server with credentials
    xmpp_broker.register_plugin('xep_0030') # Service Discovery
    xmpp_broker.register_plugin('xep_0199') # XMPP Ping
    xmpp_broker.register_plugin('xep_0060')  # Enable PubSub: Publishes received messages to a specific PubSub node using XMPP's PubSub extension
    xmpp_broker.connect()
    
    message_queue = queue.Queue()
    
    zmq_thread = threading.Thread(target=zmq_listener, args=(socket, message_queue))
    zmq_thread.daemon = True  # Ensures thread exits when the program exits
    zmq_thread.start()

    print("Manager is ready. Waiting for messages...")
    
    while True:
        if not message_queue.empty():
            node, payload = message_queue.get()  # Get the message from the queue: Messages in the queue are dequeued and parsed to extract the topic and payload
            print(f"Publishing message: Node: {node}, Payload: {payload}")
            xmpp_broker.publish_message(node, payload)  # Publish the message: The parsed message is published to the corresponding node using the XMPP broker

        await asyncio.sleep(1)  # Avoid busy-waiting, check queue periodically


if __name__ == "__main__":
    asyncio.run(manager())
