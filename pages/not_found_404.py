import dash
from dash import html


dash.register_page(__name__)

def not_found_page():
    return html.Div([
        html.Img(src='assets/img/404.png')
    ], style={'textAlign': 'center'})


layout = not_found_page()
