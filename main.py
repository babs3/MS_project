import time
import threading
from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
from utils import rides_data, stations  # Assuming stations is a shared list of Station objects
from utils import calculate_availability_rate, get_insights

# Dash App Initialization
app = Dash(__name__)

# Function to create the map figure
def create_map_figure(center=None, zoom=None):
    fig = go.Figure()

    # Extract data from Station class
    lats = [station.lat for station in stations]
    lngs = [station.lng for station in stations]
    bike_counts = [station.bike_count for station in stations]
    station_names = [station.station_name for station in stations]
    availability_rates = [station.get_availability_rate() for station in stations]

    # Define colors based on bike count
    color_map = [
        'red' if count == 0 else ('orange' if count <= 20 else ('green' if count <= 35 else 'blue'))
        for count in bike_counts
    ]

    max_bikes = max(bike_counts) if bike_counts else 1  # Avoid division by zero
    size_map = [
        7 + (count / max_bikes) * 18  # Scale size proportionally between 7 and 25
        for count in bike_counts
    ]

    # Create hover text with availability rate
    hover_text = [
        f"{name}<br>Bikes: {count}/{station.capacity}<br>Availability: {rate:.2%}"
        for name, count, station, rate in zip(station_names, bike_counts, stations, availability_rates)
    ]

    # Add a Scattermapbox trace for the stations
    fig.add_trace(go.Scattermapbox(
        lat=lats,
        lon=lngs,
        mode='markers',
        marker=dict(
            size=size_map,  # Dynamic marker size
            symbol='circle',
            color=color_map,  # Use the dynamic color map
            opacity=0.7
        ),
        text=hover_text,  # Dynamic hover text
        hoverinfo='text',
        showlegend=False
    ))

    # Add dummy traces for the legend
    fig.add_trace(go.Scattermapbox(
        lat=[None], lon=[None],
        mode='markers',
        marker=dict(size=12, color='blue', opacity=0.7),
        name='Overstocked Station'
    ))
    fig.add_trace(go.Scattermapbox(
        lat=[None], lon=[None],
        mode='markers',
        marker=dict(size=12, color='green', opacity=0.7),
        name='Healthy Station'
    ))
    fig.add_trace(go.Scattermapbox(
        lat=[None], lon=[None],
        mode='markers',
        marker=dict(size=12, color='yellow', opacity=0.7),
        name='Low Stock Station'
    ))
    fig.add_trace(go.Scattermapbox(
        lat=[None], lon=[None],
        mode='markers',
        marker=dict(size=12, color='red', opacity=0.7),
        name='Empty Station'
    ))

    # Update layout settings
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=center or dict(lat=sum(lats) / len(lats), lon=sum(lngs) / len(lngs)),
            zoom=zoom or 10,
        ),
        title="Bike Stations - Availability",
        showlegend=True,
        hovermode='closest',
        dragmode='zoom',
        margin=dict(l=10, r=10, t=40, b=20)
    )

    return fig


# Dash App Layout
app.layout = html.Div([
    dcc.Graph(id='map', config={'scrollZoom': True}, style={'width': '100%', 'height': '90vh'}),
    html.Div(id='availability-rate', style={'textAlign': 'center', 'fontSize': '20px', 'margin': '10px'}),
    dcc.Interval(id='interval-component', interval=2000, n_intervals=0),  # Auto-update every 2 seconds
    dcc.Store(id='map-state', data={'center': None, 'zoom': None})  # Store map state
], style={'margin': '0', 'padding': '0', 'height': '100vh'})  # Ensure no margins and full height


# Callback to update the map figure
@app.callback(
    Output('map', 'figure'),
    [Input('interval-component', 'n_intervals')],
    [State('map-state', 'data')]  # Map state (center, zoom)
)
def update_map_figure(n_intervals, map_state):
    center = map_state['center']
    zoom = map_state['zoom']

    # Generate and return the updated map figure
    return create_map_figure(center=center, zoom=zoom)

# Callback to store the map's current state (center and zoom)
@app.callback(
    Output('map-state', 'data'),
    Input('map', 'relayoutData'),  # Capture map's relayout events
    State('map-state', 'data')
)
def update_map_state(relayout_data, map_state):
    if relayout_data and 'mapbox.center' in relayout_data and 'mapbox.zoom' in relayout_data:
        map_state['center'] = relayout_data['mapbox.center']
        map_state['zoom'] = relayout_data['mapbox.zoom']
    return map_state

# Callback to update the System-wide Availability Rate
@app.callback(
    Output('availability-rate', 'children'),
    [Input('interval-component', 'n_intervals')]
)
def update_availability_rate(n_intervals):
    rate = calculate_availability_rate()
    return f"System-wide Availability Rate: {rate:.2%}"


def simulation_loop():
    simulation_duration = 60  # seconds 
    simulation_delay = simulation_duration / len(rides_data)
    
    try:
        print("\nRunning simulation...")
        time.sleep(5)

        # start counting time
        start_time = time.time()

        # Simulate rides
        for t, ride in rides_data.iterrows():
            for station in stations:
                if station.station_id == ride['start_station_id']:
                    if station.bike_count > 0:
                        perform_ride = True
                        station.remove_bike()
                        break

            if perform_ride:
                for station in stations:
                    if station.station_id == ride['end_station_id']:
                        #if station.bike_count < station.capacity:  # Check if the station is not full
                        station.add_bike()
                        break

            # Calculate and log the system-wide availability rate
            availability_rate = calculate_availability_rate()

            # Calculate the elapsed time
            elapsed_time = time.time() - start_time
            expected_time = (t + 1) * simulation_delay
            sleep_time = expected_time - elapsed_time

            if sleep_time > 0:
                time.sleep(sleep_time)

        # Calculate total elapsed time
        total_elapsed_time = time.time() - start_time
        print(f"Simulation completed in {total_elapsed_time:.2f} seconds")
        print(f"System-wide Availability Rate: {availability_rate:.2%}")

        get_insights() # Get insights of stations after simulation
        


    except KeyboardInterrupt:
        print("Simulation stopped by user.")
    

# Run Dash App and Simulation in Parallel
if __name__ == '__main__':
    # Run the simulation in a separate thread
    simulation_thread = threading.Thread(target=simulation_loop)
    simulation_thread.daemon = True  # Ensures thread exits when the program exits
    simulation_thread.start()

    # Run Dash app
    app.run_server(debug=True)
