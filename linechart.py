import plotly.graph_objects as go
import numpy as np
import pandas as pd
from urllib.request import urlopen
import json
from plotly.subplots import make_subplots

df = pd.read_csv('https://gist.githubusercontent.com/florianeichin/cfa1705e12ebd75ff4c321427126ccee/raw/c86301a0e5d0c1757d325424b8deec04cc5c5ca9/flights_all_cleaned.csv', sep=',')

#------------------------------------------------------------
#-------linechart for arrivals & departures per hour---------
#------------------------------------------------------------


#-------data preparation-------------------------------------
df_linechart= df[[ 'FLIGHT_NUMBER','SCHEDULED_DEPARTURE', 'SCHEDULED_DESTINATION']]


#getting a substring to add as a new column
substring_departure = []
for i in range(len(df_linechart)):
    substring_departure.append(df_linechart['SCHEDULED_DEPARTURE'][i][9:13:1])
    
#adding it & formating it
df_linechart['DEPARTURE_HOUR'] = substring_departure
df_linechart['DEPARTURE_HOUR'] = df_linechart['DEPARTURE_HOUR'].apply(lambda x :'{}{}'.format(x, ':00'))
df_linechart['DEPARTURE_HOUR'] = df_linechart['DEPARTURE_HOUR'].str.replace('1 ', '')
df_linechart_departure =  df_linechart.groupby('DEPARTURE_HOUR')['FLIGHT_NUMBER'].count().reset_index(name= 'COUNT')
df_linechart_departure['DEPARTURE_TEXT']= 'Departures' #for hovertemplate

#getting a substring to add as a new column
#1 and 2 included to show which day they arrived
substring_arrival= []
for i in range(len(df_linechart)):
    substring_arrival.append(df_linechart['SCHEDULED_DESTINATION'][i][9:13:1])

df_linechart['ARRIVAL_HOUR'] = substring_arrival
df_linechart['ARRIVAL_HOUR'] = df_linechart['ARRIVAL_HOUR'].apply(lambda x :'{}{}'.format(x, ':00'))
df_linechart_arrival = df_linechart.groupby('ARRIVAL_HOUR')['FLIGHT_NUMBER'].count().reset_index(name= 'COUNT')
df_linechart_arrival['ARRIVAL_HOUR'] = df_linechart_arrival['ARRIVAL_HOUR'].str.replace('1 ', '')
df_linechart_arrival['ARRIVAL_HOUR'] = df_linechart_arrival['ARRIVAL_HOUR'].str.replace('2 ', '2 Jan ')
df_linechart_arrival['ARRIVAL_TEXT']= 'Arrivals' #for hovertemplate

#-------hovertemplate---------------------------------------

hovertemplate= '<b>%{text}</b>' + '<br>Number of flights: %{y}<br>' + 'Time of day: %{x}<extra></extra>'



#-------visualization---------------------------------------

fig= go.Figure()

#trace1
linechart_departure = go.Scatter(x= df_linechart_departure['DEPARTURE_HOUR'], y= df_linechart_departure['COUNT'],
                              mode= 'lines+markers', line= dict(color= '#6f78a5', dash= 'dot', width=3), name= 'Departures', marker_size= 7,
                                text= df_linechart_departure['DEPARTURE_TEXT'], hovertemplate=hovertemplate)

#trace2
linechart_arrival = go.Scatter(x= df_linechart_arrival['ARRIVAL_HOUR'], y= df_linechart_arrival['COUNT'],
                               mode= 'lines+markers', line= dict(color= '#7eb774', dash= 'dot', width= 3), name= 'Arrivals', marker_size= 7,
                               text= df_linechart_arrival['ARRIVAL_TEXT'], hovertemplate= hovertemplate)

fig.add_trace(linechart_departure)
fig.add_trace(linechart_arrival)

#layout
fig.update_layout(title= 'Number of arrival & departure flights per hour', title_font_size= 25, title_font_family= 'Arial Black', xaxis_title= 'Hour of day',
                  xaxis_title_font_family= 'Arial Black' ,yaxis_title= 'Number of flights', yaxis_title_font_family= 'Arial Black', title_x= 0.5)

fig.show()
