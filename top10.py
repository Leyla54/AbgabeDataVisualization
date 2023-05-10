import plotly.graph_objects as go
import numpy as np
import pandas as pd
from urllib.request import urlopen
import json
from plotly.subplots import make_subplots

df = pd.read_csv('https://gist.githubusercontent.com/florianeichin/cfa1705e12ebd75ff4c321427126ccee/raw/c86301a0e5d0c1757d325424b8deec04cc5c5ca9/flights_all_cleaned.csv', sep=',')
df_airports= pd.read_csv('https://raw.githubusercontent.com/Leyla54/AbgabeDataVisualization/master/airports.csv', sep= ',')
df_airline_names = pd.read_csv('https://raw.githubusercontent.com/Leyla54/AbgabeDataVisualization/master/airlines.csv', sep= ',')

print(df_airline_names)
print(df)

df = df[['AIRLINE', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'DEPARTURE_DELAY', 'DESTINATION_DELAY', 'DISTANCE']]

#top 10 airlines by flight count
df_top_airlines= df.groupby('AIRLINE').count().sort_values(by= 'ORIGIN_AIRPORT', ascending= False)
df_top_airlines=df_top_airlines.nlargest(10, 'ORIGIN_AIRPORT')
#print(df_top_airlines)

#top 10 departure airports by flight count 
df_top_airports_departure= df.groupby('ORIGIN_AIRPORT').count().sort_values(by= 'AIRLINE', ascending=False)
df_top_airports_departure= df_top_airports_departure.nlargest(10,'AIRLINE')
#print(df_top_airports_departure)

#top 10 arrival airports by flight count
df_top_airports_arrival= df.groupby('DESTINATION_AIRPORT').count().sort_values(by= 'AIRLINE', ascending=False)
df_top_airports_arrival= df_top_airports_arrival.nlargest(10,'AIRLINE')
#print(df_top_airports_arrival)

#top 10 connections by distance (dumbells or map)
# def sorting(x): x.sort_values(by= 'DISTANCE', ascending=False)

# df_top_distance= df.groupby('DISTANCE').apply(sorting(df))
# print(df_top_distance)


#top 10 airports by highest arrival/departuer delay
df_top_airports_delay_departure= df.groupby('ORIGIN_AIRPORT').max().sort_values(by= 'DEPARTURE_DELAY', ascending=False)
print(df_top_airports_delay_departure)
df_top_airports_delay_departure= df_top_airports_delay_departure.nlargest(10, 'DEPARTURE_DELAY')
#print(df_top_airports_delay_departure)


df_top_airports_delay_arrival= df.groupby('DESTINATION_AIRPORT').max().sort_values(by= 'DESTINATION_DELAY', ascending=False)
df_top_airports_delay_arrival= df_top_airports_delay_arrival.nlargest(10, 'DESTINATION_DELAY')
#print(df_top_airports_delay_arrival)


#top 10 airlines average delay at origin & destination
df_top_airline_delays= df.groupby(['AIRLINE', 'DEPARTURE_DELAY'])['DEPARTURE_DELAY'].mean()
#print(df_top_airline_delays.unstack())
colours_airport= ['#6f78a5', ]*10
colours_airport[5]= '#7eb774'
colours_airport[7]= '#ed7b84'

colours_airport_arr= ['#6f78a5', ]*10
colours_airport_arr[5]= '#ed7b84'
colours_airport_arr[7]= '#7eb774'

fig= go.Figure()

airlines_barchart= go.Bar(x= df_top_airlines.index, y= df_top_airlines['ORIGIN_AIRPORT'])

fig.add_trace(airlines_barchart)
#fig.show()

fig1= make_subplots(rows= 2, cols=2, subplot_titles=('Number of departure flights', 'Arrival flight count', 'Highest departure airport delay', 'Highest arrival airport delay'),
                    )
departure_airport= go.Bar(y= df_top_airports_departure.index, x= df_top_airports_departure['AIRLINE'], marker_color= colours_airport, orientation= 'h' )
arrival_airports= go.Bar(y= df_top_airports_arrival.index, x= df_top_airports_arrival['AIRLINE'], marker_color= colours_airport_arr, orientation= 'h')
fig1.add_trace(departure_airport, row= 1, col=1)
fig1.add_trace(arrival_airports, row= 1, col=2)

delay_departure_airports= go.Bar(x= df_top_airports_delay_departure.index, y= df_top_airports_delay_departure['DEPARTURE_DELAY'])
delay_arrival_airports= go.Bar(x= df_top_airports_delay_arrival.index, y= df_top_airports_delay_arrival['DESTINATION_DELAY'])
fig1.add_trace(delay_departure_airports, row=2, col=1)
fig1.add_trace(delay_arrival_airports, row=2, col=2)

fig1.update_layout(showlegend= False, yaxis= dict(autorange= 'reversed'), yaxis2= dict(autorange= 'reversed'))
fig1.update_annotations(font = dict(family= 'Arial Black'))

fig1.show()

plot_bgcolor
piecolorway
paper_bgcolor