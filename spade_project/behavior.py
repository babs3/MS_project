from spade.behaviour import PeriodicBehaviour
import socket
import zmq.asyncio
import asyncio
import message

class CreateMessageBehaviour(PeriodicBehaviour):
    async def run(self):
        topic = "location_updates"
        payload = "Agent is that (lat lng)"
        await message.async_message('PUSH', topic, payload, self.agent.jid.resource)
        

        

            