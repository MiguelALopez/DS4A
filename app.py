import dash
from dash import Dash, html
import dash_bootstrap_components as dbc
from services import connection

connection.start()
app = Dash(
    external_stylesheets=[dbc.themes.LITERA],
    use_pages=True
)


app.title = 'Celsia Data Validator'
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Validator", href="/", active='exact')),
        dbc.NavItem(dbc.NavLink("Prediction", href="/predictions", active='exact')),
        dbc.NavItem(dbc.NavLink("Statistics", href="/statistics", active='exact')),
        dbc.NavItem(dbc.NavLink("User guide", href="/user-guide", active='exact')),
    ],
    brand="Celsia",
    brand_href="#",
    color="light",
    dark=False,
)
app.layout = html.Div([
    navbar,
    html.Div([dash.page_container], id='page-content', className='page-content container')
])


if __name__ == '__main__':
    app.run_server(debug=True)
