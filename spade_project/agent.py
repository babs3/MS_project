import spade
from spade.agent import Agent
from spade import wait_until_finished
from behavior import CreateMessageBehaviour

class BikeAgent(Agent):

    async def setup(self):
        print(f"{self.jid} ready!")
        self.add_behaviour(CreateMessageBehaviour(period=5))  # Run every 5 seconds
            
async def main():
    agent = BikeAgent("ms_proj@macaw.me", "1234")
    await agent.start(auto_register=True)
    await wait_until_finished(agent)
    

if __name__ == "__main__":
    spade.run(main())
    



        

    
    
