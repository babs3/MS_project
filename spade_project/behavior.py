from spade.behaviour import PeriodicBehaviour
import socket
import zmq.asyncio
import asyncio
import message

class CreateMessageBehaviour(PeriodicBehaviour):
    async def run(self):
        #topic = "location_updates"
        #payload = "Agent is that (lat lng)"
        #await message.async_message('PUSH', topic, payload, self.agent.jid.resource)
        print(f"Agent {self.agent.jid.resource} is sending messages...")

        # Create location update message
        #location_update = f"{self.agent.agent_name},{self.agent.latitude:.6f},{self.agent.longitude:.6f}"
        #print(f"--message sent: {location_update}")

        # Send location update to the ManagerAgent
        topic = "location_updates"
        await message.async_message('PUSH', topic, self.agent.agent_name, self.agent.latitude, self.agent.longitude, self.agent.destination_latitude, self.agent.destination_longitude, self.agent.jid.resource)
        # Send location update to the ManagerAgent
        #msg = Message(to=self.agent.manager_jid)  # Send to the ManagerAgent
        #msg.body = location_update
        #await self.send(msg)

        # Wait before the next movement
        await asyncio.sleep(1)  # Pause for 1 second to simulate movement
    

    

        