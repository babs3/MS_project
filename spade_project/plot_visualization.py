from dash import Dash, dcc, html, Input, Output
import plotly.graph_objects as go
import pandas as pd
from common import bike_positions, stations_data

# Initialize the Dash app
app = Dash(__name__)

# Create the initial figure
def create_map_figure():
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
    fig = create_map_figure()

    # Add bike positions dynamically
    if bike_positions:
        bike_lats = [lat for _, lat in bike_positions.values()]
        bike_lngs = [lng for _, lng in bike_positions.values()]
        fig.add_trace(go.Scattermapbox(
            lat=bike_lats,
            lon=bike_lngs,
            mode='markers',
            marker=dict(
                size=10,
                color='red',
                opacity=0.7
            ),
            name='Bikes'
        ))

    return fig

# Run the Dash app
if __name__ == '__main__':
    app.run_server(debug=True)

def update_plot():
    global bike_icons

    # Remove previous bike icons
