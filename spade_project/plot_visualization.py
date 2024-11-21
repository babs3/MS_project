from common import bike_positions, stations_data

import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Load the bike and station icons 
bike_icon = mpimg.imread('./images/bike_icon.png')  # Path to your bike icon image
station_icon = mpimg.imread('./images/station_icon.png')  # Path to your station icon image

import plotly.graph_objects as go
import pandas as pd
import plotly.express as px

# Assuming 'stations_data' is already loaded
# bike_positions should be a dictionary like: {bike_id: (lng, lat)}

# Create Plotly figure for map
fig = go.Figure()

# Add station icons (scatter points for stations)
fig.add_trace(go.Scattermapbox(
    lat=stations_data['lat'], 
    lon=stations_data['lng'],
    mode='markers',
    marker=dict(
        size=12,
        symbol='circle',  # You can change symbol to a custom image later
        color='blue',
        opacity=0.7
    ),
    text=stations_data['station_name'],  # Show station names when hovered
    hoverinfo='text',
    name='Stations'
))

# Add bike icons (scatter points for bikes)
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

# Set up the map layout for better interactivity (zoom, pan)
fig.update_layout(
    mapbox=dict(
        style="carto-positron",  # You can use other styles like "open-street-map" or "satellite"
        center=dict(lat=stations_data['lat'].mean(), lon=stations_data['lng'].mean()),  # Center the map based on the station data
        zoom=13,  # Initial zoom level
    ),
    title="Bike Stations and Bikes",
    showlegend=True
)

# Update the layout for hover interaction and zoom/pan support
fig.update_layout(
    hovermode='closest',  # Enable hover for closest points
    dragmode='zoom',  # Allow panning and zooming
)

# Show the plot
fig.show()

# Track bike icon objects
bike_icons = []

# Function to update the plot with new bike positions
def update_plot():
    global bike_icons

    # Remove previous bike icons
    for icon in bike_icons:
        icon.remove()
    bike_icons.clear()

    # Add updated bike icons
    if bike_positions:
        for lng, lat in bike_positions.values():
            bike_icon_extent = (lng - 0.0005, lng + 0.0005, lat - 0.0005, lat + 0.0005)
            #icon = ax.imshow(bike_icon, extent=bike_icon_extent, zorder=2)
            #bike_icons.append(icon)

    plt.draw()  # Redraw the plot