import plotly.graph_objects as go
import numpy as np
import pandas as pd
from urllib.request import urlopen
import json
from plotly.subplots import make_subplots

df = pd.read_csv('https://gist.githubusercontent.com/florianeichin/cfa1705e12ebd75ff4c321427126ccee/raw/c86301a0e5d0c1757d325424b8deec04cc5c5ca9/flights_all_cleaned.csv', sep=',')
df_airports= pd.read_csv('https://raw.githubusercontent.com/Leyla54/AbgabeDataVisualization/master/airports.csv', sep= ',')
df_airline_names = pd.read_csv('https://raw.githubusercontent.com/Leyla54/AbgabeDataVisualization/master/airlines.csv', sep= ',')
df_state_names= pd.read_csv('https://raw.githubusercontent.com/Leyla54/AbgabeDataVisualization/master/States%20-%20Sheet1.csv', sep= ',')

url_united_states= 'https://raw.githubusercontent.com/mapbox/mapboxgl-jupyter/master/examples/data/us-states.geojson'
token= 'pk.eyJ1IjoibGV5bGExMyIsImEiOiJjbGZtbHV3bGMwY21yNDNtbXJhdmFwaTE2In0.HEUGOzuyzJbiE0oz4RrwEQ'

df_airports_1= df_airports[['IATA_CODE','AIRPORT','CITY','STATE']]
df_map= df[['AIRLINE','FLIGHT_NUMBER', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'DEPARTURE_DELAY', 'DESTINATION_DELAY', 'ORIGIN_AIRPORT_LAT', 'ORIGIN_AIRPORT_LON', 'DESTINATION_AIRPORT_LAT', 'DESTINATION_AIRPORT_LON']]
df_state_names= df_state_names[['State', 'Postal']]
df_state_names.rename(columns={'State': 'ORIGIN_STATE_FULL_NAME'}, inplace=True)
df_airports_1.rename(columns={'AIRPORT' : 'ORIGIN_AIRPORT_FULL_NAME', 'CITY': 'ORIGIN_CITY', 'STATE': 'ORIGIN_STATE'}, inplace=True)
df_positions= df_airports[['IATA_CODE', 'LATITUDE', 'LONGITUDE']]

df_map = pd.merge(df_map, df_airports_1, left_on='ORIGIN_AIRPORT', right_on='IATA_CODE')
df_map = pd.merge(df_map, df_state_names, left_on='ORIGIN_STATE', right_on='Postal')

df_airports_1.rename(columns={'ORIGIN_AIRPORT_FULL_NAME' : 'DESTINATION_AIRPORT_FULL_NAME', 'ORIGIN_CITY': 'DESTINATION_CITY', 'ORIGIN_STATE': 'DESTINATION_STATE', 'IATA_CODE': 'DESTINATION_IATA_CODE'}, inplace=True)

df_state_names.rename(columns= {'ORIGIN_STATE_FULL_NAME': 'DESTINATION_STATE_FULL_NAME', 'Postal': 'POSTAL_DESTINATION'}, inplace=True)
df_map = pd.merge(df_map, df_airports_1, left_on='DESTINATION_AIRPORT', right_on='DESTINATION_IATA_CODE')
df_map = pd.merge(df_map, df_state_names, left_on='DESTINATION_STATE', right_on='POSTAL_DESTINATION')
df_map.drop('IATA_CODE', axis='columns', inplace=True)
df_map.drop('Postal', axis='columns', inplace=True)
df_map.drop('DESTINATION_IATA_CODE', axis='columns', inplace=True)
df_map.drop( 'POSTAL_DESTINATION', axis='columns', inplace=True)




df_map.to_csv('bin/Abgabe/test.csv')

df_map_states_departure = df_map.groupby('ORIGIN_STATE_FULL_NAME').mean()
df_map_states_arrival= df_map.groupby('DESTINATION_STATE_FULL_NAME').mean()

df_count_departure= df_map.groupby('ORIGIN_AIRPORT').count()
df_size_departure= df_map.groupby('ORIGIN_AIRPORT')['FLIGHT_NUMBER'].count().reset_index(name= 'flights')

df_size_departure= pd.merge(df_size_departure, df_positions, left_on='ORIGIN_AIRPORT', right_on='IATA_CODE')
df_size_departure.drop('IATA_CODE', axis='columns', inplace=True)


df_count_arrival= df_map.groupby('DESTINATION_AIRPORT').count()
df_count_arrival= df_map.groupby('DESTINATION_AIRPORT')['FLIGHT_NUMBER'].count().reset_index(name= 'flights')
df_count_arrival= pd.merge(df_count_arrival, df_positions, left_on='DESTINATION_AIRPORT', right_on='IATA_CODE')
df_count_arrival.drop('IATA_CODE', axis= 'columns', inplace=True)
print(df_count_arrival)

df_count_departure.to_csv('bin/Abgabe/dep.csv')
#print(df_count_departure[df_count_departure['ORIGIN_AIRPORT']=='JAC'])
with urlopen(url_united_states) as response:
    geo_data = json.load(response)

for feature in geo_data['features']:
    feature['id'] = feature['properties']['name']


fig = go.Figure()


usmap_departure= go.Choroplethmapbox(geojson=geo_data,
                                     locations= df_map_states_departure.index,
                                     z= df_map_states_departure.DEPARTURE_DELAY,
                                     marker_opacity =0.85,
                                     marker_line_width = 0.9,
                                     zmin= -10,
                                     zmid= 0,
                                     zmax= 60,
                                     colorscale = [[0, '#228B22'], [0.15, '#FFFFFF'], [0.75, '#FF0000'], [1, '#750000']],
                                     colorbar= dict(title= 'delay in min', titleside= 'top'), text= None
                                    )

usmap_arrival= go.Choroplethmapbox(geojson=geo_data,
                                     locations= df_map_states_arrival.index,
                                     z= df_map_states_arrival.DESTINATION_DELAY,
                                     marker_opacity =0.85,
                                     marker_line_width = 0.7,
                                     zmin= -20,
                                     zmid= 0,
                                     zmax= 65,
                                     #visible=False,
                                     colorscale = [[0, '#228B22'], [0.23, '#FFFFFF'], [0.75, '#FF0000'], [1, '#750000']],
                                     colorbar= dict(title= 'delay in min', titleside= 'top',
                                     ), text= None)

scattermap_departures= go.Scattermapbox(lat= df_size_departure['LATITUDE'],
                                        lon= df_size_departure['LONGITUDE'],
                                        mode= 'markers',
                                        marker= go.scattermapbox.Marker(size = df_size_departure['flights'],
                                                                        sizemode= 'area',
                                                                        
                                                                         color= '#228B22',
                                                                         opacity=1), text= df_size_departure['ORIGIN_AIRPORT'], showlegend=False
                                                                         
                                                                          
                                                               
                                                                         
                                                                         
                                                                         
                                                               )

scattermap_arrivals= go.Scattermapbox(lat= df_count_arrival['LATITUDE'],
                                      lon= df_count_arrival['LONGITUDE'],
                                      mode= 'markers',
                                      #visible= False,
                                      marker= go.scattermapbox.Marker(size = df_count_arrival['flights'],
                                                                      sizemode= 'area',
                                                                      color= '#000000',
                                                                      opacity= 1
                                                                         
                                                                         
                                                               ), showlegend= False
                                                               )


fig.add_trace(usmap_departure)
fig.add_trace(usmap_arrival)
fig.add_trace(scattermap_departures)
fig.add_trace(scattermap_arrivals)

fig.update_layout(mapbox_style='light', mapbox_accesstoken=token, mapbox_zoom=3, mapbox_center= {'lat': 37.522147,'lon': -95.076446}, 
                  title= 'Average delays per state', title_font_size= 25, title_font_family= 'Arial Black', title_x = 0.5,
                  updatemenus= [
                      dict(active= 0, buttons = list([
                          dict(label= 'Departure delay', method= 'update', args= [{'visible': [True, False,False, False]}, {'title': 'Average departure delay per state'}]),
                          dict(label= 'Arrival delay', method= 'update', args= [{'visible': [False, True, False, False]}, {'title': 'Average arrival delay per state'}])
                          ]), direction= 'down',pad={"r": 10, "t": 10}, showactive= True,x=0, xanchor= 'left', yanchor= 'bottom'
                          ),
                       dict(active= 0, buttons = list([
                          dict(label= 'Departures at airports', method= 'update', args= [{'visible': [False, False, True, False]},{'title': 'Number of departures at airports'}]),
                          dict(label= 'Arrival at airports', method= 'update', args= [{'visible': [False, False, False, True]}, {'title': 'Number of arrivals at airports'}])
                          ]), direction= 'down',pad={"r": 10, "t": 10}, showactive= True,x=0.13, xanchor= 'left', yanchor= 'bottom'
                          ) ])
fig.update_traces(visible = False, selector=dict(visible= True))
fig.show()
                           
#dict(label= 'All flights at airports', method= 'update', args= [{'title': 'Number of arrivals and departures at airports'}]),