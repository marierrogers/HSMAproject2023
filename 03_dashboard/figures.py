import plotly.express as px

def placeholder_bar():
    df = px.data.gapminder().query("country == 'Canada'")
    print(df.head())
    fig = px.bar(df, x='year', y='pop',
                hover_data=['lifeExp', 'gdpPercap'], color='lifeExp',
                labels={'pop':'population of Canada'}, height=400)
    return fig