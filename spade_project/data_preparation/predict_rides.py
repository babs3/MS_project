import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import seaborn as sns
import matplotlib.pyplot as plt
import random

def main():
    num_of_rides = 50000

    # Load the dataset
    df = pd.read_csv('spade_project/datasets/all_trips.csv')

    # Ensure the ride_duration is numeric
    df['ride_duration'] = pd.to_numeric(df['ride_duration'], errors='coerce')
    df.dropna(subset=['ride_duration'], inplace=True)

    # Create 15-minute intervals
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['date'] = df['started_at'].dt.date
    df['15_min_interval'] = df['started_at'].dt.floor('15min')

    # Group by date and 15-minute intervals, and count the number of departures
    departures_per_interval = df.groupby(['date', '15_min_interval']).size().reset_index(name='departures')

    # Extract only the time part for 15-minute intervals
    departures_per_interval['time'] = departures_per_interval['15_min_interval'].dt.time

    # Group by time (15-minute intervals) and compute the average departures across all days
    avg_departures_per_15min = departures_per_interval.groupby('time')['departures'].mean()

    # Fit a KDE for the average departures
    departure_kde = gaussian_kde(avg_departures_per_15min)

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


    # Predict the next rides concurrently
    current_time = pd.Timestamp.now()
    predicted_rides = []
    for i in range(num_of_rides):  # Predict 20 rides
        predicted_ride = predict_next_ride(df, departure_kde, duration_kdes, current_time)
        predicted_rides.append(predicted_ride)

        # Update current time probabilistically, simulating overlapping rides
        current_time = pd.Timestamp.now() #+= pd.Timedelta(minutes=random.uniform(5, 15))
        print(f"Predicted ride {i + 1} at {predicted_ride['started_at']}")

    # Convert the predicted rides to a DataFrame
    predicted_rides_df = pd.DataFrame(predicted_rides)

    # change the start_at and end_time to datetime format
    predicted_rides_df['started_at'] = pd.to_datetime(predicted_rides_df['started_at'])
    predicted_rides_df['end_time'] = pd.to_datetime(predicted_rides_df['end_time'])
    
    save_to_csv(predicted_rides_df, 'spade_project/auxiliar_files/predicted_rides.csv')

    plot_departures(predicted_rides_df)

# Predict next ride details
def predict_next_ride(df, departure_kde, duration_kdes, current_time):
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

    # Predict start time considering the current interval probability
    interval_prob = departure_kde.resample(1)[0][0]
    next_started_at = current_time + pd.Timedelta(minutes=15 * interval_prob)

    # Predict end time
    next_end_time = next_started_at + pd.Timedelta(minutes=ride_duration) #next_started_at + pd.Timedelta(minutes=ride_duration)

    return {
        'started_at': next_started_at,
        'end_time': next_end_time,
        'start_station_id': start_station_id,
        'end_station_id': end_station_id,
        'ride_duration': ride_duration
    }

def print_rides(predicted_rides):
    # Display the predicted rides
    for i, ride in enumerate(predicted_rides):
        print(f"Ride {i + 1}:")
        print(f"  Start Time: {ride['started_at']}")
        print(f"  End Time: {ride['end_time']}")
        print(f"  Start Station ID: {ride['start_station_id']}")
        print(f"  End Station ID: {ride['end_station_id']}")
        print(f"  Ride Duration: {ride['ride_duration']:.2f} minutes")
        print("----------------------------------------")

def save_to_csv(df, path):
    # Save the DataFrame to a CSV file
    df.to_csv(path, index=False)
    print(f"{df} saved to '{path}'.")

def plot_departures(df):
    # Create 15-minute intervals
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['date'] = df['started_at'].dt.date
    df['15_min_interval'] = df['started_at'].dt.floor('15min')
    
    predicted_rides_df = df.copy()
    # Convert 'started_at' to datetime
    predicted_rides_df['started_at'] = pd.to_datetime(predicted_rides_df['started_at'])

    # Create 15-minute intervals for the rides
    predicted_rides_df['15_min_interval'] = predicted_rides_df['started_at'].dt.floor('15min')

    # Extract only the time part (hours and minutes) of the 15-minute intervals
    predicted_rides_df['interval_time'] = predicted_rides_df['15_min_interval'].dt.strftime('%H:%M')

    # Group by the 15-minute intervals and count the number of rides in each interval
    rides_per_interval = predicted_rides_df.groupby('interval_time').size().reset_index(name='ride_count')

    # Plot the number of rides for each 15-minute interval
    plt.figure(figsize=(12, 6))
    plt.plot(rides_per_interval['interval_time'], rides_per_interval['ride_count'], marker='o', linestyle='-', color='b')

    # Set the labels and title
    plt.xlabel('Time of Day (15-Minute Intervals)')
    plt.ylabel('Number of Rides')
    plt.title('Number of Rides for Each 15-Minute Interval in a Day')
    plt.xticks(rotation=45)
    plt.tight_layout()

    # Show the plot
    plt.show()


main()