# station_agent.py
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour

class StationAgent(Agent):
    class MonitorBehaviour(CyclicBehaviour):
        async def run(self):
            print(f"{self.agent.name} is monitoring bikes.")
            # Additional logic to monitor bike availability, check-ins, etc.
            await self.agent.pause(10)  # pause for 10 seconds to simulate real-time updates

    async def setup(self):
        print(f"Station agent {self.name} starting...")
        self.add_behaviour(self.MonitorBehaviour())
 