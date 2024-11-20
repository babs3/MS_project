# bike_agent.py
import asyncio
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class BikeAgent(Agent):
    class MoveBehaviour(CyclicBehaviour):
        async def run(self):
            # Simulate movement by updating latitude and longitude
            self.agent.latitude += random.uniform(-0.001, 0.001)
            self.agent.longitude += random.uniform(-0.001, 0.001)

            # Create location update message
            location_update = f"{self.agent.name},{self.agent.latitude:.6f},{self.agent.longitude:.6f}"
            print(location_update)
            
            # Send location update to the ManagerAgent
            msg = Message(to=self.agent.manager_jid)  # Send to the ManagerAgent
            msg.body = location_update
            await self.send(msg)
            
            # Wait before next movement
            await asyncio.sleep(3)  # Pause for 3 seconds

    def __init__(self, jid, password, start_station, latitude, longitude, manager_jid):
        super().__init__(jid, password)
        self.latitude = latitude
        self.longitude = longitude
        self.current_station = start_station  # e.g., 'station_1@jabbim.com'
        self.manager_jid = manager_jid  # JID of ManagerAgent

    async def setup(self):
        print(f"Bike agent {self.name} is starting at station {self.current_station}.")
        self.add_behaviour(self.MoveBehaviour())
