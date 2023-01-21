import dash
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.express as px
import json
import pandas as pd
from dash.dependencies import Input, Output
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from plotly.offline import iplot,init_notebook_mode
import warnings
warnings.filterwarnings('ignore')


df = pd.read_csv('data/(3)covid_19_indonesia_time_series_all.csv')
indonesia_province = json.load(open('data/indonesia-province.json','r'))
indonesia_province['features'][26]['properties']['kode'] = 1

def show_province_table(x) :
    df1 = df[['Date','Location','New Cases','New Deaths','New Recovered']]
    df1.rename(columns={'Location':'Nama Provinsi',
                      'New Cases':'Jumlah Kasus',
                      'New Deaths':'Jumlah Kematian',
                      'New Recovered':'Jumlah Kesembuhan'},
                inplace=True)
    tabel = df1[df1['Nama Provinsi'] == x]
    tabel['Date'] = pd.to_datetime(tabel['Date'])
    tabel['Hari'] = tabel['Date'].dt.day
    tabel['Bulan'] = tabel['Date'].dt.month
    tabel['Hari Terurut'] = np.arange(1,len(tabel)+1)
    tabel.index = np.arange(1,len(tabel)+1)
    return tabel

def show_line_plot(a,b,c):
    tabel = show_province_table(a)
    if b == 'Term 1' :
        fig = px.line(tabel, 
                  x=(tabel[(tabel['Bulan']>2) & (tabel['Bulan']<6)]['Hari Terurut']), 
                  y=(tabel[(tabel['Bulan']>2) & (tabel['Bulan']<6)][c]),
                  title=('Grafik Perkembangan ' + c + ' pada Term 1 di '+ a))
    elif b == 'Term 2' :
        fig = px.line(tabel,
                  x=(tabel[(tabel['Bulan']>5) & (tabel['Bulan']<8)]['Hari Terurut']),
                  y=(tabel[(tabel['Bulan']>5) & (tabel['Bulan']<8)][c]),
                  title=('Grafik Perkembangan ' + c + ' pada Term 2 di '+ a))
    elif b == 'Term 3' :
        fig = px.line(tabel,
                  x=(tabel[(tabel['Bulan']>7) & (tabel['Bulan']<10)]['Hari Terurut']),
                  y=(tabel[(tabel['Bulan']>7) & (tabel['Bulan']<10)][c]),
                  title=('Grafik Perkembangan ' + c + ' pada Term 3 di '+ a))
    elif b == 'Total' :
        fig = px.line(tabel,
                  x=tabel['Hari Terurut'],
                  y=c,
                  title=('Grafik Perkembangan ' + c + ' di '+ a))
    return fig

def get_options(nama_provinsi):
    dict_list = []
    for i in nama_provinsi:
        dict_list.append({'label': i, 'value': i})

    return dict_list


app = dash.Dash(__name__)

app.layout = html.Div([
    html.H1('Mencoba Plotly'),
    html.Div('Testing'),
    dcc.Dropdown(id='pilihan1',options=get_options(df['Location'].unique()),
                multi=False, value=[df['Location'].sort_values()[0]]
                ),
    
    dcc.Dropdown(id='pilihan2',options=[
                                {'label': 'Term 1', 'value': 'Term 1'},
                                {'label': 'Term 2', 'value': 'Term 2'},
                                {'label': 'Term 3', 'value': 'Term 3'},
                                {'label': 'Total', 'value': 'Total'}
                                ],
                multi=False, value='Term 1'
                ),

    dcc.Dropdown(id='pilihan3',options=[
                                {'label': 'Jumlah Kasus', 'value': 'Jumlah Kasus'},
                                {'label': 'Jumlah Kematian', 'value': 'Jumlah Kematian'},
                                {'label': 'Jumlah Kesembuhan', 'value': 'Jumlah Kesembuhan'}
                                ],
                multi=False, value='Jumlah Kasus'
                ),

    dcc.Graph(id='graph')
])

#---------------------------------------------------------------

@app.callback(
    Output('graph','figure'),
    [Input('pilihan1','value'),
     Input('pilihan2','value'),
     Input('pilihan3','value')]
)

def show_line_plot(a,b,c):
    tabel = show_province_table(a)
    if b == 'Term 1' :
        fig = px.line(tabel, 
                  x=(tabel[(tabel['Bulan']>2) & (tabel['Bulan']<6)]['Hari Terurut']), 
                  y=(tabel[(tabel['Bulan']>2) & (tabel['Bulan']<6)][c]),
                  title=('Grafik Perkembangan ' + c + ' pada Term 1 di '+ a))
    elif b == 'Term 2' :
        fig = px.line(tabel,
                  x=(tabel[(tabel['Bulan']>5) & (tabel['Bulan']<8)]['Hari Terurut']),
                  y=(tabel[(tabel['Bulan']>5) & (tabel['Bulan']<8)][c]),
                  title=('Grafik Perkembangan ' + c + ' pada Term 2 di '+ a))
    elif b == 'Term 3' :
        fig = px.line(tabel,
                  x=(tabel[(tabel['Bulan']>7) & (tabel['Bulan']<10)]['Hari Terurut']),
                  y=(tabel[(tabel['Bulan']>7) & (tabel['Bulan']<10)][c]),
                  title=('Grafik Perkembangan ' + c + ' pada Term 3 di '+ a))
    elif b == 'Total' :
        fig = px.line(tabel,
                  x=tabel['Hari Terurut'],
                  y=c,
                  title=('Grafik Perkembangan ' + c + ' di '+ a))
    return fig

#---------------------------------------------------------------

if __name__ == '__main__':
    app.run_server(debug=True)
