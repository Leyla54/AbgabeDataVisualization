import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots

df = pd.read_csv('https://gist.githubusercontent.com/florianeichin/cfa1705e12ebd75ff4c321427126ccee/raw/c86301a0e5d0c1757d325424b8deec04cc5c5ca9/flights_all_cleaned.csv', sep=',')

#-------------animated boxplot with average delay per hour-----------------------------------------------------------------
#-----------------------------------------------------------------------------------------------------------------

#------------data preparation-------------------------------------------------------------------------------------
df_boxplot_destination = df[['SCHEDULED_DESTINATION', 'DESTINATION_DELAY' ]]
substring_hour_delay = []
for i in range(len(df_boxplot_destination)):
    substring_hour_delay.append(df_boxplot_destination['SCHEDULED_DESTINATION'][i][9:13:1])
    #since its on two days, i need the reference of what day it is, so the time on jan 1st will be 100,
    # and on 2nd 200 to differentiate between the hours

#adding as new column & changing dtype
df_boxplot_destination['DESTINATION_HOUR_DELAY'] = substring_hour_delay
df_boxplot_destination['DESTINATION_HOUR_DELAY'] = df_boxplot_destination['DESTINATION_HOUR_DELAY'].str.replace(' ', '')
df_boxplot_destination['DESTINATION_HOUR_DELAY'] = df_boxplot_destination['DESTINATION_HOUR_DELAY'].astype('int64')
df_boxplot_destination = df_boxplot_destination.sort_values(by= 'SCHEDULED_DESTINATION')

#information for y-axis
time= ['01 Jan: 03 am','01 Jan: 04 am','01 Jan: 05 am','01 Jan: 06 am','01 Jan: 07 am','01 Jan: 08 am','01 Jan: 09 am','01 Jan: 10 am','01 Jan: 11 am','01 Jan: 12 pm','01 Jan: 01 pm','01 Jan: 02 pm','01 Jan: 03 pm','01 Jan: 04 pm','01 Jan: 05 pm','01 Jan: 06 pm','01 Jan: 07 pm','01 Jan: 08 pm','01 Jan: 09 pm','01 Jan: 10 pm','01 Jan: 11 pm', '02 Jan: 12 am', '02 Jan: 01 am', '02 Jan: 02 am', '02 Jan: 03 am', '02 Jan: 04 am', '02 Jan: 05 am', '02 Jan: 07 am']

#array with data from the new column
hours= []
for i in range(len(df_boxplot_destination)):
    hours.append(df_boxplot_destination['DESTINATION_HOUR_DELAY'][i])
hours = sorted(set(hours))

#array of dataframes (row with same hour will be put in an array together inside an array)
hour_groups = []
for hour in hours:
    hour_groups.append(df_boxplot_destination[df_boxplot_destination['DESTINATION_HOUR_DELAY']== hour])
        

#-----------------visualization---------------------------------------------------------------------------------------------
data = []
frame_test= []

fig = go.Figure()

#initial boxplot seen before pressing play
boxplot_3= go.Box(x= hour_groups[0]['DESTINATION_DELAY'], name= '03 am', marker_color= '#ed7b84')

#establishing frames for animation
for i in range(len(hour_groups)):
    frame_test.append(go.Frame(data = (go.Box(x= hour_groups[i]['DESTINATION_DELAY'], name= time[i], marker_color= '#ed7b84'))))

fig.add_trace(boxplot_3)

#layout
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

fig.show()