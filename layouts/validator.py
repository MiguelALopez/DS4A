from dash import html, dcc
import dash_bootstrap_components as dbc
from services import connection


def validator_page():
    users = connection.count_users()
    print(users)
    return html.Div([
        html.H1('Meter data failure checker', className='mainTitle'),
        html.H1(users),
        html.Div([
            html.Span('Upload csv files with the consumption information to validate if the is an anomaly on the '
                      'measurement'),
        ], className='text-center mt-5 mb-5'),
        html.Div([
            dbc.RadioItems(
                id="radios",
                labelCheckedClassName="active",
                inline=True,
                options=[
                    {"label": "Consumption", "value": 'consumption'},
                    {"label": "Clients", "value": 'clients'}
                ],
                value='consumption'
            ),
        ], className='d-flex justify-content-center p-4'),
        html.Div([
            dcc.Upload(dbc.Button("Primary", color="primary", className="me-1"))

        ], className='d-flex justify-content-center m-4')

    ], className='validator')
