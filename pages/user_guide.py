import dash
from dash import html


def user_guide_page():
    return html.Div([
        html.H1('User guide', style={'textAlign': 'center'}),
    ])
