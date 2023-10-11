from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from pages.layouts import SHOW_BUTTON_STYLE, HIDE_BUTTON_STYLE, dropdown_select
from app import app

# Dynamnically insert this
staff_group_list = ['(All)', 'Ambulance Staff', 'Central functions','Doctors']

### Layout 1
refresh = html.Div([
    html.H1("Data refresh", className='display-1'),
    # create bootstrap grid 1Row x 2 cols
    dbc.Container([
        dbc.Row(
            [
                dbc.Col([
                    html.P('Data refresh buttons or something to go here....', className='lead'),
                ], className='col-3'),
                dbc.Col(
                    [
                        html.P('Data refresh buttons or something to go here....', className='lead'),
                    ],
                    className="pb-3",
                ), 
            ], className='col-9') 
        ],
    ), 
])
