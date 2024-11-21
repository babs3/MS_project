# MS_project

First navigate to spade_project folder by doing:
`cd .\spade_project\`

To run the project you should first put *tripdata.csv* file from discord in datasets folder and run the notebook *clean_data.ipynb* to create csv files *all_stations* and *all_trips* (the last is not used for now).

In project current state it only works with *some_stations.csv* dataset. This is a file you should create inside *datasets* folder (because git is ignoring all csv files to prevent crashes) and should contain the following:
```
station_id,station_name,lat,lng
2.0,Buckingham Fountain,41.87650827549585,-87.62054237689713
3.0,Shedd Aquarium,41.86719997092317,-87.61535300068208
4.0,Burnham Harbor,41.85625792166873,-87.61333879465181
```

Then you may execute the command to run the project:
`make run`