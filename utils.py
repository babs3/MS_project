import pandas as pd

from station_agent import Station

# Load station data - static data
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

# Load rides data - static data
rides_data = pd.DataFrame({
    'started_at': [],
    'start_station_id': [],
    'end_station_id': []
})

# Read the CSV file into a DataFrame
all_rides = pd.read_csv('./small_datasets/some_predicted_rides1.csv')
rides_data = all_rides.rename(columns={
    '15_min_interval': 'start_time',
    'departure_station_id': 'start_station_id',
    'chosen_arrival_station': 'end_station_id'
})
# Ensure the DataFrame has the correct columns and order
rides_data = rides_data[['start_time', 'start_station_id', 'end_station_id']]

# get the values of start_station_id from rides_data
start_station_id = rides_data['start_station_id'].values
end_station_id = rides_data['end_station_id'].values
station_id = pd.concat([rides_data['start_station_id'], rides_data['end_station_id']], axis=0)
station_id = station_id.unique()
# stay only with the rows that have the station_id in the station_id of station_data
stations_data = stations_data[stations_data['station_id'].isin(station_id)]

# Initialize Stations
print("Initializing Stations...")
# Create station objects
stations = []
for _, row in stations_data.iterrows():
    station = Station(
        station_id=row['station_id'],
        station_name=row['station_name'],
        lat=row['lat'],
        lng=row['lng'],
        initial_bike_count=10  # Example initial bike count
    )
    stations.append(station)

# Example: Log the state of all stations
for station in stations:
    station.log_state()

print("All stations initialized.")
