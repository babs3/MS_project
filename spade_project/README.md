# MS_project


In project current state it only works with *some_stations.csv*  and  *some_trips.csv* datasets.

Later, to run the project you should first put *tripdata.csv* file from discord in datasets folder and run the notebook *clean_data.ipynb* to create csv files *all_stations* and *all_trips* (the last is not used for now).

## Start and Run the project

#### 1 -  Start the web browser for ploty visualization

1.  To start the ploty web server you should open a new terminal and navigate to spade_project folder by doing: `cd .\spade_project\`

2. Then you should run `make run_host` to run the script that will start the server.
3 - Then you should open the link `http://127.0.0.1:8050/` in the browser.

#### 2 - Run the SPADE project
1. To run the main script file and be able to see bikes moving you should open another terminal and navigate to spade_project folder by doing: `cd .\spade_project\`

2. Then you just have to type `make run` and the project will run