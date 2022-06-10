from dash import Dash, html
import dash_bootstrap_components as dbc

# app = Dash(__name__)
app = Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.title = 'Celsia Data Validator'
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Validator", href="#")),
        dbc.NavItem(dbc.NavLink("Prediction", href="#")),
        dbc.NavItem(dbc.NavLink("Statistics", href="#")),
        dbc.NavItem(dbc.NavLink("User guide", href="#")),
    ],
    brand="Celsia",
    brand_href="#",
    color="light",
    dark=False,
)
app.layout = html.Div([
    navbar,
    html.H1('Voltage Failure checker', style={'textAlign': 'center'}),

])

if __name__ == '__main__':
    app.run_server(debug=True)
