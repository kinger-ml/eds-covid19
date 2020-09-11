# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 22:21:55 2020

@author: Krishna Kinger
"""
import pandas as pd
import numpy as np

import dash
import dash_html_components as html
import dash_core_components as dcc

from dash.dependencies import Input, Output
from src.visualization.html_components import tab1, tab2
from src.data.get_data import get_johns_hopkins
from src.data.process_JH_data import store_relational_JH_data
from src.features.build_features import generate_features
from src.models.sir_model import SIR_modelling

df_input_large=pd.read_csv('data/processed/COVID_final_set.csv',sep=';')
countries=[ {'label': each,'value':each} for each in df_input_large['country'].unique()]
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
tab_style = {
    'padding': '2px',
    'fontWeight': 'bold',
    'font-size': '24px',
}
tab_selected_style = {
    'padding': '2px',
    'fontWeight': 'bold',
    'font-size': '26px',
    'font-family': 'cursive',
    'backgroundColor': 'blanchedalmond',
}
app.layout = html.Div([
    dcc.Tabs(id="tabs_main", value='tab_stats', children=[
        dcc.Tab(label='Covid-19 Statistics', value='tab_stats', style=tab_style, selected_style=tab_selected_style),
        dcc.Tab(label='Covid-19 Prediction', value='tab_prediction', style=tab_style, selected_style=tab_selected_style),
    ]),
    html.Div(id='tabs_content')
])

@app.callback(Output('tabs_content', 'children'),
              [Input('tabs_main', 'value')])
def render_content(tab):
    if tab == 'tab_stats':
        return tab1(countries)
    elif tab == 'tab_prediction':
        return tab2(countries)

@app.callback(
    Output('covid_stats_plot', 'figure'),
    [Input('country_list', 'value'),
    Input('selected_viz', 'value')])
    
def update_figure(country_list,viz):
    if 'DR' in viz:
        my_yaxis={'type':"log",
               'title':'Doubling Rate'
              }
    else:
        my_yaxis={'type':"log",
                  'title':'Confirmed infected people (source johns hopkins csse, log-scale)'
              }
    traces = []
    for each in country_list:

        df_plot=df_input_large[df_input_large['country']==each]

        if viz=='doubling_rate_filtered':
            df_plot=df_plot[['state','country','confirmed','confirmed_filtered','confirmed_DR','confirmed_filtered_DR','date']].groupby(['country','date']).agg(np.mean).reset_index()
        else:
            df_plot=df_plot[['state','country','confirmed','confirmed_filtered','confirmed_DR','confirmed_filtered_DR','date']].groupby(['country','date']).agg(np.sum).reset_index()


        traces.append(dict(x=df_plot.date,
                                y=df_plot[viz],
                                mode='markers+lines',
                                opacity=0.9,
                                name=each
                        )
                )

    return {
            'data': traces,
            'layout': dict (
                style={
                "margin-left": "auto",
                "margin-right": "auto",
                },
                width=1600,
                height=720,
                xaxis={'title':'Timeline',
                        'tickangle':-45,
                        'nticks':20,
                        'tickfont':dict(size=14,color="#7f7f7f"),
                      },
                yaxis=my_yaxis
        )
    }

@app.callback(
    Output('SIR_graph', 'figure'),
    [Input('country_value', 'value')])

def update_SIR_figure(country):
    traces = []
    #pop_0 = df_population[df_population.Location == country].PopTotal.iloc[0]
    #print('Population is:', pop_0)
    df_plot = df_input_large[df_input_large['country'] == country]
    df_plot = df_plot[['state', 'country', 'confirmed', 'date']].groupby(['country', 'date']).agg(np.sum).reset_index()
    df_plot.sort_values('date', ascending = True).head()
    df_plot = df_plot.confirmed[80:]
    
    t, fitted = SIR_modelling(df_plot)
    
    traces.append(dict (x = t,
                        y = df_plot,
                        mode = 'lines',
                        opacity = 0.9,
                        name = 'Original Data')
                  )
    traces.append(dict (x = t,
                        y = fitted,
                        mode = 'markers',
                        opacity = 0.9,
                        name = 'Prediction (SIR)')
                  )
    
    return {
            'data': traces,
            'layout': dict (
                width=1280,
                height=720,
                title = 'SIR model fitting',

                xaxis= {'title':'Days',
                       'tickangle':-45,
                        'nticks':20,
                        'tickfont':dict(size=14,color="#7f7f7f"),
                      },

                yaxis={'title': "Infected population"}
        )
    }
   
if __name__ == '__main__':
    """ 
    print('-----Retrieve John Hopkins Data--------')
    get_johns_hopkins()
    print('***** Data Retrieved **********')
    print('Store processed data')
    store_relational_JH_data()
    print('Processed data stored')
    print('Generate features')
    generate_features()
    print('Features stored')
    """
    print('Inside Main')
    app.run_server(debug=False)
