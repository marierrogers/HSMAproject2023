from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from pages.layouts import SHOW_BUTTON_STYLE, HIDE_BUTTON_STYLE, tab_turnover_content, tab_sickness_content, dropdown_select
from app import app


### Layout 1
home = html.Div([
    html.H1("NHS Staff turnover and sickess", className='display-1'),
    # create bootstrap grid 1Row x 2 cols
    dbc.Container([
        dbc.Row(
            [
                dbc.Col([
                    dropdown_select('staff')
                ], className='col-3'),
                dbc.Col([
                    html.Div(
                        [
                            html.P('Insert some explanatory text here....', className='lead'),
                            dcc.Tabs(id="tabs-home", value='tab-turnover', children=[
                                dcc.Tab(label='Staff Turnover', value='tab-turnover'),
                                dcc.Tab(label='Staff Sickness', value='tab-sickness'),
                            ]),
                            html.Div(id='tabs-home-content')
                        ],
                        className="pb-3",
                    ), 
                ], className='col-9')
            ],
        ), 

    ]),
])


@app.callback(
    Output('tabs-home-content', 'children'),
    Input('tabs-home', 'value')
)
def render_tab(tab):
    if tab == 'tab-turnover':
        return tab_turnover_content()
    elif tab == 'tab-sickness':
        return tab_sickness_content()