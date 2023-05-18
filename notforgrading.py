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

#-----------------------NOT FOR GRADING!!!!!!!!!!!!!!!!-------------------------------------------------------------
#-----------------------NOT FOR GRADING!!!!!!!!!!!!!!!!-------------------------------------------------------------
#-----------------------NOT FOR GRADING!!!!!!!!!!!!!!!!-------------------------------------------------------------
#-----------------------NOT FOR GRADING!!!!!!!!!!!!!!!!-------------------------------------------------------------
#-----------------------NOT FOR GRADING!!!!!!!!!!!!!!!!-------------------------------------------------------------
#-----------------------NOT FOR GRADING!!!!!!!!!!!!!!!!-------------------------------------------------------------
#-----------------------NOT FOR GRADING!!!!!!!!!!!!!!!!-------------------------------------------------------------
#-----------------------NOT FOR GRADING!!!!!!!!!!!!!!!!-------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------
# the idea was that one can choose to look at the subplots either as horizontal or vertical barcharts, my first 
# attempt didn't work. I tried a again and now half of it is working, with the update the left graph changes but it's
# not a subplot anymore. Rather it is a full plot and on top is still the left subplot horizontally and for the 
# vertical one only graph background, since the update with the button is not subplots anymore, it doesn't take the
# arguments for the 2nd x & y axis. I couldn't find a solution and handed in the other version "working top 10", but 
# I would appreciate if you could look at it and if I made an obvious mistake, could you pleas tell me.
# 
# Many thanks :)
# Leyla
#-------------------------------------------------------------------------------------------------------------------
#-------------------------------------------------------------------------------------------------------------------

#-----------------------data preparation-----------------------------------------------------------------------

#only necessary columns
df_airports= df_airports[['IATA_CODE', 'AIRPORT', 'CITY']]
df = df[['AIRLINE', 'ORIGIN_AIRPORT', 'DESTINATION_AIRPORT', 'DEPARTURE_DELAY', 'DESTINATION_DELAY', 'DISTANCE']]

#top 10 airlines by flight count
df_top_airlines= df.groupby('AIRLINE').count().sort_values(by= 'ORIGIN_AIRPORT', ascending= False)
df_top_airlines=df_top_airlines.nlargest(10, 'ORIGIN_AIRPORT')
#print(df_top_airlines)

#top 10 departure airports by flight count bar chart
df_top_airports_departure= df.groupby('ORIGIN_AIRPORT').count().sort_values(by= 'AIRLINE', ascending=False)
df_top_airports_departure= df_top_airports_departure.nlargest(10,'AIRLINE')
df_top_airports_departure= pd.merge(df_top_airports_departure, df_airports, left_on='ORIGIN_AIRPORT', right_on='IATA_CODE')


#top 10 arrival airports by flight count bar chart
df_top_airports_arrival= df.groupby('DESTINATION_AIRPORT').count().sort_values(by= 'AIRLINE', ascending=False)
df_top_airports_arrival= df_top_airports_arrival.nlargest(10,'AIRLINE')
df_top_airports_arrival= pd.merge(df_top_airports_arrival, df_airports, left_on='DESTINATION_AIRPORT', right_on='IATA_CODE')


#colours for departure
colours_airport= ['#6f78a5', ]*10
colours_airport[5]= '#7eb774'
colours_airport[7]= '#ed7b84'

#colours for arrival
colours_airport_arr= ['#6f78a5', ]*10
colours_airport_arr[5]= '#ed7b84'
colours_airport_arr[7]= '#7eb774'

#----------------------hovertemplate--------------------------------------------------------------------
hovertemplate= '<b>%{customdata}</b>' + '<br>in %{hovertext}' + '<br>Number of flights: %{x}<extra></extra>'

hovertemplate_vertical= '<b>%{customdata}</b>' + '<br>in %{hovertext}' + '<br>Number of flights: %{y}<extra></extra>'


#---------------------making the figure-----------------------------------------------------------------


#subplots
fig1= make_subplots(rows= 1, cols=2, specs=[[{'type': 'bar'},{'type': 'bar'}]],subplot_titles=('Departure flight count', 'Arrival flight count'),
                    )

#subplot departure
departure_airport= go.Bar(x= df_top_airports_departure['AIRLINE'],y= df_top_airports_departure['IATA_CODE'],  marker_color= colours_airport, orientation= 'h' , customdata=df_top_airports_departure['AIRPORT'],
                          hovertext= df_top_airports_departure['CITY'] ,hovertemplate=hovertemplate)
#subplot arrival
arrival_airports= go.Bar(x= df_top_airports_arrival['AIRLINE'],y= df_top_airports_arrival['IATA_CODE'],  marker_color= colours_airport_arr, orientation= 'h', customdata=df_top_airports_arrival['AIRPORT'],
                         hovertext= df_top_airports_arrival['CITY'], hovertemplate=hovertemplate)

fig1.add_trace(departure_airport, row= 1, col=1)
fig1.add_trace(arrival_airports, row= 1, col=2)

departure_airport_vertical= go.Bar(x= df_top_airports_departure['IATA_CODE'], y= df_top_airports_departure['AIRLINE'], marker_color= colours_airport, orientation='v', visible = False, customdata= df_top_airports_departure['AIRPORT'], hovertext= df_top_airports_departure['CITY'], hovertemplate=hovertemplate_vertical)
arrival_airports_vertical= go.Bar(x= df_top_airports_arrival['IATA_CODE'], y= df_top_airports_arrival['AIRLINE'], marker_color= colours_airport_arr, orientation='v', visible = False, customdata= df_top_airports_departure['AIRPORT'], hovertext= df_top_airports_departure['CITY'], hovertemplate=hovertemplate_vertical)

fig1.add_trace(departure_airport_vertical, row=1, col= 1)
fig1.add_trace(arrival_airports_vertical, row= 1, col=2)

#layout
fig1.update_layout(showlegend= False,title= 'Top 10 airports by flight count', title_font_size= 25, title_font_family= 'Arial black',title_x=0.5, yaxis= dict(autorange= 'reversed'), yaxis2= dict(autorange= 'reversed'), plot_bgcolor= '#fff',
                   updatemenus= [
                      dict(active= 0, buttons = list([
                          dict(label= 'Horizontal bar chart', method= 'update', args= [{'visible': [True, True,False, False]}, {'xaxis': df_top_airports_departure['AIRLINE'],'yaxis': {'y': df_top_airports_departure['IATA_CODE'], 'autorange': 'reversed'}}, {'xaxis2': df_top_airports_arrival['AIRLINE'],'yaxis2': df_top_airports_arrival['IATA_CODE']}]),
                          dict(label= 'Vertical bar chart', method= 'update', args= [{'visible': [False, False, True, True]}, {'xaxis': df_top_airports_departure['IATA_CODE'], 'yaxis': df_top_airports_departure['AIRLINE']}, {'xaxis2': df_top_airports_arrival['IATA_CODE'], 'yaxis2': df_top_airports_arrival['AIRLINE']}])
                          ]), direction= 'down',pad={"r": 10, "t": 10}, showactive= True,x=0, xanchor= 'left', yanchor= 'bottom'
                          )]
                      )
fig1.update_annotations(font = dict(family= 'Arial Black'))

fig1.show()
