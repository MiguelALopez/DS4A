from dash import html


def not_found_page():
    return html.Div([
        html.Img(src='assets/img/404.png')
    ], style={'textAlign': 'center'})
