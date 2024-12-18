import pandas as pd

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


# Load trips data - static data
trips_data = pd.DataFrame({
    'ride_id': [],
    'started_at': [],
    'ended_at': [],
    'start_station_id': [],
    'end_station_id': [],
    'ride_duration': [],
    'distance': []
})

# Load rides data - static data
rides_data = pd.DataFrame({
    #'ride_id': [],
    'started_at': [],
    'end_time': [],
    'start_station_id': [],
    'end_station_id': [],
    'ride_duration': [],
})

# Read the CSV file into a DataFrame
all_rides = pd.read_csv('./auxiliar_files/some_predicted_rides.csv')
rides_data = all_rides.rename(columns={
    'start_time': 'start_time',
    'end_time': 'end_time',
    'start_station_id': 'start_station_id',
    'end_station_id': 'end_station_id'
})
# Ensure the DataFrame has the correct columns and order
rides_data = rides_data[['start_time', 'end_time', 'start_station_id', 'end_station_id']]

# get the values of start_station_id from rides_data
start_station_id = rides_data['start_station_id'].values
end_station_id = rides_data['end_station_id'].values
station_id = pd.concat([rides_data['start_station_id'], rides_data['end_station_id']], axis=0)
station_id = station_id.unique()
# stay only with the rows that have the station_id in the station_id of station_data
stations_data = stations_data[stations_data['station_id'].isin(station_id)]

# Load bike data
bike_positions = pd.DataFrame({
        'bike_id': [],
        'lat': [],
        'lng': []
    })

def add_or_update_bike(bike_id, curr_station_id):
    print(f"Adding or updating bike {str(bike_id)}.")

    # Read the CSV file into a DataFrame
    bike_positions = pd.read_csv('./auxiliar_files/bike_positions.csv')
    bike_positions = bike_positions.rename(columns={ # without this it will not work dont know why
        'bike_id': 'bike_id',
        'curr_station_id': 'curr_station_id'
    })
    # Ensure the DataFrame has the correct columns and order
    bike_positions = bike_positions[['bike_id', 'curr_station_id']]

    exists = False
    for id in bike_positions['bike_id'].values:
        if str(id) == str(bike_id):
            print("Bike already exists")
            # Update existing bike
            bike_positions.loc[bike_positions['bike_id'] == id, 'curr_station_id'] = float(curr_station_id)  # or the appropriate type
            exists = True
            break
    
    if not exists:
        print("Bike does not exist")
        # Add new bike using a dictionary
        bike_positions.loc[len(bike_positions)] = {'bike_id': bike_id, 'curr_station_id': curr_station_id}

    # Check if the bike_id is already in the DataFrame

    # Save the updated DataFrame to a CSV file
    bike_positions.to_csv('./auxiliar_files/bike_positions.csv', index=False)


def delete_bike(bike_id):
    print(f"Deleting bike {str(bike_id)}.")

    # Read the CSV file into a DataFrame
    bike_positions = pd.read_csv('./auxiliar_files/bike_positions.csv')
    bike_positions = bike_positions.rename(columns={ # without this it will not work dont know why
        'bike_id': 'bike_id',
        'curr_station_id': 'curr_station_id'
    })
    # Ensure the DataFrame has the correct columns and order
    bike_positions = bike_positions[['bike_id', 'curr_station_id']]

    # Check if the bike_id exists in the DataFrame
    if str(bike_id) in bike_positions['bike_id'].astype(str).values:
        # Delete the bike
        bike_positions = bike_positions[bike_positions['bike_id'].astype(str) != str(bike_id)]
        print("Bike deleted")
    else:
        print("Bike does not exist")

    # Save the updated DataFrame to a CSV file
    bike_positions.to_csv('./auxiliar_files/bike_positions.csv', index=False)
    
    
def update_bike_counts():
    # Load bike positions
    bike_positions = pd.read_csv('./auxiliar_files/bike_positions.csv')

    # Count bikes at each station
    bike_counts = bike_positions.groupby('curr_station_id').size()

    # Map counts to stations_data
    stations_data['bike_count'] = stations_data['station_id'].map(bike_counts).fillna(0).astype(int)
