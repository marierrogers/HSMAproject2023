from dash import Dash, dcc, html, Input, Output
import dash_bootstrap_components as dbc
from app import app, server
from pages.layouts import nav_bar, CONTENT_STYLE, footer, dropdown_select
from pages.home import home
from pages.turnover import turnover
from pages.sickness import sickness
from pages.organisation import organisation
from pages.regression import regression
from pages.refresh import refresh
import callbacks
import logging
from sys import version_info

import warnings
warnings.filterwarnings("ignore", category=FutureWarning)

app.logger.info('Off we go!')
# This is not supported in python 3.8
if version_info >= (3,9):
    logging.basicConfig(format='%(asctime)s %(message)s', filename='model.log', encoding='utf-8', level=logging.DEBUG)

logging.debug('Off we go!')

# Define basic structure of app:
# A horizontal navigation bar on the left side with page content on the right.
app.layout = html.Div([
    dcc.Location(id='url', refresh=False), #this locates this structure to the url
    dcc.Store(id='staff_group_store', storage_type='local'),
    html.Div([
        nav_bar(),
        dbc.Container([
            dbc.Row([
                html.Div(id='page-content',style=CONTENT_STYLE), #we'll use a callback to change the layout of this section 
            ]),
        ], className="w-100 container-fluid"),
        html.Div([
            footer()
        ], className='w-100 container-fluid bg-secondary mt-5', style={"zIndex":'1', 'position':'relative', 'minHeight':'200px'})
    ])
])

# This callback changes the layout of the page based on the URL
# For each layout read the current URL page "http://127.0.0.1:8080/pagename" and return the layout
@app.callback(Output('page-content', 'children'), #this changes the content
              [Input('url', 'pathname')]) #this listens for the url in use
def display_page(pathname):
    if pathname == '/':
        return home
    elif pathname == '/home':
        return home
    elif pathname == '/turnover':
        return turnover
    elif pathname == '/sickness':
        return sickness
    elif pathname == '/organisation':
        return organisation
    elif pathname == '/regression':
        return regression
    elif pathname == '/data':
        return refresh
    else:
        return '404' #If page not found return 404


if __name__ == "__main__":
    app.run(debug=True)
