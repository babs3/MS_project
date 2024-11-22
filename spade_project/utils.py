import pandas as pd

# Load station data - static data
stations_data = pd.DataFrame({
    'station_id': [],
    'station_name': [],
    'lat': [],
    'lng': []
})
# Read the CSV file into a DataFrame
all_stations = pd.read_csv('./auxiliar_files/some_stations.csv')
stations_data = all_stations.rename(columns={ # without this it will not work dont know why
    'station_id': 'station_id',
    'station_name': 'station_name',
    'lat': 'lat',
    'lng': 'lng'
})
# Ensure the DataFrame has the correct columns and order
stations_data = stations_data[['station_id', 'station_name', 'lat', 'lng']]

# Load bike data
bike_positions = pd.DataFrame({
        'bike_id': [],
        'lat': [],
        'lng': []
    })


def add_or_update_bike(bike_id, lat, lng):

    # Read the CSV file into a DataFrame
    bike_positions = pd.read_csv('./auxiliar_files/bike_positions.csv')
    bike_positions = bike_positions.rename(columns={ # without this it will not work dont know why
        'bike_id': 'bike_id',
        'lat': 'lat',
        'lng': 'lng'
    })
    # Ensure the DataFrame has the correct columns and order
    bike_positions = bike_positions[['bike_id', 'lat', 'lng']]


    # Check if the bike_id is already in the DataFrame
    if bike_id in bike_positions['bike_id'].values:
        # Update existing bike
        bike_positions.loc[bike_positions['bike_id'] == bike_id, ['lat', 'lng']] = [lat, lng]
    else:
        # Add new bike using a dictionary
        bike_positions.loc[len(bike_positions)] = {'bike_id': bike_id, 'lat': lat, 'lng': lng}

    # Save the updated DataFrame to a CSV file
    bike_positions.to_csv('./auxiliar_files/bike_positions.csv', index=False)

