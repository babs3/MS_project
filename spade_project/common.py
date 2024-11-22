import pandas as pd

#bike_positions = {}

# Display the first few rows of the stations_data DataFrame
#print(stations_data)




def add_or_update_bike(bike_id, lat, lng):

    bike_positions = pd.DataFrame({
        'bike_id': [],
        'lat': [],
        'lng': []
    })

    # Read the CSV file into a DataFrame
    bike_positions = pd.read_csv('./datasets/bike_positions.csv')

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
    bike_positions.to_csv('./datasets/bike_positions.csv', index=False)

