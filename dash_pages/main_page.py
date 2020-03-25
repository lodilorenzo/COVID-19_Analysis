# -*- coding: utf-8 -*-
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output, State
import os

from app import app

layout = html.Div(id='main', children=[
    html.Div(id='main-div',
             children=[
                 html.H3(
                     children='Update local data',
                     id="import-dataset-new-title",
                     style={'width': '50%'}),
                 dbc.Button(
                     'Import dataset',
                     id='button',
                     className='btn btn-primary',
                     style={
                         'margin-top': '10px',
                         'width': '100%'
                     },
                     n_clicks=0
                 ),
                 html.Div(
                     id='button-output-div',
                     style={'display': 'none'}
                 )

             ], style={'padding': '50px',
                       'margin': 'auto',
                       'width': '70%'})

], style={'columnCount': 1})


def update_covid_data():
    os.chdir('COVID-19')
    result = os.system('git pull')
    os.chdir('..')
    return result


@app.callback(
    [Output('button-output-div', 'children'),
     Output('button-output-div', 'style')],
    [Input('button', 'n_clicks')]
)
def pressed_button(button_clicks):
    if button_clicks > 1:
        print("Bottone premuto")
        result = update_covid_data()
        if result > 0:
            # Error!
            return [dbc.Alert(
                "Error updating COVID-19 git module",
                id="alert-auto",
                is_open=True,
                duration=2000,
                color="danger"
            ), {'display': 'block'}]
        else:
            # OK!
            return [dbc.Alert(
                "COVID-19 data updated succesfully",
                id="alert-auto",
                is_open=True,
                duration=2000,
                color="success"
            ), {'display': 'block'}]
    else:
        return [None, None]
