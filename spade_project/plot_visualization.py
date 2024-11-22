from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd

# Initialize the Dash app
app = Dash(__name__)

# Load station data
stations_data = pd.DataFrame({
    'station_id': [],
    'station_name': [],
    'lat': [],
    'lng': []
})

# Read the CSV file into a DataFrame
all_stations = pd.read_csv('./datasets/some_stations.csv')

stations_data = all_stations.rename(columns={ # without this it will not work dont know why
    'station_id': 'station_id',
    'station_name': 'station_name',
    'lat': 'lat',
    'lng': 'lng'
})

# Ensure the DataFrame has the correct columns and order
stations_data = stations_data[['station_id', 'station_name', 'lat', 'lng']]



# Load bikes data

bike_positions = pd.DataFrame({
    'bike_id': [],
    'lat': [],
    'lng': []
})


# Create the initial figure
def create_map_figure():
    fig = go.Figure()

    print(stations_data.columns) 
    print(stations_data.head())   # Inspect the first few rows for unexpected columns

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

    # Add layout settings
    fig.update_layout(
        mapbox=dict(
            style="carto-positron",
            center=dict(lat=stations_data['lat'].mean(), lon=stations_data['lng'].mean()),
            zoom=13,
        ),
        title="Bike Stations and Bikes",
        showlegend=True,
        hovermode='closest',  # Enable hover for closest points
        dragmode='zoom',  # Allow panning and zooming
    )

    return fig

# Dash app layout
app.layout = html.Div([
    dcc.Graph(id='map', config={'scrollZoom': True}, style={'width': '100%', 'height': '90vh'}),
    dcc.Interval(id='interval-component', interval=2000, n_intervals=0)  # Auto-update every 2 seconds
])


# Callback to update bike positions on the map
@app.callback(
    Output('map', 'figure'),
    Input('interval-component', 'n_intervals')
)
def update_bike_positions(n_intervals):
    # Read the CSV file into a DataFrame
    bike_positions = pd.read_csv('./datasets/bike_positions.csv')

    bike_positions = bike_positions.rename(columns={ # without this it will not work dont know why
        'bike_id': 'bike_id',
        'lat': 'lat',
        'lng': 'lng'
    })

    # Ensure the DataFrame has the correct columns and order
    bike_positions = bike_positions[['bike_id', 'lat', 'lng']]

    fig = create_map_figure()

    print("\n---------- DEBUG ----------")
    print(bike_positions.columns)  # Ensure columns are ['bike_id', 'lat', 'lng']
    print(bike_positions.head())   # Inspect the first few rows for unexpected columns


    # Add bike positions dynamically
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

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

def update_plot():
    global bike_icons

    # Remove previous bike icons
