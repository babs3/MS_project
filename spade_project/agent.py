import spade
from spade.agent import Agent
from spade import wait_until_finished
from behavior import CreateMessageBehaviour
import asyncio

class BikeAgent(Agent):

    async def setup(self):
        print(f"{self.jid} ready!")
        self.add_behaviour(CreateMessageBehaviour(period=5))  # Run every 5 seconds
            
async def main():
    agent = BikeAgent("ms_proj@macaw.me/0", "1234")
    await agent.start(auto_register=True)
    agent1 = BikeAgent("ms_proj@macaw.me/1", "1234")
    await agent1.start(auto_register=True)
    try:
        await asyncio.gather(
            spade.wait_until_finished(agent),
            spade.wait_until_finished(agent1),
        )
    finally:
        # Stop the agents cleanly
        await agent.stop()
        await agent1.stop()
    

if __name__ == "__main__":
    spade.run(main())
    



        

    
    
