# MS_project

First navigate to spade_project folder by doing:
`cd .\spade_project\`

To run the project you should first put *tripdata.csv* file from discord in datasets folder and run the notebook *clean_data.ipynb* to create csv files *all_stations* and *all_trips* (the last is not used for now).

Then you may execute the command to run the project:
`make run`

**Be carefull!** Do not send any csv files to github, because they are too large, so the commit will be stuck locally. You should always run `make clean` to delete files from the *datasets* folder before you want to commit something.
