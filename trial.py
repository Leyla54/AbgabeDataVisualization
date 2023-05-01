import plotly.graph_objects as go
import numpy as np
import pandas as pd

df = pd.read_csv('https://gist.githubusercontent.com/florianeichin/cfa1705e12ebd75ff4c321427126ccee/raw/c86301a0e5d0c1757d325424b8deec04cc5c5ca9/flights_all_cleaned.csv', sep=',')
small_df = pd.read_csv('https://gist.githubusercontent.com/florianeichin/b877d354d6bc52e6ce840572e40b0497/raw/19759410471073756a388dada5fcb40109f0d13e/flights_subset_cleaned.csv', sep=',')

# fig = go.Figure()
# scatter_distance = go.Scatter(x=small_df['DISTANCE'], y=small_df['AIRLINE'], line=dict(color='red', width=4, dash='dot'))
# fig.add_trace(scatter_distance)
# fig.show()

# fig = go.Figure()
# scatter_distance = go.Scatter(x=df['DISTANCE'], y=df['AIRLINE'], line=dict(color='red', width=4, dash='dot'))
# fig.add_trace(scatter_distance)
# fig.show()

#print(df[df['DISTANCE']>4900])

print(df['SCHEDULED_TIME'].max())
