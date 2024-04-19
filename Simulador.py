#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
from pylab import rcParams
import matplotlib.pyplot as plt
import dash_auth

import plotly
import plotly.graph_objects as go
from datetime import datetime

import dash
import dash_core_components as dcc 
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output

from datetime import date
from datetime import datetime as dt


# In[2]:


## Listas
anio=[2021,2022,2023]
cadena=['WALMART','NACIONAL1']
formato=['WM-SUPER CENTER','WM-SUPER CENTER-2']
categoria=['027 Pastas']
linea=['068 BARILLA SEMOLINA NACIONAL']


# In[11]:


VALID_USERNAME_PASSWORD_PAIRS = {'HERDEZ': 'HERDEZ'}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
#app = dash.Dash(__name__)

server = app.server
auth = dash_auth.BasicAuth(app,VALID_USERNAME_PASSWORD_PAIRS)
app.layout = html.Div([
    
    html.Div([
        html.H1('Prueba de parametros - SIMULADOR/CHARLES', style={'fontSize': 30,'font-family':'sans-serif', 'color':'red'}),
        html.Img(src='assets/HERDEZ.png')
    ],style = {}, className = 'banner'),

    html.Div([
        html.Div([html.P('Año:', className = 'fix_label', style={'fontSize': 20,'color':'green', 'margin-top': '4px'}),
            dcc.Dropdown(id="ANIO",options=anio,value=2021,multi=False,className="dropdown")]),
    ]),
    html.Div([
        html.Div([html.P('Cadena:', className = 'fix_label', style={'fontSize': 18,'color':'green', 'margin-top': '4px'}),
            dcc.Dropdown(id="CADENA",options=cadena,value='WALMART',multi=False,className="dropdown")]),
    ]),

    html.Div([
        html.Div([html.P('Formato:', className = 'fix_label', style={'fontSize': 18,'color':'green', 'margin-top': '4px'}),
            dcc.Dropdown(id="FORMATO",options=formato,value='WM-SUPER CENTER',multi=False,className="dropdown")]),
    ]),

    html.Div([
        html.Div([html.P('Categoria:', className = 'fix_label', style={'fontSize': 18,'color':'green', 'margin-top': '4px'}),
            dcc.Dropdown(id="CATEGORIA",options=categoria,value='027 Pastas',multi=False,className="dropdown")]),
    ]),

    html.Div([
        html.Div([html.P('Línea:', className = 'fix_label', style={'fontSize': 18,'color':'green', 'margin-top': '4px'}),
            dcc.Dropdown(id="LINEA",options=linea,value='068 BARILLA SEMOLINA NACIONAL',multi=False,className="dropdown")]),
    ]),

    html.Div([
        html.Div([html.P('Rango de Fechas:', className = 'fix_label', style={'fontSize': 18,'color':'green', 'margin-top': '4px'}),
             dcc.DatePickerRange(
        id='Calendario',
        calendar_orientation='horizontal',  # formato del calentadio
        start_date_placeholder_text="Fecha inicial",
        end_date_placeholder_text="Fecha final",  # etiquetas de inicio y fin
        with_portal=True,  # Si True, abre en toda la pantalla
        first_day_of_week=0,  # Display del calendar abierto (0 = Sunday)
        reopen_calendar_on_clear=True,
        clearable=True,  # Calendario limpiable
        number_of_months_shown=3,  # numero de meses a observar
        min_date_allowed=dt(2022, 1, 1),  # Fecha minima para seleccionar
        max_date_allowed=dt(2023, 6, 20),  # Fecha maxima para seleccionar
        display_format='MMMM Y, DD',  
        month_format='MMMM Y'  

    )            
                 ]),
    ]),

    
    
##################################################################------------------------------
    html.Div([
        html.Div([
            dcc.Graph(id = 'CURVAS', figure = {})
        ], className = 'create_container1 eight columns'),
        html.Div([
            dcc.Graph(id = 'INDICADOR', figure = {})
        ], className = 'create_container1 four columns'),
        html.Div([
            dcc.Graph(id = 'INDICADORR', figure = {})
        ], className = 'create_container1 four columns'),
        
    ], className = 'row flex-display'),
    
##################################################################------------------------------
    html.Div([
        html.H1('Escenario 1', style={'fontSize': 25,'font-family':'sans-serif'})
    ],style = {}, className = 'banner3'),
    
    html.Div([
        html.Div([
            dcc.Graph(id = 'INDICADOR6', figure = {})
        ], className = 'create_container1 five columns'),
        html.Div([
            dcc.Graph(id = 'INDICADOR5', figure = {})
        ], className = 'create_container1 eight columns'),
        
    ], className = 'row flex-display'),
    
    
##################################################################------------------------------
    html.Div([
        html.H1('Escenario 2', style={'fontSize': 25,'font-family':'sans-serif'})
    ],style = {}, className = 'banner3'),
    
    html.Div([
        html.Div([
            dcc.Graph(id = 'INDICADOR66', figure = {})
        ], className = 'create_container1 five columns'),
        html.Div([
            dcc.Graph(id = 'INDICADOR55', figure = {})
        ], className = 'create_container1 eight columns'),
        
    ], className = 'row flex-display'),
    
##################################################################------------------------------
    html.Div([
        html.H1('Comparativo de escenarios', style={'fontSize': 35,'font-family':'sans-serif'})
    ],style = {}, className = 'banner3'),
    
    html.Div([
        html.Div([
            dcc.Graph(id = 'INDICADOR2', figure = {})
        ], className = 'create_container1 five columns'),
        html.Div([
            dcc.Graph(id = 'INDICADOR3', figure = {})
        ], className = 'create_container1 five columns'),
        html.Div([
            dcc.Graph(id = 'INDICADOR4', figure = {})
        ], className = 'create_container1 five columns'),
        
    ], className = 'row flex-display'),
    
##################################################################------------------------------
    html.Div([
        html.H1('', style={'fontSize': 25,'font-family':'sans-serif'})
    ],style = {}, className = 'banner2'),
##################################################################------------------------------
], id='mainContainer', style={'display':'flex', 'flex-direction':'column'})


@app.callback(
    Output('mymap', 'figure'),
    [Input('Calendario', 'start_date'),
     Input('Calendario', 'end_date'),])
def update_output(start_date, end_date):
    fig = go.Figure()
    return fig


@app.callback(
    Output("CURVAS", "figure"),
    [Input("RECURSO","value")
    ])
def update_graph(recurso):


    fig = go.Figure()
    fig.update_layout(title="GRÁFICA - 1",height=400)
    return fig

@app.callback(
    Output("INDICADOR", "figure"),
    [Input("RECURSO","value"),
     Input("COBERTURA","value")
    ])
def update_graph(recurso,cobertura):
    fig = go.Figure()
    fig.update_layout(title="GRÁFICA - 2",height=400)
    return fig

@app.callback(
    Output("INDICADORR", "figure"),
    [Input("RECURSO","value"),
     Input("COBERTURA","value")
    ])
def update_graph(recurso,cobertura):
    fig = go.Figure()
    fig.update_layout(title="GRÁFICA - 3",height=400)
    return fig

@app.callback(
    Output("INDICADOR2", "figure"),
    [Input("RECURSO","value"),
    ])
def update_graph(recurso):
    fig = go.Figure()
    fig.update_layout(title="DATOS - 1",height=400)
    return fig

@app.callback(
    Output("INDICADOR3", "figure"),
    [Input("RECURSO","value"),
    ])
def update_graph(recurso):
    fig = go.Figure()
    fig.update_layout(title="DATOS - 2",height=400)
    return fig

@app.callback(
    Output("INDICADOR4", "figure"),
    [Input("RECURSO","value"),
    ])
def update_graph(recurso):
    fig = go.Figure()
    fig.update_layout(title="DATOS - 3",height=400)
    return fig

@app.callback(
    Output("INDICADOR5", "figure"),
    [Input("RECURSO","value"),
    ])
def update_graph(recurso):
    fig = go.Figure()
    fig.update_layout(title="DATOS - 4",height=400)
    return fig

@app.callback(
    Output("INDICADOR6", "figure"),
    [Input("RECURSO","value"),
    ])
def update_graph(recurso):
    fig = go.Figure()
    fig.update_layout(title="DATOS - 5",height=400)
    return fig

@app.callback(
    Output("INDICADOR55", "figure"),
    [Input("RECURSO","value"),
    ])
def update_graph(recurso):
    fig = go.Figure()
    fig.update_layout(title="DATOS - 4",height=400)
    return fig

@app.callback(
    Output("INDICADOR66", "figure"),
    [Input("RECURSO","value"),
    ])
def update_graph(recurso):
    fig = go.Figure()
    fig.update_layout(title="DATOS - 5",height=400)
    return fig



if __name__ == ('__main__'):
    app.run_server()


# In[ ]:





# In[ ]:





# In[ ]:




