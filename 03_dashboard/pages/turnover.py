from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from pages.layouts import SHOW_BUTTON_STYLE, HIDE_BUTTON_STYLE, dropdown_select
from app import app
import pandas as pd
import plotly.express as px

# Load in and prepare data
url_t = 'data/annual_turnover.csv'
df_t = pd.read_csv(url_t, parse_dates=['DATE'])

# Dynamnically insert this
staff_group_list = ['(All)', 'Ambulance Staff', 'Central functions','Doctors']

### Layout 1
turnover = html.Div([
    html.H1("NHS Staff turnover", className='display-1'),
    # create bootstrap grid 1Row x 2 cols
    dbc.Container([
        dbc.Row(
            [
                dbc.Col([
                    html.Div([
                        dropdown_select(staff_group_list, 'Staff groups', 'staff_group_dropdown', True),
                    ]),
                    # html.Div([
                    #     dropdown_select(benchmark_group_list, 'Benchmarking groups', 'benchmark_group_dropdown'),
                    # ], className="pt-4"),
                    # html.Div([
                    #     dropdown_select(nhse_region_name_list, 'Region', 'region_dropdown'),
                    # ], className="pt-4"),
                ], className='col-4'),
                dbc.Col(
                    [
                    html.P('Insert some explanatory text here....', className='lead'),
                    html.Div([
                        dcc.Graph(id='test-bar')
                    ]),
                    ],
                    className="pb-3",
                    ), 
                ], className='col-9') 
            ],
        ), 
    ]),
