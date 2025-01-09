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
all_rides = pd.read_csv('./small_datasets/descriptive_rides.csv')
#all_rides = pd.read_csv('./small_datasets/rebalanced0.2.csv')
#all_rides = pd.read_csv('./small_datasets/rebalanced0.4.csv')
#all_rides = pd.read_csv('./small_datasets/rebalanced0.6.csv')
#all_rides = pd.read_csv('./small_datasets/rebalanced0.8.csv')
#all_rides = pd.read_csv('./small_datasets/rebalanced100.csv')
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
print("\nInitializing Stations...")
# Create station objects
stations = []
for _, row in stations_data.iterrows():
    station = Station(
        station_id=row['station_id'],
        station_name=row['station_name'],
        lat=row['lat'],
        lng=row['lng'],
        initial_bike_count=22,  # Example initial bike count
        capacity=35   # Set capacity for each station

    )
    stations.append(station)

# Example: Log the state of all stations
#for station in stations:
    #station.log_state()

#print("All stations initialized.")

def calculate_availability_rate():
    total_bikes = sum(station.bike_count for station in stations)
    total_capacity = sum(station.capacity for station in stations)
    system_availability_rate = total_bikes / total_capacity if total_capacity > 0 else 0

    # Log individual station availability rates
    #for station in stations:
        #station_availability_rate = station.bike_count / station.capacity
        #print(f"{station.station_name}: {station_availability_rate:.2%}")

    return system_availability_rate


def get_insights():
        
    # Insights of stations after simulation
    color_stations_dict = {
        'red': 0,
        'orange': 0,
        'green': 0,
        'blue': 0
    }
    # Insights bikes per coloured station
    bikes_per_coloured_station_dict = {
        'red': 0,
        'orange': 0,
        'green': 0,
        'blue': 0
    }
    
    for station in stations:
        if station.bike_count == 0:
            color_stations_dict['red'] += 1
        elif station.bike_count <= 20:
            color_stations_dict['orange'] += 1
            bikes_per_coloured_station_dict['orange'] += station.bike_count
        elif station.bike_count <= 35:
            color_stations_dict['green'] += 1
            bikes_per_coloured_station_dict['green'] += station.bike_count
        else:
            color_stations_dict['blue'] += 1
            bikes_per_coloured_station_dict['blue'] += station.bike_count

    print("\nStation Insights:")
    for color, count in color_stations_dict.items():
        print(f"{count} stations with {color} color")

    print("\nBikes per station Insights:")
    for color, count in bikes_per_coloured_station_dict.items():
        print(f"{count} bikes in {color} stations")
