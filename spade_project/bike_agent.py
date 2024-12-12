# bike_agent.py
import asyncio
import math
import random
from spade.agent import Agent
from spade.behaviour import CyclicBehaviour
from spade.message import Message

import message
from behavior import CreateMessageBehaviour

class BikeAgent(Agent):

    def __init__(self, jid, password, started_at, start_station, start_latitude, start_longitude, end_latitude, end_longitude, ride_duration): #,manager_jid
        super().__init__(jid, password)
        self.started_at = started_at
        self.latitude = start_latitude
        self.longitude = start_longitude
        self.destination_latitude = end_latitude
        self.destination_longitude = end_longitude
        self.ride_duration = ride_duration
        self.current_station = start_station  # e.g., 'station_1@jabbim.com'
        #self.manager_jid = manager_jid  # JID of ManagerAgent
        self.agent_name = self.jid.resource


    async def setup(self):
        print(f"Bike agent {self.agent_name} is starting at station {self.current_station}.")

        
        # Define the coordinates of the start and end stations
        start_station = (self.latitude, self.longitude)
        end_station = (self.destination_latitude, self.destination_longitude)

        # Define the ride duration in seconds
        ride_duration = self.ride_duration

        # Calculate the Euclidean distance between the start and end stations
        distance = math.sqrt((end_station[0] - start_station[0])**2 + (end_station[1] - start_station[1])**2)

        # Calculate the step size
        self.step_size = distance / ride_duration
        print(f"- Step size of {self.agent_name}: {self.step_size}")


        #self.add_behaviour(self.MoveBehaviour())
        self.add_behaviour(CreateMessageBehaviour(period=5))  # Run every 5 seconds

