import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

df = pd.read_csv('https://gist.githubusercontent.com/florianeichin/cfa1705e12ebd75ff4c321427126ccee/raw/c86301a0e5d0c1757d325424b8deec04cc5c5ca9/flights_all_cleaned.csv', sep=',')
df_airline_names = pd.read_csv('https://raw.githubusercontent.com/Leyla54/AbgabeDataVisualization/master/airlines.csv', sep= ',')
#------falls zeit ist noch total number of short,   flights hinschreiben und die ändert sich beim abwählen
colours = ['#f5c5cb', '#f5c7a9', '#e2f0cb', '#f7e5ad', '#ff9aa2', '#d8f7ad', 
          '#aadef7', '#a3a8f0', '#a4b8ac', '#f09ec8', '#d3a8f0', '#55cbcd','#c9f7e0', '#c9d2f7']
#bar chart showing overall flights categorized by short, medium and long haul 
# and seperated by colour for each airline which is visible with a hover 

#short haul: less than 807 (average of 1,100-1,500 km)
#mid haul: 807 - 2765
#long haul: more than 2765
#distance is in miles
#scheduled time is in minutes

#-------getting the data how I want it-------------
#-------adding new column with haul typ for easier categorization-------
df_airline_names.rename(columns={'AIRLINE' : 'AIRLINE_FULL_NAME'}, inplace=True)

df_haul_by_distance = df[['DISTANCE','AIRLINE']]
df_haul_by_distance = pd.merge(df_haul_by_distance, df_airline_names, left_on='AIRLINE', right_on='IATA_CODE')

conditions=[(df_haul_by_distance['DISTANCE'] < 807),(df_haul_by_distance['DISTANCE'] >= 807)&(df_haul_by_distance['DISTANCE'] <= 2765),(df_haul_by_distance['DISTANCE'] > 2765)]
values = ['short haul','mid haul','long haul']

df_haul_by_distance['HAUL_TYP'] = np.select(conditions,values)

# print(df_haul_by_distance['HAUL_TYP'].unique())
# print(df_haul_by_distance[df_haul_by_distance['HAUL_TYP']== 'short haul']['HAUL_TYP'])

df_haul_by_distance = df_haul_by_distance.sort_values(by ='HAUL_TYP', ascending=True)

df_haul_flights_grouped = df_haul_by_distance.groupby(['AIRLINE', 'HAUL_TYP'])['HAUL_TYP'].count()
df_haul_flights_grouped = df_haul_flights_grouped.unstack()
df_haul_flights_grouped = df_haul_flights_grouped.iloc[::-1]
# print(df_haul_flights_grouped.index)

df_haul_by_distance_airline = df_haul_by_distance.sort_values(by= ['AIRLINE', 'HAUL_TYP'])

print(df_haul_flights_grouped)
# print(df_haul_by_distance_airline)
# print(df_haul_by_distance_airline['HAUL_TYP'].unique())

# print(df_haul_by_distance['HAUL_TYP'].count())
# print(df_haul_by_distance[df_haul_by_distance['HAUL_TYP'] == 'long haul']['HAUL_TYP'].count())


#---------making the figure------------
fig = go.Figure()
bar = go.Bar(x = df_haul_by_distance['HAUL_TYP'].unique(), 
             y = [df_haul_by_distance[df_haul_by_distance['HAUL_TYP'] == 'long haul']['HAUL_TYP'].count(), df_haul_by_distance[df_haul_by_distance['HAUL_TYP'] == 'mid haul']['HAUL_TYP'].count(), df_haul_by_distance[df_haul_by_distance['HAUL_TYP'] == 'short haul']['HAUL_TYP'].count()],
             name = 'all flights')            
fig.add_trace(bar)


for i in range(len(df_haul_flights_grouped)):
    bar_short = go.Bar(x = df_haul_by_distance_airline['HAUL_TYP'].unique(),
                          y= df_haul_flights_grouped.loc[df_haul_flights_grouped.index[i]],
                          name = df_haul_flights_grouped.index[i], marker= dict(color= colours[i]), hovertext=df_haul_flights_grouped.index[i] ,visible= False)
    fig.add_trace(bar_short)
    

#------------array for the visibility of the different graphs--------------------
all_flight_show= []
airlines_show=[]
for visible in range(15):
    if visible == 0:
        all_flight_show.append(True)
        airlines_show.append(False)
    else :
        all_flight_show.append(False)
        airlines_show.append(True)
#---------------------------------------------------------------------------------

fig.update_traces(hoverinfo= 'text + y')
fig.update_layout(barmode = 'stack', title = 'Flights categorized by their distance and airline', title_font_size= 25,
                #   title_xanchor = 'center', title_yanchor = 'top',
                  title_font_family= 'Arial Black', legend_title_font_family = 'Arial Black',
                  xaxis_title= 'Haul Typ', yaxis_title= 'Number of Flights', xaxis_title_font_family= 'Arial Black', yaxis_title_font_family= 'Arial Black',
                  legend_title_text = 'Airlines', coloraxis= dict(colorbar= dict(title= 'Legend Title')),
                  updatemenus= [
                      dict(active= 0, buttons = list([
                          dict(label= 'Just haul typ', method= 'update', args= [{'visible': all_flight_show}, {'title': 'Flights categorized by their distance'}]),
                          dict(label= 'Haul typ and airline', method= 'update', args= [{'visible': airlines_show}, {'title': 'Flights categorized by their distance and airline'}])
                          ]), direction= 'down', showactive= True ,xanchor= 'right', yanchor= 'top'
                      )
                  ])
fig.show()





# for i in df_haul_by_distance:
#     if (df['DISTANCE'] < 807):
#         df.insert(2, 'HAUL_TYP', 'short haul')
#     elif (df['DISTANCE'] > 2765):
#         df.insert(2, 'HAUL_TYP', 'long haul')
#     else: df.insert(2, 'HAUL_TYP', 'mid haul')
#tried with for loop, didn't work, tried np.where(), but only works for 2 values

# df_haul_by_distance['HAUL_TYP']= 'short haul'
# print(df_haul_by_distance["HAUL_TYP"])

#print(df_haul_by_distance)


# for i in df_haul_by_distance:
    # if ((df_haul_by_distance['DISTANCE'][i] > 2765).any()):
    #     print()
    #     df_haul_by_distance = df_haul_by_distance['HAUL_TYP'].replace('short haul', 'long haul') 
    # elif ((807 <= df_haul_by_distance['DISTANCE'] <= 2765).any()):

# df_haul_by_distance["HAUL_TYP"] = df_haul_by_distance['HAUL_TYP'].replace('short haul', 'mid haul')
# df_haul_by_distance[df_haul_by_distance['DISTANCE'] < 807]["HAUL_TYP"] = "short haul"
# df_haul_by_distance[df_haul_by_distance['DISTANCE'] > 2765]['HAUL_TYP'] = df_haul_by_distance[df_haul_by_distance['DISTANCE'] > 2765]["HAUL_TYP"].replace('mid haul',"long haul")

# df_haul_by_distance['HAUL_TYP'] = df_haul_by_distance['DISTANCE'].transform(lambda x: 'short haul' if x < 807  else 'mid haul')

# df_haul_by_distance['HAUL_TYP'] = np.where(df['DISTANCE']< 807, 'short haul', np.NAN)

# df_haul_by_distance['HAUL_TYP'] = np.where(df['DISTANCE']< 807, 'short haul', np.NAN)
# df_haul_by_distance['HAUL_TYP'] = df_haul_by_distance.loc[df['DISTANCE']< 807, 'short haul']
# df['HAUL_TYP'] = np.where(df['DISTANCE']> 2765, 'long haul', 'mid haul')
# df['HAUL_TYP'] = np.where((df['DISTANCE']>= 807) & (df['DISTANCE']<= 2765), 'short haul')

# conditions = [
#     (df_haul_by_distance['DISTANCE'] < 807),
#     (df_haul_by_distance['DISTANCE'] >= 807) & (df_haul_by_distance['DISTANCE'] <= 2765),
#     (df_haul_by_distance['DISTANCE'] > 2765)]
# choices = ['short haul', 'mid haul', 'long haul']
# df_haul_by_distance['HAUL_TYP'] = np.select(conditions, choices)


# print(df_haul_by_distance['HAUL_TYP'] == 'short haul')
# df_mid_haul_by_distance = df[807 <= df['DISTANCE']<= 2765]