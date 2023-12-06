from dash import Dash
import dash_bootstrap_components as dbc
from sys import version_info

app = Dash(
    __name__,
    external_stylesheets=[dbc.icons.FONT_AWESOME],
    )

app.config.suppress_callback_exceptions = True
server = app.server