import asyncio
import slixmpp
import zmq
import threading
import time
import queue
from slixmpp import Message
from slixmpp.exceptions import IqError
from slixmpp.exceptions import IqError, IqTimeout
import message

class Broker(slixmpp.ClientXMPP):
    def __init__(self, jid, password, node):
        slixmpp.ClientXMPP.__init__(self, jid, password)
        self.node = node
        self.add_event_handler("session_start", self.start)
        self.add_event_handler("pubsub_publish", self.pubsub_event_handler)
        

    async def start(self, event):
        self.send_presence()
        print("Broker connected to XMPP server and ready!")
        await self.get_roster()
        
        self.register_plugin('xep_0060')  # Enable PubSub
        #self.plugin['xep_0060'].subscribe(self.boundjid.bare, self.node)

    # When a message is published to this node (by pub_client.py), the pubsub_event_handler is triggered:
    async def pubsub_event_handler(self, msg):
        items = msg['pubsub_event']['items']
        for item in items['substanzas']:
            item_xml = item.xml  # This is an XML element
            print(f"Received item ID: {item['id']}") # Extracts the message body and additional metadata
            
            # Processes the data as required (e.g., forwards it to another system):
            message_elem = item_xml.find("{jabber:client}message")
            body_elem = message_elem.find('{jabber:client}body')
            print(body_elem.text)
            await message.async_message_sub('PUSH', 'location_updates', body_elem.text, item['id'])

            

async def manager():
    
    # Initialize the XMPP broker
    xmpp_broker = Broker("ms_proj@macaw.me", "1234", "location_updates") # Connects to the same XMPP server as the publisher and Subscribes to a specified PubSub node
    xmpp_broker.register_plugin('xep_0030') # Service Discovery
    xmpp_broker.register_plugin('xep_0199') # XMPP Ping
    xmpp_broker.register_plugin('xep_0060')  # Enable PubSub
    xmpp_broker.register_plugin('xep_0059')  # Enable PubSub
    xmpp_broker.connect()
   
    # await asyncio.sleep(5)
    # print("Manager is ready. Waiting for messages...")
    
    while(True):
        await asyncio.sleep(1)
    

if __name__ == "__main__":
    asyncio.run(manager())
