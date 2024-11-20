# station_agent.py
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class StationAgent(Agent):
    class ReceiveBikeUpdates(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"[{self.agent.name}] Received: {msg.body}")
    
    async def setup(self):
        print(f"{self.name} is starting.")
        self.add_behaviour(self.ReceiveBikeUpdates())
