import dash
from datetime import date
from dash import html, dcc
import dash_bootstrap_components as dbc


def predictions_page():
    return html.Div([
        html.H1('Predictions', className='mainTitle'),
        html.Div([
            html.Span('Generate predictions based on historical data of voltage failures'),
        ], className='text-center mt-5 mb-5'),
        dbc.Row([
            dbc.Col([
                dbc.Label('Start Date', className='w-100 input-label'),
                dcc.DatePickerSingle(
                    id='my-date-picker-single',
                    min_date_allowed=date(1995, 8, 5),
                    max_date_allowed=date(2017, 9, 19),
                    initial_visible_month=date(2017, 8, 5),
                    display_format='DD/MM/YYYY',
                    className='w-100'
                )]
            ),
            dbc.Col([
                dbc.Label('End Date', className='w-100 input-label'),
                dcc.DatePickerSingle(
                    id='my-date-picker-single',
                    min_date_allowed=date(1995, 8, 5),
                    max_date_allowed=date(2017, 9, 19),
                    initial_visible_month=date(2017, 8, 5),
                    display_format='DD/MM/YYYY',
                    className='w-100'
                )
            ]),
            dbc.Col([
                dbc.Label('Region', className='w-100 input-label'),
                dbc.Input(id="input", placeholder="Select value", type="text")
            ]),
            dbc.Col([
                dbc.Label('Business', className='w-100 input-label'),
                dbc.Input(id="input", placeholder="Select Value", type="text")
            ])
        ], className='container')
    ])
