# Shared data structure - hardcoded for now
import pandas as pd


bike_positions = {}

# Load station data
stations_data = pd.DataFrame({
    'station_id': [0, 1],
    'station_name': ['station_0', 'station_1'],
    'lat': [40.7128, 40.7064],
    'lng': [-74.0060, -74.0099]
})