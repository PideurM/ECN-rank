import pandas as pd
import streamlit as st
import numpy as np
import plotly.graph_objects as go
import plotly.express as px
import datetime

import datetime

@st.cache
def get_and_process_data():
    data = pd.read_html('https://www.cngsante.fr/chiron/celine/limite.html',header=1)
    data = data[0]
    data = data.iloc[-2].to_frame()
    data.rename(columns={data.columns[0]:'rang'},inplace=True)
    data.dropna(axis=0, inplace=True)
    data = data.rang.str.split(' ',expand=True)
    data.rename(columns={0:'Rang_1er_admis',1:'Rang_dernier_admis'},inplace=True)
    for e,i in data[data.columns[1]].items():
        data[data.columns[1]][e] = i[:4]
    data = data.rename_axis('Spécialités').reset_index()
    for e,i in data['Spécialités'].items():
        data['Spécialités'][e] = i[:3] + ' - ' + i[3:]
    data = data.set_index('Spécialités')
    return data.iloc[:-1,:]

data = get_and_process_data()
now = datetime.datetime.now()

st.header('Rang ECN à ce jour ' + now.strftime("%d-%m-%Y"))
selected_specialities = st.multiselect('Spécialités',data.index)
st.write('Choisis les rangs à consulter :')
first_rank = st.checkbox('Premier admis')
last_rank = st.checkbox('Dernier admis')

if last_rank and first_rank:
    data_selected = data[(data.index.isin(selected_specialities))]
    st.dataframe(data_selected)

elif first_rank:
    data_selected = data[(data.index.isin(selected_specialities))]
    st.dataframe(data_selected['Rang_1er_admis'])

elif last_rank:
    data_selected = data[(data.index.isin(selected_specialities))]
    st.dataframe(data_selected['Rang_dernier_admis'])
