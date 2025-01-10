import time
import pandas as pd
import numpy as np
from scipy.stats import gaussian_kde
import seaborn as sns
import matplotlib.pyplot as plt
import random
import os
import dask.dataframe as dd
script_dir = os.path.dirname(__file__)
file_path = os.path.join(script_dir, '../datasets/all_trips.csv')
output_path = os.path.join(script_dir, '../small_datasets/some_predicted_rides.csv')
output_path1 = os.path.join(script_dir, '../small_datasets/some_predicted_rides1.csv')
output_path2 = os.path.join(script_dir, '../small_datasets/rebalanced0.2.csv')

def main():
    num_of_rides = 5000

    # Load the dataset
    df = pd.read_csv(file_path)
    
    # Ensure the ride_duration is numeric
    df['ride_duration'] = pd.to_numeric(df['ride_duration'], errors='coerce')
    df.dropna(subset=['ride_duration'], inplace=True)

    # Create 15-minute intervals
    df['started_at'] = pd.to_datetime(df['started_at'])
    df['date'] = df['started_at'].dt.date
    df['15_min_interval'] = df['started_at'].dt.round('15min').dt.time
    

    # Step 1: Aggregate total departures per date and interval
    grouped = df.groupby(['date', '15_min_interval']).agg(
        total_departures=('ride_duration', 'count')  
    ).reset_index()
    
    
    departures_per_station = (
        df.groupby(['15_min_interval', 'start_station_id','date'])['ride_duration']
        .count()  
        .reset_index(name='departures') 
    )
    
    station_probs = (
        departures_per_station.groupby(['15_min_interval','date'])
        .apply(lambda x: x['departures'] / x['departures'].sum())  
        .reset_index(name='station_probability')
    )
    
    predicted_rides = []
    
    specific_date = pd.to_datetime('2020-08-01')
    

    
    df['date'] = pd.to_datetime(df['date'], errors='coerce')

    # Step 2: Iterate through each unique date
    for date in grouped['date'].unique():
        date_group = grouped[grouped['date'] == date]
        for interval in date_group['15_min_interval']:
            
            interval_data = station_probs[(station_probs['date'] == date) & (station_probs['15_min_interval'] == interval)]
            print(interval_data)
            
            total_departures_at_interval = grouped[(grouped['date'] == date) & (grouped['15_min_interval'] == interval)]
            
            if not total_departures_at_interval.empty:
            
                total_departures_at_interval = total_departures_at_interval['total_departures'].values[0]
                
                
                for _, row in interval_data.iterrows():
                    station_id = row['level_2']
                    station_prob = row['station_probability']
                    
                    
                    predicted_departures = np.random.poisson(total_departures_at_interval * station_prob)

                    
                    predicted_rides.append({
                        'date': date,
                        '15_min_interval': interval,
                        'station_id': station_id,
                        'predicted_rides': predicted_departures
                    })

    #Step 3: Convert to dataframe and filter through the specific date    
    predicted_rides_df = pd.DataFrame(predicted_rides)
   
    predicted_rides_df['date'] = pd.to_datetime(predicted_rides_df['date'], errors='coerce')
    
    filtered_predicted_rides = predicted_rides_df[predicted_rides_df['date'] == specific_date]
    
    #Step 4: Fetch arrivals for the departures 
    arrivals_per_station = df.groupby(['date', '15_min_interval', 'end_station_id']).size().reset_index(name='arrivals')

    arrival_probs = (
        arrivals_per_station.groupby(['date', '15_min_interval'])
        .apply(lambda x: x.assign(arrival_probability=x['arrivals'] / x['arrivals'].sum()))
        .reset_index(drop=True)
    )
    
    filtered_arrival_probs = arrival_probs[arrival_probs['date'] == specific_date]
    
    
    #Step 5: Add the arrivals to departures based on historical data
    predicted_rides_with_arrivals = []
    filtered_arrival_probs.set_index(['date', '15_min_interval'], inplace=True)

    for _, row in filtered_predicted_rides.iterrows():
        departure_date = row['date']
        departure_interval = row['15_min_interval']
        departure_station_id = row['station_id']
        predicted_departures = row['predicted_rides']

        try:
            possible_arrivals = filtered_arrival_probs.loc[(departure_date, departure_interval)]
        except KeyError:
            
            print(f"No possible arrivals for {departure_date}, {departure_interval}")
            continue
        
        print(possible_arrivals)

        
        possible_arrivals = (
            possible_arrivals.groupby('end_station_id')
            .agg({'arrival_probability': 'sum'})
            .reset_index()
        )
        possible_arrivals['normalized_prob'] = (
            possible_arrivals['arrival_probability'] / possible_arrivals['arrival_probability'].sum()
        )

        
        chosen_station_idx = possible_arrivals['normalized_prob'].sample(weights=possible_arrivals['normalized_prob']).index[0]
        chosen_station = possible_arrivals.loc[chosen_station_idx, 'end_station_id']

        
        predicted_rides_with_arrivals.append({
            'date': departure_date,
            '15_min_interval': departure_interval,
            'departure_station_id': departure_station_id,
            'predicted_rides': predicted_departures,
            'chosen_arrival_station': chosen_station
        })

    # Step 6: Create the final DataFrame
    predicted_rides_with_arrivals_df = pd.DataFrame(predicted_rides_with_arrivals)

    # expanded_df = predicted_rides_with_arrivals_df.loc[predicted_rides_with_arrivals_df.index.repeat(predicted_rides_with_arrivals_df['predicted_rides'])].reset_index(drop=True)

    # expanded_df.to_csv(output_path1, index=False)

    rebalanced_df = rebalancing(predicted_rides_with_arrivals_df)
    
    expanded_df = rebalanced_df.loc[rebalanced_df.index.repeat(rebalanced_df['ride'])].reset_index(drop=True)

    expanded_df.to_csv(output_path2, index=False)

 

def rebalancing(predicted_df):
    stations = pd.concat([
        predicted_df['departure_station_id'], 
        predicted_df['chosen_arrival_station']
    ]).unique()
    bike_tracker = {station: 22 for station in stations}
    capacity = 35

    
    rebalanced_rides = []
    

  
    for i, row in predicted_df.iterrows():
    
  
        start_station = row['departure_station_id']
        end_station = row['chosen_arrival_station']
        rides = row['predicted_rides']
        
        # Update bike counts for start and end stations
        bike_tracker[start_station] = max(0, bike_tracker[start_station] - rides)
        bike_tracker[end_station] = min(capacity, bike_tracker[end_station] + rides)

        # Calculate median bikes and demand
        median_bikes = np.median(list(bike_tracker.values()))
        demand = {station: median_bikes - bikes for station, bikes in bike_tracker.items() if bikes < median_bikes}

        # Only redistribute if start station has 12 or more bikes
        if bike_tracker[start_station] >= 12:  
            for _ in range(rides):
                if random.random() < 0.2:  
                    if demand:
                        # Find the 5 highest-demand stations
                        top_demand_stations = sorted(demand, key=demand.get)[:5]

                        # Redistribute to the top 5 stations iteratively
                        for highest_demand_station in top_demand_stations:
                            if bike_tracker[start_station] < 12:  # Stop redistributing if fewer than 12 bikes remain
                                break
                            bike_tracker[highest_demand_station] += 1
                            bike_tracker[start_station] -= 1
                            rebalanced_rides.append({
                                '15_min_interval': row['15_min_interval'],
                                'departure_station_id': start_station,
                                'chosen_arrival_station': highest_demand_station,
                                'ride': 1
                            })
                    else:
                        # No demand stations, send bikes to original end station
                        rebalanced_rides.append({
                            '15_min_interval': row['15_min_interval'],
                            'departure_station_id': start_station,
                            'chosen_arrival_station': end_station,
                            'ride': 1
                        })
                else:
                    # Normal ride to end station
                    rebalanced_rides.append({
                        '15_min_interval': row['15_min_interval'],
                        'departure_station_id': start_station,
                        'chosen_arrival_station': end_station,
                        'ride': 1
                    })
        else:
            # Directly assign rides to end station without redistribution
            rebalanced_rides.append({
                '15_min_interval': row['15_min_interval'],
                'departure_station_id': start_station,
                'chosen_arrival_station': end_station,
                'ride': rides
            })

        
  
        # if bike_tracker[start_station] >= rides:
        #     bike_tracker[start_station] -= rides
        # else:
  
        #     bike_tracker[start_station] = 0

  
        # if bike_tracker[end_station] + rides <= capacity:
        #     bike_tracker[end_station] += rides
        # else:
  
        #     bike_tracker[end_station] = capacity

  
        # median_bikes = np.median(list(bike_tracker.values()))
        # demand = {station: median_bikes - bikes for station, bikes in bike_tracker.items() if bikes < median_bikes}

  
        # if bike_tracker[start_station] >= 12:  
        #     for _ in range(rides):
        #         if random.random() < 0.2:  
                    
        #             if demand:
        #                 highest_demand_station = min(demand, key=demand.get)
        #                 bike_tracker[highest_demand_station] += 1
        #                 rebalanced_rides.append({
        #                     '15_min_interval': row['15_min_interval'],
        #                     'departure_station_id': start_station,
        #                     'chosen_arrival_station': highest_demand_station,
        #                     'ride': 1
        #                 })
        #             else:
                    
        #                 rebalanced_rides.append({
        #                     '15_min_interval': row['15_min_interval'],
        #                     'departure_station_id': start_station,
        #                     'chosen_arrival_station': end_station,
        #                     'ride': 1
        #                 })
        #         else:
                    
        #             rebalanced_rides.append({
        #                 '15_min_interval': row['15_min_interval'],
        #                 'departure_station_id': start_station,
        #                 'chosen_arrival_station': end_station,
        #                 'ride': 1
        #             })
        # else:
            
        #     rebalanced_rides.append({
        #         '15_min_interval': row['15_min_interval'],
        #         'departure_station_id': start_station,
        #         'chosen_arrival_station': end_station,
        #         'ride': rides
        #     })

    
    rebalanced_df = pd.DataFrame(rebalanced_rides)
    
    print(median_bikes)

    return rebalanced_df

def time_to_minutes(time_obj):
    return time_obj.hour * 60 + time_obj.minute

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

def clean_df(predicted_rides_df):

    # rename the columns
    predicted_rides_df.rename(columns={'started_at': 'start_time'}, inplace=True)

    # delete rows where the end_time before the start_time
    predicted_rides_df = predicted_rides_df[predicted_rides_df['end_time'] > predicted_rides_df['start_time']]

    # delete the columns
    predicted_rides_df = predicted_rides_df.drop(columns=['ride_duration', 'end_time'])

    # Reorder the columns
    predicted_rides_df = predicted_rides_df[['start_time', 'start_station_id', 'end_station_id']]

    # stay only with the hours, minutes and seconds of the start_time and end_time
    predicted_rides_df['start_time'] = predicted_rides_df['start_time'].dt.strftime('%H:%M:%S')

    # order rows by start_time ascending
    predicted_rides_df.sort_values(by='start_time', inplace=True)

    return predicted_rides_df



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
    print(f"\nDataframe saved to '{path}'.")

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

def plot_departures_sec(predicted_rides_df):
    # Plot the number of rides per scaled 15-second interval in simulation
    predicted_rides_df['scaled_15s_interval'] = predicted_rides_df['start_time'].dt.floor('15s')
    rides_per_interval = predicted_rides_df.groupby('scaled_15s_interval').size().reset_index(name='ride_count')

    plt.figure(figsize=(10, 6))
    plt.plot(rides_per_interval['scaled_15s_interval'], rides_per_interval['ride_count'], marker='o', linestyle='-', color='b')
    plt.xlabel('Simulation Time (15-Second Intervals)')
    plt.ylabel('Number of Rides')
    plt.title('Number of Rides per 15-Second Interval in Scaled Simulation')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()


main()
