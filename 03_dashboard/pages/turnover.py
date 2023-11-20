from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from pages.layouts import SHOW_BUTTON_STYLE, HIDE_BUTTON_STYLE, dropdown_select
from app import app
import pandas as pd
import plotly.express as px

# Load in and prepare data
url_t = 'data/annual_turnover.csv'
df_t = pd.read_csv(url_t, parse_dates=['DATE'])
df_t.rename(columns=str.lower,inplace=True)
# No turnover data before April 2018
df_t1 = df_t[df_t['date'] > '2018-03-01']
# Group lists
staff_group_list = sorted(df_t1['staff_group'].unique())
benchmark_group_list = sorted(df_t1['benchmark_group'].unique())
benchmark_group_list.insert(0, 'All benchmark groups')

org_name_list= sorted(df_t1['org_name'].unique())
org_name_list.insert(0,'All organisations')
#region_code_list = sorted(df_r2['region_code'].unique())
nhse_region_name_list = sorted(df_t1['nhse_region_name'].unique())
nhse_region_name_list.insert(0, 'All regions')

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
                    html.Div([
                        dropdown_select(benchmark_group_list, 'Benchmarking groups', 'benchmark_group_dropdown'),
                    ], className="pt-4"),
                    html.Div([
                        dropdown_select(nhse_region_name_list, 'Region', 'region_dropdown'),
                    ], className="pt-4"),
                    html.Div([
                        dropdown_select(org_name_list, 'Organisation name', 'org_name_dropdown'),
                    ], className="pt-4 small"),
                ], className='col-4'),
                dbc.Col(
                    [
                        html.P('Insert some explanatory text here....', className='lead'),
                        html.Div(id='fig-turnover'),
                    ],
                    className="pb-3 col-8",
                ), 
                ], className='col-12') 
            ],
        ), 
    ]),


@app.callback(
    Output('fig-turnover', 'children'), 
    Input('staff_group_dropdown', 'value')
)
def fig_turnover(staff_group):

    app.logger.info(f"fig_turnover function triggered with: {staff_group}")
    if type(staff_group) != list:
        turnover_staff_group = [staff_group]
    else:
        turnover_staff_group = staff_group

    app.logger.info(f"sickness_staff_group values is: {turnover_staff_group}")

    app.logger.info('some staff')
    df = df_t1[df_t1['staff_group'].isin(turnover_staff_group)]

    fig_df = df.groupby(['date', 'staff_group']).agg({'leave_fte':'sum',
                                                    'denom_fte_mean':'sum'}).reset_index()
    fig_df['fte_rate'] = fig_df['leave_fte']/fig_df['denom_fte_mean']


    fig = px.line(fig_df, x = 'date', y = 'fte_rate', color='staff_group', markers=True,
                  labels={
                     "date": "Date",
                     "fte_rate": "Turnover Rate (%)",
                     "staff_group": "Staff groups"
                 },)
    
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    return dcc.Graph(figure=fig)