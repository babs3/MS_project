# station_agent.py
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message


class StationAgent(Agent):
    class ReceiveBikeUpdates(CyclicBehaviour):
        async def run(self):
            msg = await self.receive(timeout=10)
            if msg:
                print(f"[{self.agent.agent_name}] Received: {msg.body}")

    def __init__(self, jid, password):
        super().__init__(jid, password)
        self.agent_name = self.jid.resource

    async def setup(self):
        print(f" - {self.agent_name} is starting.")
        self.add_behaviour(self.ReceiveBikeUpdates())
