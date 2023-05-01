import plotly.graph_objects as go
import numpy as np
import pandas as pd
from plotly.subplots import make_subplots
from datetime import datetime

df = pd.read_csv('https://gist.githubusercontent.com/florianeichin/cfa1705e12ebd75ff4c321427126ccee/raw/c86301a0e5d0c1757d325424b8deec04cc5c5ca9/flights_all_cleaned.csv', sep=',')

'''add Pause Button
    add Slider with hours
    make scale
    what to do with outliers
    looks
    hover'''

#boxplot with average delay per hour
#frames with for loop

df_boxplot_destination = df[['SCHEDULED_DESTINATION', 'DESTINATION_DELAY' ]]
substring_hour_delay = []
for i in range(len(df_boxplot_destination)):
    substring_hour_delay.append(df_boxplot_destination['SCHEDULED_DESTINATION'][i][9:13:1])
    #------since its on two days, i need the reference of what day it is, so the time on jan 1st will be 100, and on 2nd 200 to differentiate between the hours

df_boxplot_destination['DESTINATION_HOUR_DELAY'] = substring_hour_delay
df_boxplot_destination['DESTINATION_HOUR_DELAY'] = df_boxplot_destination['DESTINATION_HOUR_DELAY'].str.replace(' ', '')
df_boxplot_destination['DESTINATION_HOUR_DELAY'] = df_boxplot_destination['DESTINATION_HOUR_DELAY'].astype('int64')
df_boxplot_destination = df_boxplot_destination.sort_values(by= 'SCHEDULED_DESTINATION')

#print(df_boxplot_destination.groupby(['DESTINATION_HOUR_DELAY']).count())

print(df_boxplot_destination.dtypes)

hours= []
for i in range(len(df_boxplot_destination)):
    hours.append(df_boxplot_destination['DESTINATION_HOUR_DELAY'][i])
hours = sorted(set(hours))

hour_groups = []
for hour in hours:
    hour_groups.append(df_boxplot_destination[df_boxplot_destination['DESTINATION_HOUR_DELAY']== hour])

print(hour_groups)
#array of dataframes
        

#print(substring_hour_delay)

data = []
frame_test= []
fig = go.Figure()
boxplot_3= go.Box(x= hour_groups[0]['DESTINATION_DELAY'], name= '')
for i in range(len(hour_groups)):
    frame_test.append(go.Frame(data = (go.Box(x= hour_groups[i]['DESTINATION_DELAY']))))

fig.add_trace(boxplot_3)
fig.frames = frame_test
#fig.add_trace(frame_test)
fig.update_layout(title= 'Average delay of all flights per hour',title_font_size= 25, title_font_family= 'Arial Black',
                  xaxis_title= 'Average delay in min', xaxis_title_font_family= 'Arial Black',
                  xaxis_range= [-50, 100],
    updatemenus=[dict(
            type='buttons',
            buttons=[dict(label= 'Play',
                          method= 'animate',
                          args=[None, dict(frame= dict(duration= 700, redraw = True), mode= 'immediate')]),
                    dict(label= 'Pause',
                         method= 'animate',
                         args= [None, dict(frame= dict(duration= 0, redraw= False), mode= 'immediate')])
                    ])])
fig.show()










# df_boxplot_destination['SCHEDULED_DESTINATION'] = pd.to_datetime(df_boxplot_destination['SCHEDULED_DESTINATION'], format= '%Y-%m-%d %H:%M:%S')
# print(df_boxplot_destination)
# print(df_boxplot_destination['SCHEDULED_DESTINATION'].dtype)

# df_boxplot_destination_test = df_boxplot_destination.groupby(['SCHEDULED_DESTINATION']).count()
# print(df_boxplot_destination_test)

# for i in range(len(df_boxplot_destination)):
#     if (datetime.strptime('2015-01-01 00:00:00', format= '%Y-%m-%d %H:%M:%S') <= df_boxplot_destination['SCHEDULED_DESTINATION'][i]) & (df_boxplot_destination['SCHEDULED_DESTINATION'][i] <=datetime.strptime('2015-01-01 04:00:00', format= '%Y-%m-%d %H:%M:%S') ):
#         print("HALLO")