from dash import html, Input, Output, State, dcc, dash_table
from app import app
import plotly.express as px
import logging

# Placeholder bar chart

@app.callback(
    Output('test-bar', 'figure'), 
    Input('staff_group_dropdown', 'value')
)
def fig_call_vol(staff_group):
    df = px.data.gapminder().query("country == 'Canada'")
    app.logger.info(f"Callback triggered with staff group {staff_group}")
    logging.debug(df.head())
    fig = px.bar(df, x='year', y='pop',
                hover_data=['lifeExp', 'gdpPercap'], color='lifeExp',
                labels={'pop':'population of Canada'}, height=400)
    
    return fig


@app.callback(
    Output('test-bar1', 'figure'), 
    Input('staff_group_dropdown', 'value')
)
def fig_call_vol(staff_group):
    df = px.data.gapminder().query("country == 'Canada'")
    app.logger.info(f"Callback triggered with staff group {staff_group}")
    logging.debug(df.head())
    fig = px.bar(df, x='year', y='pop',
                hover_data=['lifeExp', 'gdpPercap'], color='lifeExp',
                labels={'pop':'population of Canada'}, height=400)
    
    return fig


@app.callback(
    Output('test-bar2', 'figure'), 
    Input('staff_group_dropdown', 'value')
)
def fig_call_vol(staff_group):
    df = px.data.gapminder().query("country == 'Canada'")
    app.logger.info(f"Callback triggered with staff group {staff_group}")
    logging.debug(df.head())
    fig = px.bar(df, x='year', y='pop',
                hover_data=['lifeExp', 'gdpPercap'], color='lifeExp',
                labels={'pop':'population of Canada'}, height=400)
    
    return fig


@app.callback(
    Output('test-bar3', 'figure'), 
    Input('staff_group_dropdown', 'value')
)
def fig_call_vol(staff_group):
    df = px.data.gapminder().query("country == 'Canada'")
    app.logger.info(f"Callback triggered with staff group {staff_group}")
    logging.debug(df.head())
    fig = px.bar(df, x='year', y='pop',
                hover_data=['lifeExp', 'gdpPercap'], color='lifeExp',
                labels={'pop':'population of Canada'}, height=400)
    
    return fig