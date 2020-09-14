# -*- coding: utf-8 -*-
"""
Created on Fri Sep 11 23:04:44 2020

@author: Krishna Kinger
"""
import dash_html_components as html
import dash_core_components as dcc
def tab1(countries):
    return html.Div([
            html.H2('Country', style={'width': '13%','display': 'inline-block'}),          
            dcc.Dropdown(
                id='country_list',
                options=countries,
                value=['US', 'Germany','India'], # which are pre-selected
                multi=True,
                style={'width': '60%','display': 'inline-block', 'height': '40px'}
            ),
            dcc.Markdown('''
            
            '''),
            html.H2('Visualization', style={'width': '13%','display': 'inline-block'}),
            dcc.Dropdown(
            id='selected_viz',
            options=[
                {'label': 'Timeline Confirmed ', 'value': 'confirmed'},
                {'label': 'Timeline Confirmed Filtered', 'value': 'confirmed_filtered'},
                {'label': 'Timeline Doubling Rate', 'value': 'confirmed_DR'},
                {'label': 'Timeline Doubling Rate Filtered', 'value': 'confirmed_filtered_DR'},
            ],
            value='confirmed',
            multi=False,
            style={'width': '40%','display': 'inline-block', 'height': '40px'}
            ),
            dcc.Graph(id='covid_stats_plot')
],style={'fontWeight': 'bold', 'font-size': '16px', 'font-family': 'cursive'})

def tab2(countries):
    return html.Div([
    
        dcc.Markdown('''        
        # Prediction by SIR Model
        '''),
        dcc.Dropdown(
            id = 'country_value',
            options=countries,
            value= 'India', # which are pre-selected
            multi=False),
        
        dcc.Graph(id = 'SIR_graph')
        ])
        
if __name__ == "__main__":
    tab1()
