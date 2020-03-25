import logging

import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
from dash_pages import main_page
from app import app

app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])


@app.callback(Output('page-content', 'children'),
              [Input('url', 'pathname')])
def display_page(pathname):
    if pathname is None:
        return
    else:
        return main_page.layout


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    app.run_server(debug=True, host='0.0.0.0')
