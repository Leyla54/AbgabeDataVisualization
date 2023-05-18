import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

df = pd.read_csv('https://gist.githubusercontent.com/florianeichin/cfa1705e12ebd75ff4c321427126ccee/raw/c86301a0e5d0c1757d325424b8deec04cc5c5ca9/flights_all_cleaned.csv', sep=',')
df_airline_names = pd.read_csv('https://raw.githubusercontent.com/Leyla54/AbgabeDataVisualization/master/airlines.csv', sep= ',')

colours = ['#f5c5cb', '#f5c7a9', '#e2f0cb', '#f7e5ad', '#ff9aa2', '#d8f7ad', 
          '#aadef7', '#a3a8f0', '#a4b8ac', '#f09ec8', '#d3a8f0', '#55cbcd','#c9f7e0', '#c9d2f7']

colours_long_haul= ['#e2f0cb','#f7e5ad','#a3a8f0','#d3a8f0','#c9f7e0','#c9d2f7']


#----------bar chart showing overall flights categorized by short, medium and long haul----------------------------------
#----------and seperated by colour for each airline which is visible with a hover----------------------------------------

#short haul: less than 807 (average of 1,100-1,500 km)
#mid haul: 807 - 2765
#long haul: more than 2765
#distance is in miles
#scheduled time is in minutes

#----------data preparation----------------------------------------------------------------------------------------------

#make the dataframe
df_airline_names.rename(columns={'AIRLINE' : 'AIRLINE_FULL_NAME'}, inplace=True)
df_haul_by_distance = df[['DISTANCE','AIRLINE']]
df_haul_by_distance = pd.merge(df_haul_by_distance, df_airline_names, left_on='AIRLINE', right_on='IATA_CODE')

#categorize flights by their distance
conditions=[(df_haul_by_distance['DISTANCE'] < 807),(df_haul_by_distance['DISTANCE'] >= 807)&(df_haul_by_distance['DISTANCE'] <= 2765),(df_haul_by_distance['DISTANCE'] > 2765)]
values = ['short haul','mid haul','long haul']
df_haul_by_distance['HAUL_TYP'] = np.select(conditions,values)

df_haul_by_distance = df_haul_by_distance.sort_values(by ='HAUL_TYP', ascending=True)

#df for stacked barchart to show the airlines as well
df_haul_flights_grouped = df_haul_by_distance.groupby(['AIRLINE', 'HAUL_TYP'])['HAUL_TYP'].count()
df_haul_flights_grouped = df_haul_flights_grouped.unstack()
df_haul_flights_grouped = df_haul_flights_grouped.iloc[::-1]

#df for a closer look at long haul flights
df_long_haul= df_haul_flights_grouped.dropna()
df_long_haul= df_long_haul['long haul'].astype('int64').reset_index(name= 'long haul')
df_long_haul['HAUL_TYP']= 'long haul'
df_long_haul= pd.merge(df_long_haul, df_airline_names, left_on='AIRLINE', right_on='IATA_CODE')
df_long_haul.drop('IATA_CODE', axis= 'columns', inplace=True)

#this is after getting the long haul df to not mess with the code below
df_haul_flights_grouped= pd.merge(df_haul_flights_grouped, df_airline_names, left_on='AIRLINE', right_on='IATA_CODE')

df_haul_by_distance_airline = df_haul_by_distance.sort_values(by= ['AIRLINE', 'HAUL_TYP'])

#----------hovertemplates--------------------------------------------------------------------------------------------------------

#for trace 2 & 3
hovertemplate= '<b>%{customdata}</b><br>' + '<br>Number of flights: %{y}<extra></extra>'

#for trace 1
hovertemplate_all_flights= '<extra></extra>'
#hoverinfo= None didn't work, so had to get a bit creative

#numbers on trace 1 bar chart
array_count = [df_haul_by_distance[df_haul_by_distance['HAUL_TYP'] == 'long haul']['HAUL_TYP'].count(), df_haul_by_distance[df_haul_by_distance['HAUL_TYP'] == 'mid haul']['HAUL_TYP'].count(), df_haul_by_distance[df_haul_by_distance['HAUL_TYP'] == 'short haul']['HAUL_TYP'].count()]

#------------array for the visibility of the different graphs--------------------
all_flight_show= []
airlines_show=[]
long_show=[]
for visible in range(21):
    if visible == 0:
        all_flight_show.append(True)
        airlines_show.append(False)
        long_show.append(False)
    elif visible >= 15:
        all_flight_show.append(False)
        airlines_show.append(False)
        long_show.append(True)
    else :
        all_flight_show.append(False)
        airlines_show.append(True)
        long_show.append(False)

#----------making the figure-----------------------------------------------------------------------------------------------------
fig = go.Figure()

#1st bar chart
bar = go.Bar(x = df_haul_by_distance['HAUL_TYP'].unique(), 
             y = [df_haul_by_distance[df_haul_by_distance['HAUL_TYP'] == 'long haul']['HAUL_TYP'].count(), df_haul_by_distance[df_haul_by_distance['HAUL_TYP'] == 'mid haul']['HAUL_TYP'].count(), df_haul_by_distance[df_haul_by_distance['HAUL_TYP'] == 'short haul']['HAUL_TYP'].count()],
             name = 'all flights', marker= dict(color= '#6f78a5'), text= array_count,
             textposition='auto', hovertemplate= hovertemplate_all_flights)            
fig.add_trace(bar)


#2nd bar chart
for i in range(len(df_haul_flights_grouped)):
    bar_short = go.Bar(x = df_haul_by_distance_airline['HAUL_TYP'].unique(),
                          y= df_haul_flights_grouped.loc[df_haul_flights_grouped.index[i]],
                          name = df_haul_flights_grouped.iloc[i]['IATA_CODE'], customdata = [df_haul_flights_grouped.iloc[i]['AIRLINE_FULL_NAME'] ,df_haul_flights_grouped.iloc[i]['AIRLINE_FULL_NAME'],df_haul_flights_grouped.iloc[i]['AIRLINE_FULL_NAME']], hovertemplate=hovertemplate, marker= dict(color= colours[i], line= dict(color= 'white', width= 1)),visible= False)
    fig.add_trace(bar_short)



#3rd bar chart
for i in range(len(df_long_haul)):
    bar_long= go.Bar(x= [df_long_haul.iloc[i]['HAUL_TYP']] ,y= [df_long_haul.iloc[i]['long haul']],
                  name= df_long_haul.iloc[i]['AIRLINE'] ,marker= dict(color= colours_long_haul[i], line= dict(color= 'white', width= 1)),
                   customdata= [df_long_haul.iloc[i]['AIRLINE_FULL_NAME']],hovertemplate=hovertemplate, visible= False)
    fig.add_trace(bar_long)

#layout
fig.update_layout(barmode = 'stack', title = 'Flights categorized by their distance and airline', title_font_size= 25, title_x=0.5,
                  title_font_family= 'Arial Black', legend_title_font_family = 'Arial Black',
                  xaxis_title= 'Haul Typ', yaxis_title= 'Number of Flights', xaxis_title_font_family= 'Arial Black', yaxis_title_font_family= 'Arial Black',
                  legend_title_text = 'Airlines', coloraxis= dict(colorbar= dict(title= 'Legend Title')), waterfallgroupgap= 1, 
                  updatemenus= [
                      dict(active= 0, buttons = list([
                          dict(label= 'Just haul typ', method= 'update', args= [{'visible': all_flight_show}, {'title': 'Flights categorized by their distance'}]),
                          dict(label= 'Haul typ and airline', method= 'update', args= [{'visible': airlines_show}, {'title': 'Flights categorized by their distance and airline'}]),
                          dict(label= 'Long haul and airlines', method= 'update', args= [{'visible': long_show}, {'title': 'Closer look at the long haul flights'}]),
                          ]), direction= 'down', showactive= True ,xanchor= 'right', yanchor= 'top', x=1, y= 1.05
                      )
                  ])
fig.show()
