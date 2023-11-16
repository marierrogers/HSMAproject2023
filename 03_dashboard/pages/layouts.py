from turtle import width
from dash import html, dcc
import dash_bootstrap_components as dbc

# Mostly stolen from here: https://towardsdatascience.com/callbacks-layouts-bootstrap-how-to-create-dashboards-in-plotly-dash-1d233ff63e30


CONTENT_STYLE = {
    #"top":0,
   # "marginTop":'2rem',
    "marginLeft": "1rem",
    "marginRight": "1rem",
}

SHOW_BUTTON_STYLE = {
    "display": "block"
}

HIDE_BUTTON_STYLE = {
    "display": "none"
}

DROPDOWN_STYLE = {
    "marginBottom":"20px"
}



#####################################
# Create Auxiliary Components Here
#####################################

# Dynamnically insert this

def dropdown_select(group_list, title='Staff group', select_id="staff_group_dropdown", multi_sel=False):

    staff_sel = html.Div(
        [
            html.P(title, id=f"{select_id}_label", className='lead'),
            dcc.Dropdown(
                options = group_list,
                value = group_list[0] if len(group_list) > 0 else "",
                id=select_id,
                multi=multi_sel
            ),
        ],
        className='pt-2, w-100'
    )
    return staff_sel

def nav_bar():
    """
    Creates Navigation bar
    """
    navbar = html.Div(
        [
            dbc.Navbar(
                dbc.Container([
                    dbc.Row(
                        [
                            dbc.Col(html.Img(src="assets/nhs-logo.jpg", height="30px")),
                            dbc.Col(dbc.NavbarBrand("NHS Staff Turnover and Sickness", className="ms-2")),
                        ],
                        align="center",
                        className="g-0",
                    ),
                    #dbc.NavLink("Home", href="/home", active="exact"),
                    dbc.NavLink("Staff turnover", href="/turnover", external_link=True, active="exact"),
                    dbc.NavLink("Staff sickness rates", href="/sickness", external_link=True, active="exact"),
                    dbc.NavLink("Staff sickness reasons", href="/reasons", external_link=True, active="exact"),
                    #dbc.NavLink("Organisations", href="/organisation", external_link=True, active="exact"),
                    #dbc.NavLink("Impact factors", href="/regression", external_link=True, active="exact"),
                    dbc.NavLink("Data refresh", href="/data", external_link=True, active="exact"),
                ]),
            ),
        ],
    )  
    return navbar

def footer():
    footer = dbc.Container(
        [   
            dbc.Row([
                dbc.Col([
                    html.P(' ')
                ]),
                dbc.Col([
                    html.P(' ')
                ]),
                dbc.Col([
                    dbc.Row([
                        dbc.Col([html.A(href='https://github.com/marierrogers/HSMAproject2023', className='fa-brands fa-github display-3 text-light', style={'textDecoration':'none'})]),
                    ]),
                    dbc.Row([
                        html.Div([
                            html.Span('Icons made by '),
                            html.A('Freepik', href="https://www.flaticon.com/authors/freepik", className='text-light'),
                            html.Span(' from '),
                            html.A('www.flaticon.com', href="https://www.flaticon.com/", className='text-light')
                        ], className="small pt-5 text-light")

                    ])

                ])
            ], className='pt-4')
        ], className='pt-4',
    )

    return footer


def tab_turnover_content():
    return html.Div([
        html.H4('Staff turnover', className='display-4'),
        dbc.Row([
            html.H4('National turnover by (staff group) over time', className='display-6'),
            html.Div([
                dcc.Graph(id='test-bar')
            ]),
            html.Hr(),
        ]),
        dbc.Row([
            html.H4('National turnover rate by (staff group) year on year', className='display-6'),
            html.Div([
                dcc.Graph(id='test-bar1')
            ]),
            html.Hr(),
        ])
    ])


def tab_sickness_content():
    return html.Div([
        html.H4('Staff sickness', className='display-4'),
        dbc.Row([
            html.H4('National sickness by (staff group) over time', className='display-6'),
            html.Div([
               dcc.Graph(id='test-bar2')
            ]),
            html.Hr(),
        ]),
        dbc.Row([
            html.H4('National sickness absence by (staff group) year on year', className='display-6'),
            html.Div([
                dcc.Graph(id='test-bar3')
            ]),
            html.Hr(),
        ])
    ])