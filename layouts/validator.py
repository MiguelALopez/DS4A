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
    
def parse_contents(contents, filename, date):
    content_type, content_string = contents.split(',')

    decoded = base64.b64decode(content_string)
    try:
        if 'csv' in filename:
            # Assume that the user uploaded a CSV file
            df = pd.read_csv(
                io.StringIO(decoded.decode('utf-8')))
        elif 'xls' in filename:
            # Assume that the user uploaded an excel file
            df = pd.read_excel(io.BytesIO(decoded))
    except Exception as e:
        print(e)
        return html.Div([
            'There was an error processing this file.'
        ])

    return html.Div([
        html.H5(filename),
        html.H6(datetime.fromtimestamp(date)),

        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i} for i in df.columns],
            page_size=10,
            filter_action='native',
            page_action='native'
        ),

        html.Hr(),  # horizontal line

        # For debugging, display the raw contents provided by the web browser
        html.Div('Raw Content'),
        html.Pre(contents[0:200] + '...', style={
            'whiteSpace': 'pre-wrap',
            'wordBreak': 'break-all'
        })
    ])

@callback(Output('output-data-upload', 'children'),
              Input('upload_button','n_clicks'),
              State('upload-data', 'contents'),
              State('upload-data', 'filename'),
              State('upload-data', 'last_modified'))
def update_output(nc,list_of_contents, list_of_names, list_of_dates):
    if list_of_contents is not None:
        children = [
            parse_contents(c, n, d) for c, n, d in
            zip(list_of_contents, list_of_names, list_of_dates)]
        return children