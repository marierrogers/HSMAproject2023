from dash import dcc, html, Input, Output
import dash_bootstrap_components as dbc
from pages.layouts import SHOW_BUTTON_STYLE, HIDE_BUTTON_STYLE, dropdown_select
from app import app
import pandas as pd
import plotly.express as px
from utils import flatten

# Load in and prepare data
url_r2 = 'data/sickness_benchmarking.csv'
df_r2 = pd.read_csv(url_r2, parse_dates=['DATE'])

trust_types_todrop = ['Clinical Commissioning Group','Integrated Care Board']
df_r2 = df_r2[~df_r2['CLUSTER_GROUP'].isin(trust_types_todrop)]
#df_r2 = df_r2.drop(['ORG_NAME',
 #                   'NHSE_REGION_CODE','CLUSTER_GROUP','file_date'],axis=1)
df_r2.rename(columns=str.lower,inplace=True)
merge_cols = ['month_year', 'org_code','region_name','staff_group']
df_r2['sickness_absence'] = round(df_r2['fte_days_lost']/df_r2['fte_days_available']*100,2)
df_r2 = df_r2.reset_index(drop=True)

df_r2['date'] = pd.to_datetime(df_r2['date'])

# Sort the DataFrame by organisation, staff_group, and month
df_r2.sort_values(by=['org_code', 'staff_group', 'date'], inplace=True)

# Calculate the rolling sums for days lost and days available
df_r2['rolling_days_lost'] = df_r2.groupby(['org_code', 
                        'staff_group'])['fte_days_lost'].rolling(window=12, min_periods=1).sum().reset_index(level=[0, 1], drop=True)

df_r2['rolling_days_available'] = df_r2.groupby(['org_code', 
                        'staff_group'])['fte_days_available'].rolling(window=12, min_periods=1).sum().reset_index(level=[0, 1], drop=True)

# Calculate the rolling sickness absence rate
df_r2['annual_sickness_absence'] = df_r2['rolling_days_lost'] / df_r2['rolling_days_available']



# Group lists
staff_group_list = sorted(df_r2['staff_group'].unique())
benchmark_group_list = sorted(df_r2['benchmark_group'].unique())
benchmark_group_list.insert(0, 'All benchmark groups')

org_code_list= sorted(df_r2['org_code'].unique())
org_code_list.insert(0,'All organisations')

org_name_list= sorted(df_r2['org_name'].unique())
org_name_list.insert(0,'All organisations')
#region_code_list = sorted(df_r2['region_code'].unique())
nhse_region_name_list = sorted(df_r2['nhse_region_name'].unique())
nhse_region_name_list.insert(0, 'All regions')

clust_group_list = sorted(df_r2['cluster_group'].unique())
clust_group_list.insert(0, 'All group clusters')

combo_region_dict = df_r2[['nhse_region_name', 'org_name']].drop_duplicates().set_index('nhse_region_name').stack().groupby(level=0).apply(list).to_dict()
combo_region_list = list(combo_region_dict.keys())
combo_region_list.insert(0, 'All regions')


### Layout 1
sickness = html.Div([
    html.H1("NHS Staff Sickness Rates", className='display-1'),
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
                    html.Div([
                        dropdown_select(nhse_region_name_list, 'Region', 'region_dropdown'),
                    ], className="pt-4"),
                    html.Div([
                        dropdown_select(org_name_list, 'Organisation name', 'org_name_dropdown_sickness'),
                    ], className="pt-4 small"),
                ], className='col-4'),
                dbc.Col(
                    [
                        html.P('Insert some explanatory text here....', id='info-sickness', className='lead'),
                        html.Div(id='fig-sickness'),
                    ],
                    className="pb-3 col-8",
                ), 
            ], className='col-12') 
        ],
    ), 
])


@app.callback(
    Output('org_name_dropdown_sickness', 'options'),
    Input('region_dropdown', 'value'))
def set_organisation_options(selected_region):
    print('Updating dropdowns called')
    return_list = combo_region_dict[selected_region] if selected_region != 'All regions' else list(flatten(combo_region_dict.values()))
    return_list_sorted = sorted(return_list)
    return_list_sorted.insert(0, 'All organisations')
    return return_list_sorted


@app.callback(
    Output('fig-sickness', 'children'), 
    Output('info-sickness', 'children'),
    Input('staff_group_dropdown', 'value'),
    Input('region_dropdown', 'value'),
    Input('org_name_dropdown_sickness', 'value')
)
def fig_call_vol(staff_group, region, org):

    app.logger.info(f"fig_call_vol function triggered with: {staff_group}")
    if type(staff_group) != list:
        sickness_staff_group = [staff_group]
    else:
        sickness_staff_group = staff_group

    if type(staff_group) != list:
        turnover_staff_group = [staff_group]
    else:
        turnover_staff_group = staff_group

    turnover_region_group = sorted(df_r2['nhse_region_name'].unique()) if region == 'All regions' else [region]

    if org != 'All organisations' and region == 'All regions': 
        turnover_org_group = [org]
    elif org == 'All organisations' and region == 'All regions':
        turnover_org_group = list(flatten(combo_region_dict.values()))
    else:
        if org in str(combo_region_dict[region]):
            turnover_org_group = [org]
        else:
            org = 'All organisations'
            turnover_org_group = combo_region_dict[region]

    info_caption = f"Line chart showing Staff turnover for {', '.join(turnover_staff_group)}, {region}, {org}"

    app.logger.info(f"sickness_staff_group values is: {sickness_staff_group}")

    app.logger.info('some staff')
   # df = df_r2[df_r2['staff_group'].isin(sickness_staff_group)]
    df = df_r2[(df_r2['staff_group'].isin(turnover_staff_group)) & (df_r2['org_name'].isin(turnover_org_group))]

    fig_df = df.groupby(['date', 'staff_group'])['sickness_absence'].mean().reset_index()

    fig = px.line(fig_df, x = 'date', y = 'sickness_absence', color='staff_group', markers=True,
                  labels={
                     "date": "Date",
                     "sickness_absence": "Absence Rate (%)",
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