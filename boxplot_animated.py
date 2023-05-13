import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

df = pd.read_csv('https://gist.githubusercontent.com/florianeichin/cfa1705e12ebd75ff4c321427126ccee/raw/c86301a0e5d0c1757d325424b8deec04cc5c5ca9/flights_all_cleaned.csv', sep=',')

#-------------boxplot with average delay per hour-----------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------

#------------data preparation-------------------------------------------------------------------------------------
df_boxplot_destination = df[['SCHEDULED_DESTINATION', 'DESTINATION_DELAY' ]]
substring_hour_delay = []
for i in range(len(df_boxplot_destination)):
    substring_hour_delay.append(df_boxplot_destination['SCHEDULED_DESTINATION'][i][9:13:1])
    #------since its on two days, i need the reference of what day it is, so the time on jan 1st will be 100, and on 2nd 200 to differentiate between the hours

df_boxplot_destination['DESTINATION_HOUR_DELAY'] = substring_hour_delay
df_boxplot_destination['DESTINATION_HOUR_DELAY'] = df_boxplot_destination['DESTINATION_HOUR_DELAY'].str.replace(' ', '')
df_boxplot_destination['DESTINATION_HOUR_DELAY'] = df_boxplot_destination['DESTINATION_HOUR_DELAY'].astype('int64')
df_boxplot_destination = df_boxplot_destination.sort_values(by= 'SCHEDULED_DESTINATION')

#information for y-axis
time= ['01 Jan: 03 am','01 Jan: 04 am','01 Jan: 05 am','01 Jan: 06 am','01 Jan: 07 am','01 Jan: 08 am','01 Jan: 09 am','01 Jan: 10 am','01 Jan: 11 am','01 Jan: 12 pm','01 Jan: 01 pm','01 Jan: 02 pm','01 Jan: 03 pm','01 Jan: 04 pm','01 Jan: 05 pm','01 Jan: 06 pm','01 Jan: 07 pm','01 Jan: 08 pm','01 Jan: 09 pm','01 Jan: 10 pm','01 Jan: 11 pm', '02 Jan: 12 am', '02 Jan: 01 am', '02 Jan: 02 am', '02 Jan: 03 am', '02 Jan: 04 am', '02 Jan: 05 am', '02 Jan: 07 am']

#-------this didnt work atm for a day scale but i did it manually now------
# day=[]
# for number in range(28):
#     if number< 21:
#         day.append('01.01.2015')
#     else: day.append('02.01.2015')
# print(day)    


#array of dataframes
hours= []
for i in range(len(df_boxplot_destination)):
    hours.append(df_boxplot_destination['DESTINATION_HOUR_DELAY'][i])
hours = sorted(set(hours))

hour_groups = []
for hour in hours:
    hour_groups.append(df_boxplot_destination[df_boxplot_destination['DESTINATION_HOUR_DELAY']== hour])
        

#hovertemplate
hovertemplate= '<b>Min:</b> %{min}'+ '<br><b>Q1:</b> %{q1}<br>' + '<b>Median:</b> %{y}' + '<br><b>Q3:</b> %{q3}<br>' + '<b>Max:</b> %{max}<extra></extra>'
texttemplate= '<b>Min:</b> %{min}'+ '<br><b>Q1:</b> %{lower}<br>' + '<b>Median:</b> %{y}' + '<br><b>Q3:</b> %{upper}<br>' + '<b>Max:</b> %{max}<extra></extra>'

#-----------------visualization---------------------------------------------------------------------------------------------
data = []
frame_test= []

fig = go.Figure()

boxplot_3= go.Box(x= hour_groups[0]['DESTINATION_DELAY'], name= '03 am', marker_color= '#ed7b84')
for i in range(len(hour_groups)):
    frame_test.append(go.Frame(data = (go.Box(x= hour_groups[i]['DESTINATION_DELAY'], name= time[i], marker_color= '#ed7b84'))))


fig.add_trace(boxplot_3)

###########################################
fig.frames = frame_test

for frame in fig.frames:
    frame.data[0].hovertemplate=hovertemplate
###########################################



fig.update_layout(title= 'Average delay of all flights at arrival per hour',title_font_size= 25, title_font_family= 'Arial Black',
                  xaxis_title= 'Average delay in min', xaxis_title_font_family= 'Arial Black',
                  xaxis_range= [-70, 100], title_x = 0.5, yaxis_title= 'Time of day', yaxis_title_font_family= 'Arial Black',
    updatemenus=[dict(
            type='buttons',
            buttons=[dict(label= 'Play',
                          method= 'animate',
                          args=[None, dict(frame= dict(duration= 700, redraw = True), mode= 'immediate')]),
                    dict(label= 'Pause',
                         method= 'animate',
                         args= [None, dict(frame= dict(duration= 0, redraw= False), mode= 'immediate')])
                    ])]
                    )
fig.update_traces(hovertemplate=texttemplate)
fig.show()



# sliders= [dict(active = 0, yanchor= 'bottom', xanchor= 'left', currentvalue= dict(font= dict(size= 10), prefix=
#                                                                                       'text-before-value-on-display', visible= True,
#                                                                                       xanchor= 'right'),
#                                                                                       transition= dict(duration= 700, easing= 'cubic-in-out'),
#                                                                                       pad= dict(b= 20, t= 70), len= 0.9, x= 0.1, y = 0,
#                                                                                       steps= [dict(method= 'animate', label=
#                                                                                                    'label-for-frame', value= 'value-for-frame(defaults to label)', args= [dict(frame= dict(duration= 700, redraw= False),
#                                                                                                           mode= 'immediate')]) ])]



# df_boxplot_destination['SCHEDULED_DESTINATION'] = pd.to_datetime(df_boxplot_destination['SCHEDULED_DESTINATION'], format= '%Y-%m-%d %H:%M:%S')
# print(df_boxplot_destination)
# print(df_boxplot_destination['SCHEDULED_DESTINATION'].dtype)

# df_boxplot_destination_test = df_boxplot_destination.groupby(['SCHEDULED_DESTINATION']).count()
# print(df_boxplot_destination_test)

# for i in range(len(df_boxplot_destination)):
#     if (datetime.strptime('2015-01-01 00:00:00', format= '%Y-%m-%d %H:%M:%S') <= df_boxplot_destination['SCHEDULED_DESTINATION'][i]) & (df_boxplot_destination['SCHEDULED_DESTINATION'][i] <=datetime.strptime('2015-01-01 04:00:00', format= '%Y-%m-%d %H:%M:%S') ):
#         print("HALLO")