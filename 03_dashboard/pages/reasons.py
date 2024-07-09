from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from pages.layouts import SHOW_BUTTON_STYLE, HIDE_BUTTON_STYLE, dropdown_select, date_select
from app import app
import pandas as pd
import plotly.express as px
from datetime import date, datetime
import re

# Load in and prepare data
url_r2 = 'data/sickness_reasons.csv'
df_r2 = pd.read_csv(url_r2, parse_dates=['DATE'])

df_r2.rename(columns=str.lower,inplace=True)
df_r2['date'] = pd.to_datetime(df_r2['date'])

# Group lists
staff_group_list = sorted(df_r2['staff_group'].unique())
sickness_reason_list = sorted(df_r2['reason'].unique())
short_sickness_list = [x for x in sickness_reason_list if re.search(r'^s[0-9]+', x)]
short_sickness_list.insert(0, 'all reasons')

### Layout 1
reasons = html.Div([
    html.H1("NHS Staff Sickness Reasons", className='display-1'),
    # create bootstrap grid 1Row x 2 cols
    dbc.Container([
        dbc.Row(
            [
                dbc.Col([
                    html.Div([
                        dropdown_select(staff_group_list, 'Staff groups', 'staff_group_dropdown', True),
                    ]),
                    html.Div([
                        date_select(df_r2, 'Date range', 'reason_date_range','date'),
                    ], className='pt-4'),
                    html.Div([
                        html.P("For a longitudinal view of conditions by staff group, scroll down..."),
                    ], className='pt-4 lead'),
                ], className='col-4'),
                dbc.Col(
                    [
                        html.P('Insert some explanatory text here....', className='lead',id='info-reasons',),
                        html.Div(id='fig-reasons'),
                    ],
                    className="pb-3 col-8"
                ), 
            ], className='col-12', style={"height":"900px"}),
        dbc.Row(
            [
                dbc.Col([
                    html.Div([
                        dropdown_select(short_sickness_list, 'Sickness Reason', 'reason_dropdown', True),
                    ]),
                    html.Div([
                        dropdown_select(staff_group_list, 'Staff Group', 'reason_staff_group'),
                    ], className="pt-4"),
                    html.Div([
                        date_select(df_r2, 'Date range', 'reason_date_range2','date'),
                    ], className='pt-4'),
                ], className='col-4'),
                dbc.Col(
                    [
                        html.P('Insert some explanatory text here....', className='lead',id='info-sickness-reason',),
                        html.Div(id='fig-sickness-reason'),
                    ],
                    className="pb-3 col-8"
                ), 
            ], className='col-12', style={"height":"500px"}) 
        ],
    ), 
])



@app.callback(
    Output('fig-reasons', 'children'), 
    Output('info-reasons', 'children'),
    Input('staff_group_dropdown', 'value'),
    Input('reason_date_range', 'start_date'),
    Input('reason_date_range', 'end_date')
)
def fig_reasons_sick(staff_group, start_date, end_date):

    date_format = "%Y-%m-%dT%H:%M:%S"
    date_only_format = "%Y-%m-%d"
    min_date = df_r2['date'].min()
    max_date = df_r2['date'].max()

    if start_date is None:
        sd = min_date
    elif len(start_date) == 10:
        sd = datetime.strptime(start_date, date_only_format)
    else:
        sd = datetime.strptime(start_date, date_format)

    if end_date is None:
        ed = max_date
    elif len(end_date) == 10:
        ed = datetime.strptime(end_date, date_only_format)
    else:
        ed = datetime.strptime(end_date, date_format)


    if type(staff_group) != list:
        sickness_staff_group = [staff_group]
    else:
        sickness_staff_group = staff_group

    if staff_group == 'All staff groups': 
        reasons_staff_group = [staff_group]
    else:
        reasons_staff_group = staff_group

    info_caption = f"Bar chart showing staff sickness reasons for {', '.join(reasons_staff_group)} between {sd.strftime('%B %Y')} and {ed.strftime('%B %Y')}"

    df = df_r2[(df_r2['date'] >= sd) & (df_r2['date'] <= ed)]
    df1 = df[df['reason'] != 'all reasons'].groupby(['staff_group', 'reason']).agg({'fte_days_lost' : 'sum'}).reset_index()
    df1['total_days_lost'] = df1.groupby(['staff_group'])['fte_days_lost'].transform('sum')
    df1['percentage_days_lost'] = round(df1['fte_days_lost'] / df1['total_days_lost']*100, 1)

    # Sort the DataFrame by organisation, staff_group, and month
    df1.sort_values(by=['reason', 'staff_group'], inplace=True)


    df2 = df1[df1['staff_group'].isin(sickness_staff_group)].sort_values(by=['staff_group', 'percentage_days_lost'])
    df3 = df2[df2['percentage_days_lost'] > 0]

    #app.logger.info(df1.head().to_string())

    fig = px.bar(df3, x = 'reason', y = 'percentage_days_lost', text = 'percentage_days_lost', color='staff_group',
                 barmode='group',
                  labels={
                     "reason": "Reason",
                     "percentage_days_lost": "Percentage of days lost",
                     "staff_group": "Staff groups"
                 },)
    
    fig.update_traces(texttemplate='%{text:.2s}', textposition='outside')
    fig.update_layout(uniformtext_minsize=8, uniformtext_mode='hide')

    fig.update_layout(legend=dict(
        orientation="h",
        entrywidth=500,
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    fig['layout'].update(height=800)

    #fig.update_xaxes(showticklabels=False)

    return [dcc.Graph(figure=fig), info_caption]

@app.callback(
    Output('fig-sickness-reason', 'children'), 
    Output('info-sickness-reason', 'children'),
    Input('reason_dropdown', 'value'),
    Input('reason_staff_group', 'value'),
    Input('reason_date_range2', 'start_date'),
    Input('reason_date_range2', 'end_date')
)
def fig_sickness_reasons(reason_dropdown, staff_group, start_date, end_date):

    app.logger.info(f"fig_sickness_reasons function triggered with: {reason_dropdown}")

    date_format = "%Y-%m-%dT%H:%M:%S"
    date_only_format = "%Y-%m-%d"
    min_date = df_r2['date'].min()
    max_date = df_r2['date'].max()

    if start_date is None:
        sd = min_date
    elif len(start_date) == 10:
        sd = datetime.strptime(start_date, date_only_format)
    else:
        sd = datetime.strptime(start_date, date_format)

    if end_date is None:
        ed = max_date
    elif len(end_date) == 10:
        ed = datetime.strptime(end_date, date_only_format)
    else:
        ed = datetime.strptime(end_date, date_format)

    info_caption = f"Line chart showing Sickness Reasons for {staff_group} between {sd.strftime('%B %Y')} and {ed.strftime('%B %Y')}"

    if type(reason_dropdown) != list:
        reason_dropdown_group = [reason_dropdown]
    else:
        reason_dropdown_group = reason_dropdown

    df = df_r2[(df_r2['date'] >= sd) & (df_r2['date'] <= ed)]
    df1 = df[(df['staff_group'].isin([staff_group])) & (df['reason'].isin(reason_dropdown_group))]
    df1['total_days_lost'] = df1.groupby(['date','reason'])['fte_days_lost'].transform('sum')

    fig_df = df1.groupby(['date', 'reason'])['total_days_lost'].sum().reset_index()

    fig = px.line(fig_df, x = 'date', y = 'total_days_lost', color='reason', markers=True,
                  labels={
                     "date": "Date",
                     "total_days_lost": "Total days lost",
                     "staff_group": "Staff groups"
                 },)
    
    fig.update_layout(legend=dict(
        orientation="h",
        yanchor="bottom",
        y=1.02,
        xanchor="right",
        x=1
    ))

    return [dcc.Graph(figure=fig), info_caption]