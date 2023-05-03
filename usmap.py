import plotly.graph_objects as go
import numpy as np
import pandas as pd
from urllib.request import urlopen
import json
from plotly.subplots import make_subplots

df = pd.read_csv('https://gist.githubusercontent.com/florianeichin/cfa1705e12ebd75ff4c321427126ccee/raw/c86301a0e5d0c1757d325424b8deec04cc5c5ca9/flights_all_cleaned.csv', sep=',')
df_airports= pd.read_csv('https://raw.githubusercontent.com/Leyla54/AbgabeDataVisualization/master/airports.csv', sep= ',')
df_airline_names = pd.read_csv('https://raw.githubusercontent.com/Leyla54/AbgabeDataVisualization/master/airlines.csv', sep= ',')

url_united_states= 'https://raw.githubusercontent.com/mapbox/mapboxgl-jupyter/master/examples/data/us-states.geojson'
token= 'pk.eyJ1IjoibGV5bGExMyIsImEiOiJjbGZtbHV3bGMwY21yNDNtbXJhdmFwaTE2In0.HEUGOzuyzJbiE0oz4RrwEQ'
df_airports= df_airports[['IATA_CODE','AIRPORT','CITY','STATE']]
df_map= df[['AIRLINE', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'DEPARTURE_DELAY', 'DESTINATION_DELAY', 'ORIGIN_AIRPORT_LAT', 'ORIGIN_AIRPORT_LON', 'DESTINATION_AIRPORT_LAT', 'DESTINATION_AIRPORT_LON']]
df_airports.rename(columns={'AIRPORT' : 'ORIGIN_AIRPORT_FULL_NAME', 'CITY': 'ORIGIN_CITY', 'STATE': 'ORIGIN_STATE'}, inplace=True)
df_map = pd.merge(df_map, df_airports, left_on='ORIGIN_AIRPORT', right_on='IATA_CODE')

df_airports.rename(columns={'ORIGIN_AIRPORT_FULL_NAME' : 'DESTINATION_AIRPORT_FULL_NAME', 'ORIGIN_CITY': 'DESTINATION_CITY', 'ORIGIN_STATE': 'DESTINATION_STATE', 'IATA_CODE': 'DESTINATION_IATA_CODE'}, inplace=True)
print(df_airports)
df_map = pd.merge(df_map, df_airports, left_on='DESTINATION_AIRPORT', right_on='DESTINATION_IATA_CODE')

df_map.to_csv('bin/Abgabe/test.csv')

df_map_states_departure = df_map.groupby('ORIGIN_STATE')

df_map_states_arrival= df_map.groupby('DESTINATION_STATE')
#print(df_map_states_departure.count())

with urlopen(url_united_states) as response:
    geo_data = json.load(response)

for feature in geo_data['features']:
    feature['id'] = feature['properties']['name']


fig = go.Figure()

usmap= go.Choroplethmapbox(geojson=geo_data)
fig.add_trace(usmap)
fig.update_layout(mapbox_style='light', mapbox_accesstoken=token, mapbox_zoom=5, mapbox_center= {'lat': 37.522147,'lon': -95.076446})
fig.show()
                           

