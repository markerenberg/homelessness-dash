# ======== Scrape site for data ======== #

#import imports

import os
import time
import numpy as np
import pandas as pd
import requests
import matplotlib.pyplot as plt
import seaborn as sns
from bs4 import BeautifulSoup
import plotly.express as px
import plotly
import dash_core_components as dcc
import dash_html_components as html

# Get data files
local_path = r'C:\Users\marke\Downloads\Datasets\Toronto_Homelessness'
sna_export = pd.read_csv(local_path+r'\sna2018opendata_export.csv').fillna(0)
sna_rows = pd.read_csv(local_path+r'\sna2018opendata_keyrows.csv')
sna_cols = pd.read_csv(local_path+r'\sna2018opendata_keycolumns.csv')
shelter_flow = pd.read_csv(local_path+r'\toronto-shelter-system-flow_march4.csv')
occupancy_curr = pd.read_csv(local_path+r'\Daily_shelter_occupancy_current.csv')
occupancy_2020 = pd.read_csv(local_path+r'\daily-shelter-occupancy-2020.csv')

################### Street Needs Assessment ###################
sna_export = sna_export.merge(sna_rows.iloc[:,:3],on='SNA RESPONSE CATEGORY')

# Pivot on question-response
q_cols = ['SNA RESPONSE CATEGORY','QUESTION/CATEGORY DESCRIPTION','RESPONSE']
shelter_cols = ['OUTDOORS','CITY-ADMINISTERED SHELTERS','24-HR RESPITE','VAW SHELTERS']
dem_cols = ['SINGLE ADULTS','FAMILY','YOUTH']

sna_melt = sna_export.melt(id_vars=q_cols,value_vars=shelter_cols+dem_cols,
                           var_name='GROUP',value_name='COUNT')

# Track count/average responses
avg_cols = [cat for cat in sna_melt['SNA RESPONSE CATEGORY'].unique() if ('AVERAGE' in cat)]
cnt_cols = [cat for cat in sna_melt['SNA RESPONSE CATEGORY'].unique() if ('COUNT' in cat)]

# Plot bar graph of question-response
q1 = sna_export[sna_export['QUESTION/CATEGORY DESCRIPTION']=='What family members are staying with you tonight?']
fig = px.bar(q1, x="RESPONSE", y=shelter_cols, title='What family members are staying with you tonight?')
fig.show()

q1 = sna_melt.loc[(sna_melt['QUESTION/CATEGORY DESCRIPTION']=='What family members are staying with you tonight?')\
    &(~sna_melt['SNA RESPONSE CATEGORY'].isin(cnt_cols))\
    &(sna_melt['GROUP'].isin(shelter_cols))]
fig = px.bar(q1, x="RESPONSE", y="COUNT", color="GROUP", title="What family members are staying with you tonight?")
#fig.show()
plotly.offline.plot(fig)

################### Build Dash ###################