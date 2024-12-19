# MS_project

The purpose of this project is to build a simulation model of a shared eletrical bike system that manages to redistribute bikes between stations after X time lapse ending with a high median of bikes per station. In order to make communication between agents (bikes, stations), protocol XMPP is used. The agents then proceed to enact their behaviors congruent with a pre processed dataset [Chicago Dataset](https://divvy-tripdata.s3.amazonaws.com/index.html) making the base model a descriptive model. The second model attempts to achieve the same purpose only by changing the controllable variables values making it a speculative model. A second scenario for this model introduces new endogenous variables in the form of incentives for the agents to change their behaviors.


In project current state it only works with *some_stations.csv*  and  *some_trips.csv* datasets.

Later, to run the project you should first put *tripdata.csv* file from discord in datasets folder and run the notebook *clean_data.ipynb* to create csv files *all_stations* and *all_trips* (the last is not used for now).


## Start and Run the project

### 1 -  Start the web browser for ploty visualization

1.  To start the ploty web server you should open a new terminal and navigate to spade_project folder by doing: `cd .\spade_project\`

2. Then you should run `make run_host` to run the script that will start the server.
3 - Then you should open the link `http://127.0.0.1:8050/` in the browser.

    ![alt text](images/ploty-map.png)

### 2 - Run the SPADE project
1.  `cd .\spade_project\` then run `python .\agent.py\`, `python .\sub_client.py\`, `python .\pub_client.py\`, the order is irrelevant.

---
---

## Update of 12/12/2024:
- The project does not show the movement of bikes anymore, for now you will only see blue points in the host, representing stations.
- the `bike_positions.csv` file kepts the bikes ids and the current station where it belongs (later this can be stored in bike agent I think)
- To see thing running in terminal, you should:
    - run the `predict_rides.py` file to populate the `some_predicted_rides.csv`. It will generate rides for the next minutes.
    - open two terminals to run the `agent.py` and `pub_client.py` files. The terminals output what is currently hapenning.

**Next steps:**  make the stations appear differently in the host, taking into account the number of bikes.

## Update of 19/12/2024:
- Stations appear differently in the host, taking into account the number of bikes.
    - Red Station: 0 bikes
    - Yellow Station: 1 - 3 bikes
    - Green Station: 4 and more bikes

**Notes from the teacher:**  
- we should keep the station position fixed
- the metrix of the system is the availability rate (the capacity of the bikes with the bikes in the station) 
- capacity should be the same for all stations and the bikes in the station should be 70% of the capacity (max 15 bikes per station, but in each one 10 bikes inside)

**Next Steps**
- run the basic scenario (picking up, time duration and drop off)
- measure availability rate
- apply cost function to ask users to leave bikes in other stations that needs bikes, by offering a discound 
