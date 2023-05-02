import plotly.graph_objects as go
import numpy as np
import pandas as pd
from urllib.request import urlopen
import json
from plotly.subplots import make_subplots

df = pd.read_csv('https://gist.githubusercontent.com/florianeichin/cfa1705e12ebd75ff4c321427126ccee/raw/c86301a0e5d0c1757d325424b8deec04cc5c5ca9/flights_all_cleaned.csv', sep=',')
df_states= pd.read_csv('https://raw.githubusercontent.com/Leyla54/AbgabeDataVisualization/master/airports.csv', sep= ',')

url_united_states= ''
token= 'pk.eyJ1IjoibGV5bGExMyIsImEiOiJjbGZtbHV3bGMwY21yNDNtbXJhdmFwaTE2In0.HEUGOzuyzJbiE0oz4RrwEQ'
