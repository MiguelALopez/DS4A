import dash
import dash_bootstrap_components as dbc
from services import connection
from pages import validator, statistics, predictions, user_guide, not_found_404
from dash import Dash, html, callback, Output, Input, dcc


app = Dash(
    external_stylesheets=[dbc.themes.LITERA],
    use_pages=True
)
connection.start()


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
    dcc.Location(id='url', refresh=False),
    navbar,
    html.Div([dash.page_container], id='page-content', className='page-content container')
])

routes = {
    '/': validator.validator_page(),
    '/validator': validator.validator_page(),
    '/prediction': predictions.predictions_page(),
    '/statistics': statistics.statistics_page(),
    '/user-guide': user_guide.user_guide_page(),
    '/404': not_found_404.not_found_page()
}


@callback(Output('page-content', 'children'),
          [Input('url', 'pathname')])
def display_page(pathname):
    return routes.get(pathname, not_found_404.not_found_page())


if __name__ == '__main__':
    app.run_server(debug=True)
