from dash import Dash, dcc, html, Input, Output, State
import plotly.graph_objects as go
import pandas as pd
from utils import bike_positions, stations_data

# Initialize the Dash app
app = Dash(__name__)

# Create the initial figure
def create_map_figure(center=None, zoom=None):
    fig = go.Figure()

    # Add station icons
    fig.add_trace(go.Scattermapbox(
        lat=stations_data['lat'],
        lon=stations_data['lng'],
        mode='markers',
        marker=dict(
            size=12,
            symbol='circle',
            color='blue',
            opacity=0.7
        ),
        text=stations_data['station_name'],
        hoverinfo='text',
        name='Stations'
    ))

    # Add layout settings with dynamic center and zoom
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=center or dict(lat=stations_data['lat'].mean(), lon=stations_data['lng'].mean()),
            zoom=zoom or 13,
        ),
        title="Bike Stations and Bikes",
        showlegend=True,
        hovermode='closest',  # Enable hover for closest points
        dragmode='zoom',  # Allow panning and zooming
    )

    return fig

# Standalone function to update bike positions
def get_updated_bike_positions_figure(center=None, zoom=None):
    # Read the CSV file into a DataFrame
    bike_positions = pd.read_csv('./auxiliar_files/bike_positions.csv')
    bike_positions = bike_positions.rename(columns={
        'bike_id': 'bike_id',
        'lat': 'lat',
        'lng': 'lng'
    })
    bike_positions = bike_positions[['bike_id', 'lat', 'lng']]

    # Create the map figure with updated bike positions
    fig = create_map_figure(center=center, zoom=zoom)

    fig.add_trace(go.Scattermapbox(
        lat=bike_positions['lat'],
        lon=bike_positions['lng'],
        mode='markers',
        marker=dict(
            size=10,
            symbol='circle',
            color='red',
            opacity=0.5
        ),
        text=bike_positions['bike_id'],
        hoverinfo='text',
        name='Bikes'
    ))

    return fig

# Dash app layout
app.layout = html.Div([
    dcc.Graph(id='map', config={'scrollZoom': True}, style={'width': '100%', 'height': '90vh'}),
    dcc.Interval(id='interval-component', interval=2000, n_intervals=0),  # Auto-update every 2 seconds
    dcc.Store(id='map-state', data={'center': None, 'zoom': None})  # Store for map center and zoom
])

# Dash callback to update the map
@app.callback(
    Output('map', 'figure'),
    [
        Input('interval-component', 'n_intervals'),
        State('map-state', 'data')  # Get the current map state
    ]
)
def update_bike_positions(n_intervals, map_state):
    center = map_state['center']
    zoom = map_state['zoom']
    return get_updated_bike_positions_figure(center=center, zoom=zoom)

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

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)
