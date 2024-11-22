# bike_agent.py
import asyncio
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

class BikeAgent(Agent):
    class MoveBehaviour(CyclicBehaviour):
        async def run(self):
            # Define the step size for each movement
            step_size = 0.0001

            # Calculate the direction vector to the destination
            delta_lat = self.agent.destination_latitude - self.agent.latitude
            delta_lng = self.agent.destination_longitude - self.agent.longitude

            # Calculate the distance to the destination
            distance = (delta_lat**2 + delta_lng**2)**0.5

            if distance > step_size:
                # Normalize the direction vector and move by the step size
                direction_lat = delta_lat / distance
                direction_lng = delta_lng / distance

                self.agent.latitude += direction_lat * step_size
                self.agent.longitude += direction_lng * step_size
            else:
                # Stop at the destination if within step size
                self.agent.latitude = self.agent.destination_latitude
                self.agent.longitude = self.agent.destination_longitude
                print(f"{self.agent.agent_name} has reached the destination!")
                await asyncio.sleep(3)  # Pause for 3 seconds before next action
                return  # Stop moving further

            # Create location update message
            location_update = f"{self.agent.agent_name},{self.agent.latitude:.6f},{self.agent.longitude:.6f}"
            print(location_update)

            # Send location update to the ManagerAgent
            msg = Message(to=self.agent.manager_jid)  # Send to the ManagerAgent
            msg.body = location_update
            await self.send(msg)

            # Wait before the next movement
            await asyncio.sleep(1)  # Pause for 1 second to simulate movement


    def __init__(self, jid, password, start_station, start_latitude, start_longitude, end_latitude, end_longitude, manager_jid):
        super().__init__(jid, password)
        self.latitude = start_latitude
        self.longitude = start_longitude
        self.destination_latitude = end_latitude
        self.destination_longitude = end_longitude
        self.current_station = start_station  # e.g., 'station_1@jabbim.com'
        self.manager_jid = manager_jid  # JID of ManagerAgent
        self.agent_name = self.jid.resource


    async def setup(self):
        print(f"Bike agent {self.agent_name} is starting at station {self.current_station}.")
        self.add_behaviour(self.MoveBehaviour())
