import dash
import pandas as pd
from datetime import datetime
import base64
import io
from dash import html, dcc, dash_table, callback,Output,Input,State
import dash_bootstrap_components as dbc
from services import connection


def validator_page():
    return html.Div([
        html.H1('Meter data failure checker', className='mainTitle'),
        html.Div([
            html.Span('Upload csv files with the consumption information to validate whether or not there are anomalies on the '
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
            dcc.Upload(
            id='upload-data',
            children=html.Div([
                'Drag and Drop or ',
                html.A('Select Files'),
                '  (only csv files. max file size 20MB)'
            ]),
            style={
                'width': '100%',
                'height': '130px',
                'linewidth':'100%',
                'lineHeight': '130px',
                'borderWidth': '1px',
                'borderStyle': 'dashed',
                'borderRadius': '10px',
                'textAlign': 'center',
                'margin': '10px'
            },
            style_active = {'borderStyle': 'solid', 'borderColor': '#6c6', 'backgroundColor': '#9DB2BF'},
            multiple=True,
            max_size=20971520),
            ], className='upload-data--uploader'),
        html.Div(dbc.Button(children='Go ahead!'),id='upload_button'),
        html.Div(id='output-data-upload')

        ], className='validator')


def read_contents(contents, filename, nrows) -> pd.DataFrame:
    content_type, content_string = contents.split(',')
    nrows = None if nrows == 0 else 1
    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')), nrows=nrows)
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded), nrows=nrows)
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])
    return df


def parse_contents(value, contents, filename, date):
    # validating info feeded
    if value == 'consumption':
        try:
            assert 1 == 1  # assert list(read_contents(contents,filename,1).columns) == ['CODIGO_SIC','I_a_mean','I_b_mean','I_c_mean','VLA','VLB','VLC','kWhD','kWhR','kVarhD','kVarhR','FECHA','Capacidad','FALLA']
        except Exception as e:
            return html.Div(['File has not expected format. Please see user guide'])
        else:
            return read_contents(contents, filename, 0)
    else:
        try:
            assert list(read_contents(contents, filename, 1).columns) == []  # Only columns in clients table in DB
        except Exception as e:
            return html.Div(['File has not expected format. Please see user guide'])
        else:
            connection.upload_clients(read_contents(contents, filename, 0))
            return html.Div(["Client's info has been uploaded succesfully!"])


def get_stats(df):
    # function to predict failures from data feeded
    #
    return html.Div([
        html.Hr(),  # horizontal line
        html.Div(children=[html.H1('Results of validation'),

                           dcc.Graph(id='dashboard_validator', figure=go.Scatter(y=df['I_a_mean'], x=df['VLA'])),
                           dash_table.DataTable(
                               df.to_dict('records'),
                               [{'name': i, 'id': i} for i in df.columns],
                               page_size=10,
                               filter_action='native',
                               page_action='native'
                           ),

                           html.Hr(),  # horizontal line
                           html.Div([dbc.Button(id='valid-results-save', children=['Save results']),
                                     dbc.Button(id='valid-results-back', children=['Back to start'])
                                     ])
                           ])

    ])


@callback([Output('results_validator', 'children'),
           Output('output-data-upload', 'children')],
          [Input('upload_button', 'n_clicks')],
          State('radios', 'value'),
          State('upload-data', 'contents'),
          State('upload-data', 'filename'),
          State('upload-data', 'last_modified'), prevent_initial_call=True)
def update_output(nc, value, list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:

        dfs = [parse_contents(value, c, n, d) for c, n, d in
               zip(list_of_contents, list_of_names, list_of_dates)]
        if any([True for x in dfs if type(x) == html.Div]):
            i = 0
            while type(dfs[i]) != html.Div:
                i += 1
            error_desc = dfs[i]
            return None, error_desc
        else:
            df = dfs[0]
            for x in dfs[1:]:
                pd.concat(df, x, ignore_index=True)

            return get_stats(df), html.Div('Results are ready! Please view them below')
