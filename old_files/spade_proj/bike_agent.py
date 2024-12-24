# bike_agent.py
import asyncio
import math
import random
import pandas as pd
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

import spade_project.old_files.spade_proj.message as message
from spade_project.old_files.spade_proj.behavior import CreateMessageBehaviour

class BikeAgent(Agent):

    def __init__(self, jid, password, start_time, end_time, start_station, end_station): #,manager_jid
        super().__init__(jid, password)
        self.start_time = pd.Timestamp(start_time)
        self.end_time = pd.Timestamp(end_time)
        self.current_station = start_station  # e.g., 'station_1@jabbim.com'
        self.start_station = start_station
        self.end_station = end_station
        #self.manager_jid = manager_jid  # JID of ManagerAgent
        self.agent_name = self.jid.resource


    async def setup(self):
        print(f"Bike agent {self.agent_name} is starting at station {self.current_station}.")
        self.add_behaviour(CreateMessageBehaviour(period=5))  # Run every 5 seconds

