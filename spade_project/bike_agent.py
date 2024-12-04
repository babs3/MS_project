# bike_agent.py
import asyncio
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

import message
from behavior import CreateMessageBehaviour

class BikeAgent(Agent):

    def __init__(self, jid, password, start_station, start_latitude, start_longitude, end_latitude, end_longitude): #,manager_jid
        super().__init__(jid, password)
        self.latitude = start_latitude
        self.longitude = start_longitude
        self.destination_latitude = end_latitude
        self.destination_longitude = end_longitude
        self.current_station = start_station  # e.g., 'station_1@jabbim.com'
        #self.manager_jid = manager_jid  # JID of ManagerAgent
        self.agent_name = self.jid.resource


    async def setup(self):
        print(f"Bike agent {self.agent_name} is starting at station {self.current_station}.")
        #self.add_behaviour(self.MoveBehaviour())
        self.add_behaviour(CreateMessageBehaviour(period=5))  # Run every 5 seconds

