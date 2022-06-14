from dash import Dash, html, callback, Output, Input, dcc
import dash_bootstrap_components as dbc
from layouts import validator, statistics, predicitons, user_guide, not_found

app = Dash(
    external_stylesheets=[dbc.themes.BOOTSTRAP]
)
app.title = 'Celsia Data Validator'
navbar = dbc.NavbarSimple(
    children=[
        dbc.NavItem(dbc.NavLink("Validator", href="/validator")),
        dbc.NavItem(dbc.NavLink("Prediction", href="/prediction")),
        dbc.NavItem(dbc.NavLink("Statistics", href="/statistics")),
        dbc.NavItem(dbc.NavLink("User guide", href="/user-guide")),
    ],
    brand="Celsia",
    brand_href="#",
    color="light",
    dark=False,
)
app.layout = html.Div([
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div(id='page-content')

])

routes = {
    '/validator': validator.validator_page(),
    '/prediction': predicitons.predictions_page(),
    '/statistics': statistics.statistics_page(),
    '/user-guide': user_guide.user_guide_page(),
    '/404': not_found.not_found_page()
}


@callback(Output('page-content', 'children'),
          [Input('url', 'pathname')])
def display_page(pathname):
    return routes.get(pathname, not_found.not_found_page())


if __name__ == '__main__':
    app.run_server(debug=True)
