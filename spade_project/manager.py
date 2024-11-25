import asyncio
import slixmpp
import zmq
import time
from slixmpp import Message


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
            print(f"Published message to node '{node}': {message}")
        except Exception as e:
            print(f"Failed to publish message: {e}")

async def manager():
    # Initialize the ZeroMQ context
    context = zmq.Context()
    socket = context.socket(zmq.PULL)
    socket.bind("tcp://*:65432")  # Bind to port 5555

    # Initialize the XMPP broker
    xmpp_broker = Broker("ms_proj@macaw.me", "1234")
    xmpp_broker.register_plugin('xep_0030') # Service Discovery
    xmpp_broker.register_plugin('xep_0199') # XMPP Ping
    xmpp_broker.register_plugin('xep_0060')  # Enable PubSub
    xmpp_broker.plugin['xep_0060'].create_node(xmpp_broker.boundjid.bare, 'location_updates')
    #await xmpp_broker.create_node('location_updates')
    xmpp_broker.connect()

    print("Manager is ready. Waiting for messages...")

    # Main loop to receive messages and publish to XMPP
    while True:
        try:
            message = socket.recv_string()
            print(f"Received message: {message}")
            node, payload = message.split(",", 1)  # Split into topic and payload
            xmpp_broker.publish_message(node.strip(), payload.strip())
        except zmq.ZMQError as e:
            print(f"ZeroMQ Error: {e}")
            break
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    asyncio.run(manager())
