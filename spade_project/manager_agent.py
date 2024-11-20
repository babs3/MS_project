from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class ManagerAgent(Agent):
    class UpdatePositionBehaviour(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)  # Wait for a message
            if msg:
                data = msg.body.split(",")
                bike_id, lat, lng = data[0], float(data[1]), float(data[2])
                self.agent.bike_positions[bike_id] = (lng, lat)  # Update bike_positions (note lng, lat order)
                print(f"[Manager] Updated position of {bike_id} to ({lat}, {lng})")

    async def setup(self):
        self.add_behaviour(self.UpdatePositionBehaviour())
    
    def __init__(self, jid, password, bike_positions):
        super().__init__(jid, password)
        print(f"Manager agent {self.name} is starting.")
        self.bike_positions = bike_positions
