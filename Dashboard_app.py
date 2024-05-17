#!/usr/bin/env python
# coding: utf-8

import pandas as pd
#from pylab import rcParams
#import matplotlib.pyplot as plt
#import dash_auth
import numpy as np

import plotly
import plotly.graph_objects as go
from datetime import datetime

import dash
import dash_core_components as dcc 
import dash_html_components as html
import plotly.express as px
from dash.dependencies import Input, Output, State

import dash_bootstrap_components as dbc


DAT=pd.read_csv('DATOS_2.csv')
DATOS=DAT.groupby(['PERIODO','SUCURSAL','PROVEEDOR','EDITORIAL_','TEMA_']).sum().reset_index()

DATOS=DATOS[['SUCURSAL','PROVEEDOR','EDITORIAL_','TEMA_']]
DATOS.columns=['SUCURSAL','PROVEEDOR','EDITORIAL','TEMA']

df1=pd.concat([DATOS])
df2=pd.concat([DATOS])
df2['SUCURSAL']='TOTAL'
df3=pd.concat([df2,df1])

df11=pd.concat([df3])
df21=pd.concat([df3])
df21['PROVEEDOR']='TOTAL'
df31=pd.concat([df21,df11])

df111=pd.concat([df31])
df211=pd.concat([df31])
df211['EDITORIAL']='TOTAL'
df311=pd.concat([df211,df111])

df1111=pd.concat([df311])
df2111=pd.concat([df311])
df2111['TEMA']='TOTAL'
DATOS=pd.concat([df2111,df1111])




#VALID_USERNAME_PASSWORD_PAIRS = {
 #   'OGUTI': 'OGUTI','HERDEZ': 'HERDEZ'}
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__,suppress_callback_exceptions = True, external_stylesheets=[dbc.themes.SPACELAB])
server = app.server
#auth = dash_auth.BasicAuth(app,VALID_USERNAME_PASSWORD_PAIRS)


Sucursal = DATOS['SUCURSAL'].unique()

Suc = html.Div(
    [   dbc.Label("Sucursal", html_for="cadena"),
        dcc.Dropdown(id='Sucursal', options=[{'label': i, 'value': i} for i in Sucursal],placeholder='Selecciona...'),
    ],className="mt-2",)

Prov = html.Div(
    [   dbc.Label("Proveedor", html_for="formato"),
        dcc.Dropdown(id='Proveedor',placeholder='Selecciona...'),
    ],className="mt-2",)

Edit = html.Div(
    [   dbc.Label("Producto", html_for="categoria"),
        dcc.Dropdown(id='Producto',placeholder='Selecciona...'),
    ],className="mt-2",)



button=html.Div(
    [dbc.Button('Consulta',id='button', color="primary")],
    )




control_panel = dbc.Card(
    dbc.CardBody(
    [html.Div("", className="text-center",style={'fontSize': 20}),
        dbc.Row([dbc.Col(Suc, md=4), dbc.Col(Prov, md=4),dbc.Col(Edit, md=4)]),
     html.Div(".",className='text-center' , style={'color': 'rgb(255,255,255)','fontSize': 8}),
      html.Div(button),

     
    ],))


logo_up= html.Img(src='assets/enigma.png',height='145px')



FIGURA1=html.Div(id='FIGURA')



TABS=dcc.Tabs([
        dcc.Tab(label='Enfoque Descriptivo', children=[control_panel,FIGURA1],selected_style={'font-size': '18px'},
            style={'font-size': '16px'}),

        dcc.Tab(label='Enfoque Predictivo', children=[],selected_style={'font-size': '18px'},
            style={'font-size': '16px'}),

        dcc.Tab(label='Inteligencia Artificial', children=[] ,selected_style={'font-size': '18px'},
            style={'font-size': '18px'}),
        ])


separa1=html.Div(style={'border-top': '15px solid rgb(244,204,159)'})
separa2=html.Div(style={'border-top': '15px solid rgb(39,161,158)'})

app.layout = html.Div([logo_up,separa2,separa1,TABS])



@app.callback(
    Output('Proveedor', 'options'),
    [Input('Sucursal', 'value')]
)
def update_dropdown_estado(Cadena):
    estados_filtrados = DATOS[DATOS['SUCURSAL'] == Cadena]['PROVEEDOR'].unique()
    options = [{'label': estado, 'value': estado} for estado in estados_filtrados]

    return options

@app.callback(
    Output('Producto', 'options'),
    [Input('Sucursal', 'value'),
     Input('Proveedor', 'value')]
)
def update_dropdown_region(Cadena, Formato):
    regiones_filtradas = DATOS[(DATOS['SUCURSAL'] == Cadena) & (DATOS['PROVEEDOR'] == Formato)]['EDITORIAL'].unique()
    options = [{'label': region, 'value': region} for region in regiones_filtradas]

    return options



@app.callback(
     Output('FIGURA', 'children'),
    [Input('button', 'n_clicks'),Input('Sucursal', 'value')
    ,Input('Proveedor', 'value'),Input('Producto', 'value')]
)

def perform_operation(n_clicks,Sucursal,Proveedor,Producto):
    if n_clicks is None:
        return [],[]
    else:
        Sucursal = f'{Sucursal}'
        Proveedor = f'{Proveedor}'
        Editorial = f'{Producto}'
        Tema = 'TOTAL'

        datos_general=DAT.groupby(['PROVEEDOR','TEMA_']).sum()[['TOTAL_VENTA']].reset_index()

        if Sucursal=='TOTAL':
            datos_general=DAT.groupby(['PROVEEDOR','TEMA_']).sum()[['TOTAL_VENTA']].reset_index()

            if Proveedor=='TOTAL':
                if Editorial=='TOTAL':
                    df=DAT[(DAT['PERIODO']==2021)].groupby(['MES','N_mes_ven']).sum()[['TOTAL_VENTA']].reset_index()
                    df1=DAT[(DAT['PERIODO']==2022)].groupby(['MES','N_mes_ven']).sum()[['TOTAL_VENTA']].reset_index()
                    
                    df_0=DAT[(DAT['PERIODO']==2021)].groupby(['MES','N_mes_ven']).mean()[['PRECIO_LISTA']].reset_index()
                    df_1=DAT[(DAT['PERIODO']==2022)].groupby(['MES','N_mes_ven']).mean()[['PRECIO_LISTA']].reset_index()
                    
                else:
                    df=DAT[(DAT['EDITORIAL_']==Editorial)&(DAT['PERIODO']==2021)].groupby(['MES','N_mes_ven']).sum()[['TOTAL_VENTA']].reset_index()
                    df1=DAT[(DAT['EDITORIAL_']==Editorial)&(DAT['PERIODO']==2022)].groupby(['MES','N_mes_ven']).sum()[['TOTAL_VENTA']].reset_index()

                    df_0=DAT[(DAT['EDITORIAL_']==Editorial)&(DAT['PERIODO']==2021)].groupby(['MES','N_mes_ven']).mean()[['PRECIO_LISTA']].reset_index()
                    df_1=DAT[(DAT['EDITORIAL_']==Editorial)&(DAT['PERIODO']==2022)].groupby(['MES','N_mes_ven']).mean()[['PRECIO_LISTA']].reset_index()

            else:
                if Editorial=='TOTAL':
                    df=DAT[(DAT['PROVEEDOR']==Proveedor)&(DAT['PERIODO']==2021)].groupby(['MES','N_mes_ven']).sum()[['TOTAL_VENTA']].reset_index()
                    df1=DAT[(DAT['PROVEEDOR']==Proveedor)&(DAT['PERIODO']==2022)].groupby(['MES','N_mes_ven']).sum()[['TOTAL_VENTA']].reset_index()
                    df_0=DAT[(DAT['PROVEEDOR']==Proveedor)&(DAT['PERIODO']==2021)].groupby(['MES','N_mes_ven']).mean()[['PRECIO_LISTA']].reset_index()
                    df_1=DAT[(DAT['PROVEEDOR']==Proveedor)&(DAT['PERIODO']==2022)].groupby(['MES','N_mes_ven']).mean()[['PRECIO_LISTA']].reset_index()

                else:
                    df=DAT[(DAT['PROVEEDOR']==Proveedor)&(DAT['EDITORIAL_']==Editorial)&(DAT['PERIODO']==2021)].groupby(['MES','N_mes_ven']).sum()[['TOTAL_VENTA']].reset_index()
                    df1=DAT[(DAT['PROVEEDOR']==Proveedor)&(DAT['EDITORIAL_']==Editorial)&(DAT['PERIODO']==2022)].groupby(['MES','N_mes_ven']).sum()[['TOTAL_VENTA']].reset_index()
                    df_0=DAT[(DAT['PROVEEDOR']==Proveedor)&(DAT['EDITORIAL_']==Editorial)&(DAT['PERIODO']==2021)].groupby(['MES','N_mes_ven']).mean()[['PRECIO_LISTA']].reset_index()
                    df_1=DAT[(DAT['PROVEEDOR']==Proveedor)&(DAT['EDITORIAL_']==Editorial)&(DAT['PERIODO']==2022)].groupby(['MES','N_mes_ven']).mean()[['PRECIO_LISTA']].reset_index()

        else:
            datos_general=DAT[DAT['SUCURSAL']==Sucursal].groupby(['PROVEEDOR','TEMA_']).sum()[['TOTAL_VENTA']].reset_index()

            if Proveedor=='TOTAL':                
                if Editorial=='TOTAL':
                    df=DAT[(DAT['SUCURSAL']==Sucursal)&(DAT['PERIODO']==2021)].groupby(['MES','N_mes_ven']).sum()[['TOTAL_VENTA']].reset_index()
                    df1=DAT[(DAT['SUCURSAL']==Sucursal)&(DAT['PERIODO']==2022)].groupby(['MES','N_mes_ven']).sum()[['TOTAL_VENTA']].reset_index()
                    df_0=DAT[(DAT['SUCURSAL']==Sucursal)&(DAT['PERIODO']==2021)].groupby(['MES','N_mes_ven']).mean()[['PRECIO_LISTA']].reset_index()
                    df_1=DAT[(DAT['SUCURSAL']==Sucursal)&(DAT['PERIODO']==2022)].groupby(['MES','N_mes_ven']).mean()[['PRECIO_LISTA']].reset_index()

                else:
                    df=DAT[(DAT['SUCURSAL']==Sucursal)&(DAT['EDITORIAL_']==Editorial)&(DAT['PERIODO']==2021)].groupby(['MES','N_mes_ven']).sum()[['TOTAL_VENTA']].reset_index()
                    df1=DAT[(DAT['SUCURSAL']==Sucursal)&(DAT['EDITORIAL_']==Editorial)&(DAT['PERIODO']==2022)].groupby(['MES','N_mes_ven']).sum()[['TOTAL_VENTA']].reset_index()
                    df_0=DAT[(DAT['SUCURSAL']==Sucursal)&(DAT['EDITORIAL_']==Editorial)&(DAT['PERIODO']==2021)].groupby(['MES','N_mes_ven']).mean()[['PRECIO_LISTA']].reset_index()
                    df_1=DAT[(DAT['SUCURSAL']==Sucursal)&(DAT['EDITORIAL_']==Editorial)&(DAT['PERIODO']==2022)].groupby(['MES','N_mes_ven']).mean()[['PRECIO_LISTA']].reset_index()

            else:
                if Editorial=='TOTAL':
                    df=DAT[(DAT['SUCURSAL']==Sucursal)&(DAT['PROVEEDOR']==Proveedor)&(DAT['PERIODO']==2021)].groupby(['MES','N_mes_ven']).sum()[['TOTAL_VENTA']].reset_index()
                    df1=DAT[(DAT['SUCURSAL']==Sucursal)&(DAT['PROVEEDOR']==Proveedor)&(DAT['PERIODO']==2022)].groupby(['MES','N_mes_ven']).sum()[['TOTAL_VENTA']].reset_index()
                    df_0=DAT[(DAT['SUCURSAL']==Sucursal)&(DAT['PROVEEDOR']==Proveedor)&(DAT['PERIODO']==2021)].groupby(['MES','N_mes_ven']).mean()[['PRECIO_LISTA']].reset_index()
                    df_1=DAT[(DAT['SUCURSAL']==Sucursal)&(DAT['PROVEEDOR']==Proveedor)&(DAT['PERIODO']==2022)].groupby(['MES','N_mes_ven']).mean()[['PRECIO_LISTA']].reset_index()

                else:
                    df=DAT[(DAT['SUCURSAL']==Sucursal)&(DAT['EDITORIAL_']==Editorial)&(DAT['PROVEEDOR']==Proveedor)&(DAT['PERIODO']==2021)].groupby(['MES','N_mes_ven']).sum()[['TOTAL_VENTA']].reset_index()
                    df1=DAT[(DAT['SUCURSAL']==Sucursal)&(DAT['EDITORIAL_']==Editorial)&(DAT['PROVEEDOR']==Proveedor)&(DAT['PERIODO']==2022)].groupby(['MES','N_mes_ven']).sum()[['TOTAL_VENTA']].reset_index()
                    df_0=DAT[(DAT['SUCURSAL']==Sucursal)&(DAT['EDITORIAL_']==Editorial)&(DAT['PROVEEDOR']==Proveedor)&(DAT['PERIODO']==2021)].groupby(['MES','N_mes_ven']).mean()[['PRECIO_LISTA']].reset_index()
                    df_1=DAT[(DAT['SUCURSAL']==Sucursal)&(DAT['EDITORIAL_']==Editorial)&(DAT['PROVEEDOR']==Proveedor)&(DAT['PERIODO']==2022)].groupby(['MES','N_mes_ven']).mean()[['PRECIO_LISTA']].reset_index()




        fig = go.Figure(data=go.Bar(x=df['N_mes_ven'], y=df['TOTAL_VENTA'],name="Venta - Año Anterior",marker=dict(color="rgb(149,214,249)"),))
        fig.add_trace(go.Bar(x=df['N_mes_ven'], y=df1['TOTAL_VENTA'],name="Venta - Año Actual",marker=dict(color="rgb(245,183,152)")))

        fig.add_trace(go.Scatter(x=df_0['N_mes_ven'], y=df_0['PRECIO_LISTA'], yaxis="y2",name='Precio- Año Anterior',marker=dict(color="rgb(220,64,12)")))
        fig.add_trace(go.Scatter(x=df_1['N_mes_ven'], y=df_1['PRECIO_LISTA'], yaxis="y2",name='Precio- Año Actual',marker=dict(color="rgb(55,160,0)")))

        
        fig.update_layout(height=500,legend=dict(orientation="h"),title='Comparativo Precio / Venta',
                                  yaxis=dict(title=dict(text="Venta ($)"), side="left",),
                                  yaxis2=dict(title=dict(text="Precio ($)"),side="right",
                                      overlaying="y"),plot_bgcolor='rgba(0, 0, 0, 0)',
                                      paper_bgcolor='rgba(0, 0, 0, 0)')

        
        
       # df = px.data.gapminder().query("year == 2007")
        fig1 = px.sunburst(datos_general[datos_general['PROVEEDOR']==Proveedor], path=['PROVEEDOR','TEMA_'], values='TOTAL_VENTA',
                          color='TOTAL_VENTA', hover_data=['TOTAL_VENTA'],
                          color_continuous_scale='Blues',
                          color_continuous_midpoint=np.average(datos_general['TOTAL_VENTA'], 
                                                               weights=datos_general['TOTAL_VENTA']))

        if Proveedor =='TOTAL':

            fig1 = px.sunburst(datos_general, path=['PROVEEDOR','TEMA_'], values='TOTAL_VENTA',
                          color='TOTAL_VENTA', hover_data=['TOTAL_VENTA'],
                          color_continuous_scale='Blues',
                          color_continuous_midpoint=np.average(datos_general['TOTAL_VENTA'], 
                                                               weights=datos_general['TOTAL_VENTA']))
        
        fig1.update_layout(height=500)
        

        output0=dcc.Graph(figure=fig)
        output1=dcc.Graph(figure=fig1)

        output=dbc.Row([dbc.Col(output0), dbc.Col(output1,md=4)])
        
        return output

        


if __name__ == ('__main__'):
    app.run_server()