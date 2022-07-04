import dash
from dash import html

dash.register_page(__name__)

def user_guide_page():
    return html.Div([
        html.H1('User guide', style={'textAlign': 'center'}),
    ])


layout = user_guide_page()
