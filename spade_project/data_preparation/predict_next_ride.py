import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import seaborn as sns
import matplotlib.pyplot as plt
import random

# Load the dataset
df = pd.read_csv('spade_project/datasets/all_trips.csv')

# Ensure the ride_duration is numeric
df['ride_duration'] = pd.to_numeric(df['ride_duration'], errors='coerce')
df.dropna(subset=['ride_duration'], inplace=True)

# Group by start_station_id to model start time probabilities
avg_departures_per_hour = df.groupby('start_station_id')['ride_duration'].count() / (24 * 60)

# Fit a KDE for average departures
departure_kde = gaussian_kde(avg_departures_per_hour)

# Fit KDEs for ride durations by station pairs
duration_distributions = df.groupby(['start_station_id', 'end_station_id'])['ride_duration']
duration_kdes = {}

for (start_id, end_id), durations in duration_distributions:
    durations = durations.to_numpy()  # Convert to a NumPy array for easier processing
    if len(durations) > 1 and durations.std() > 0:  # Ensure there are at least two data points and non-zero variance
        duration_kdes[(start_id, end_id)] = gaussian_kde(durations)
    else:
        # Fallback: Store the mean duration if variance is zero or not enough data
        duration_kdes[(start_id, end_id)] = durations.mean() if len(durations) > 0 else None

# Predict next ride details
def predict_next_ride(df, departure_kde, duration_kdes, current_time):
    # Predict time gap to next ride
    random_departure = departure_kde.resample(1)[0][0]  # Sample a random departure time gap in minutes
    next_start_time = current_time + pd.Timedelta(minutes=random_departure)

    # Predict start and end station
    start_station_id = random.choice(list(df['start_station_id'].unique()))
    possible_end_stations = df[df['start_station_id'] == start_station_id]['end_station_id'].unique()
    if len(possible_end_stations) > 0:
        end_station_id = random.choice(list(possible_end_stations))
    else:
        end_station_id = random.choice(list(df['end_station_id'].unique()))  # Fallback

    # Predict ride duration
    if (start_station_id, end_station_id) in duration_kdes:
        kde_or_mean = duration_kdes[(start_station_id, end_station_id)]
        if isinstance(kde_or_mean, gaussian_kde):
            ride_duration = kde_or_mean.resample(1)[0][0]
        elif kde_or_mean is not None:
            ride_duration = kde_or_mean
        else:
            ride_duration = df['ride_duration'].mean()  # Fallback to overall mean
    else:
        ride_duration = df['ride_duration'].mean()  # Fallback to overall mean

    # Predict end time
    next_end_time = next_start_time + pd.Timedelta(minutes=ride_duration)

    return {
        'start_time': next_start_time,
        'end_time': next_end_time,
        'start_station_id': start_station_id,
        'end_station_id': end_station_id,
        'ride_duration': ride_duration
    }

# Example simulation loop
current_time = pd.Timestamp.now()
for i in range(5):  # Predict 5 rides sequentially
    predicted_ride = predict_next_ride(df, departure_kde, duration_kdes, current_time)
    print(f"Ride {i + 1}:")
    print(f"  Start Time: {predicted_ride['start_time']}")
    print(f"  End Time: {predicted_ride['end_time']}")
    print(f"  Start Station ID: {predicted_ride['start_station_id']}")
    print(f"  End Station ID: {predicted_ride['end_station_id']}")
    print(f"  Ride Duration: {predicted_ride['ride_duration']:.2f} minutes")
    print("----------------------------------------")

    # Update current time to the end time of the predicted ride
    current_time = predicted_ride['end_time']
