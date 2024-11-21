# Shared data structure - hardcoded for now
import pandas as pd


bike_positions = {}

# Load station data
stations_data = pd.DataFrame({
    'station_id': [],
    'station_name': [],
    'lat': [],
    'lng': []
})


# Read the CSV file into a DataFrame
all_stations = pd.read_csv('./datasets/all_stations.csv')

stations_data = all_stations.rename(columns={ # without this it will not work dont know why
    'station_id': 'station_id',
    'station_name': 'station_name',
    'lat': 'lat',
    'lng': 'lng'
})

# Ensure the DataFrame has the correct columns and order
stations_data = stations_data[['station_id', 'station_name', 'lat', 'lng']]

# Display the first few rows of the stations_data DataFrame
#print(stations_data)
