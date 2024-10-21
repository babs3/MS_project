import pandas as pd
import numpy as np

def init():
    # Load your dataset
    df = pd.read_csv("tripdata.csv")
    # Convert the started_at and ended_at columns to datetime
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['ended_at'] = pd.to_datetime(df['ended_at'])
    
    df['ride_duration'] = (df['ended_at'] - df['started_at']).dt.total_seconds() / 60
    
    df_cleaned = df[df['ride_duration'] > 0].copy()

    df_cleaned['distance'] = df_cleaned.apply(lambda row: haversine(row['start_lat'], row['start_lng'], row['end_lat'], row['end_lng']), axis=1)
  # Group by start_station_id and end_station_id
    grouped = df_cleaned.groupby(['start_station_id', 'end_station_id']).agg(
    avg_distance=('distance', 'mean'),
    avg_duration=('ride_duration', 'mean'),
    #ride_count=('ride_id', 'count'),
    shortest_duration=('ride_duration', 'min')
    ).reset_index()
    
    df_cleaned = df_cleaned.merge(grouped[['start_station_id', 'end_station_id', 'shortest_duration', 'avg_distance']], 
                on=['start_station_id', 'end_station_id'], 
                how='left')

    # # Calculate the irregularity factor: duration / shortest duration
    df_cleaned['irregularity_factor'] = df_cleaned['ride_duration'] / df_cleaned['shortest_duration']

    # # Adjust the average distance using the irregularity factor
    df_cleaned['adjusted_distance'] = df_cleaned['avg_distance'] * df_cleaned['irregularity_factor']

    # # Now, calculate the adjusted average distance for each start/end station pair
    final_grouped = df_cleaned.groupby(['start_station_id', 'end_station_id']).agg(
        adjusted_avg_distance=('adjusted_distance', 'mean'),
        avg_duration=('ride_duration', 'mean'),
        #ride_count=('ride_id', 'count')
    ).reset_index()
    
    df_cleaned = df_cleaned.merge(final_grouped[['start_station_id', 'end_station_id', 'adjusted_avg_distance', 'avg_duration']], 
                on=['start_station_id', 'end_station_id'], 
                how='left')

    return df_cleaned

def haversine(lat1, lon1, lat2, lon2):
    # Convert degrees to radians
    lat1, lon1, lat2, lon2 = map(np.radians, [lat1, lon1, lat2, lon2])
    
    # Haversine formula
    dlat = lat2 - lat1
    dlon = lon2 - lon1
    a = np.sin(dlat / 2)**2 + np.cos(lat1) * np.cos(lat2) * np.sin(dlon / 2)**2
    c = 2 * np.arcsin(np.sqrt(a))
    
    # Radius of Earth in kilometers (use 6371 for km, 3956 for miles)
    r = 6371  
    return c * r

cleaned = init()

#Specify the path where you want to save the CSV file
output_path = "./output/cleaned_data.csv"

#Export the grouped DataFrame to a CSV file
cleaned.to_csv(output_path, index=False)

