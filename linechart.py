import plotly.graph_objects as go
import numpy as np
import pandas as pd
from urllib.request import urlopen
import json
from plotly.subplots import make_subplots

df = pd.read_csv('https://gist.githubusercontent.com/florianeichin/cfa1705e12ebd75ff4c321427126ccee/raw/c86301a0e5d0c1757d325424b8deec04cc5c5ca9/flights_all_cleaned.csv', sep=',')
df_airports= pd.read_csv('https://raw.githubusercontent.com/Leyla54/AbgabeDataVisualization/master/airports.csv', sep= ',')
df_airline_names = pd.read_csv('https://raw.githubusercontent.com/Leyla54/AbgabeDataVisualization/master/airlines.csv', sep= ',')

#-------linechart for arrivals & departures per hour---------
#it's a forecast

df_linechart= df[[ 'FLIGHT_NUMBER','SCHEDULED_DEPARTURE', 'SCHEDULED_DESTINATION']]

substring_departure = []
for i in range(len(df_linechart)):
    substring_departure.append(df_linechart['SCHEDULED_DEPARTURE'][i][9:13:1])
    

df_linechart['DEPARTURE_HOUR'] = substring_departure
df_linechart['DEPARTURE_HOUR'] = df_linechart['DEPARTURE_HOUR'].apply(lambda x :'{}{}'.format(x, ':00'))
df_linechart['DEPARTURE_HOUR'] = df_linechart['DEPARTURE_HOUR'].str.replace('1 ', '')

df_linechart_departure =  df_linechart.groupby('DEPARTURE_HOUR')['FLIGHT_NUMBER'].count().reset_index(name= 'COUNT')

#print(df_linechart_departure)

substring_arrival= []
for i in range(len(df_linechart)):
    substring_arrival.append(df_linechart['SCHEDULED_DESTINATION'][i][9:13:1])

df_linechart['ARRIVAL_HOUR'] = substring_arrival
df_linechart['ARRIVAL_HOUR'] = df_linechart['ARRIVAL_HOUR'].apply(lambda x :'{}{}'.format(x, ':00'))
df_linechart_arrival = df_linechart.groupby('ARRIVAL_HOUR')['FLIGHT_NUMBER'].count().reset_index(name= 'COUNT')
df_linechart_arrival['ARRIVAL_HOUR'] = df_linechart_arrival['ARRIVAL_HOUR'].str.replace('1 ', '')
df_linechart_arrival['ARRIVAL_HOUR'] = df_linechart_arrival['ARRIVAL_HOUR'].str.replace('2 ', '2 Jan ')

print(df_linechart_arrival)

fig= go.Figure()

linechart_departure = go.Scatter(x= df_linechart_departure['DEPARTURE_HOUR'], y= df_linechart_departure['COUNT'],
                              mode= 'lines+markers', line= dict(color= '#6f78a5', dash= 'dot', width=3), name= 'Departures', marker_size= 7)

linechart_arrival = go.Scatter(x= df_linechart_arrival['ARRIVAL_HOUR'], y= df_linechart_arrival['COUNT'],
                               mode= 'lines+markers', line= dict(color= '#12ce02', dash= 'dot', width= 3), name= 'Arrivals', marker_size= 7)

fig.add_trace(linechart_departure)
fig.add_trace(linechart_arrival)
fig.update_layout(title= 'Number of arrival & departure flights per hour', title_font_size= 25, title_font_family= 'Arial Black', xaxis_title= 'Hour of day',
                  xaxis_title_font_family= 'Arial Black' ,yaxis_title= 'Number of flights', yaxis_title_font_family= 'Arial Black', title_x= 0.5)

fig.show()