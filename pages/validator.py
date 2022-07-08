import dash
#import numpy as np
import pandas as pd
from datetime import datetime
import base64
import io
from dash import html, dcc, dash_table, callback,Output,Input,State
import dash_bootstrap_components as dbc
#from sklearn.ensemble import RandomForestClassifier
#import joblib as joblib

#dash.register_page(__name__, path='/')


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

def cleaning_data(df):
    """Cleans the entry data"""
    
    clean_df = df.drop(columns=['falla','codigo_sic','nivel_tension','fecha_original_de_registro']).copy()
    clean_df = pd.concat([(clean_df["i_a_mean"] - clean_df["i_a_mean"].mean())/clean_df["i_a_mean"].std(),\
                     (clean_df["i_b_mean"] - clean_df["i_b_mean"].mean())/clean_df["i_b_mean"].std(),\
                    (clean_df.vla - clean_df.vla.mean())/clean_df.vla.std(),\
                    (clean_df.vlb - clean_df.vlb.mean())/clean_df.vlb.std(),\
                    (clean_df.vlc - clean_df.vlc.mean())/clean_df.vlc.std(),\
                    (clean_df.kvarhd - clean_df.kvarhd.mean())/clean_df.kvarhd.std(),\
                    (clean_df.kwhd - clean_df.kwhd.mean())/clean_df.kwhd.std(),\
                     pd.get_dummies(clean_df["requiere_medidor_respaldo"], prefix='req_medidor', drop_first=False), \
                    (clean_df["capacidad_kva"] - clean_df["capacidad_kva"].mean())/clean_df["capacidad_kva"].std(),\
                     pd.get_dummies(clean_df["clase_de_precision_tc"], prefix='clasePrecisionTc', drop_first=False), \
                    pd.get_dummies(clean_df["clase_de_precision_tp"], prefix='clasePrecisionTp', drop_first=False), \
                    pd.get_dummies(clean_df["conexion"], prefix='conexion', drop_first=False), \
                    pd.get_dummies(clean_df["departamento"], prefix='departamento', drop_first=False), \
                    pd.get_dummies(clean_df["medio_modem_principal"], prefix='medioModemPpal', drop_first=False), \
                    pd.get_dummies(clean_df["multiplo_prime_read"], prefix='multiploPrimeR', drop_first=False), \
                    (clean_df["multiplo_tc"] - clean_df["multiplo_tc"].mean())/clean_df["multiplo_tc"].std(),\
                    (clean_df["multiplo_tp"] - clean_df["multiplo_tp"].mean())/clean_df["multiplo_tp"].std(),\
                    (clean_df["nivel_de_tension"] - clean_df["nivel_de_tension"].mean())/clean_df["nivel_de_tension"].std(),\
                    (clean_df["punto_de_medicion"] - clean_df["punto_de_medicion"].mean())/clean_df["punto_de_medicion"].std(),\
                    pd.get_dummies(clean_df["relacion_tc"], prefix='realacionTc', drop_first=False), \
                    pd.get_dummies(clean_df["relacion_tp"], prefix='realacionTp', drop_first=False), \
                    (clean_df["tension_kv"] - clean_df["tension_kv"].mean())/clean_df["tension_kv"].std(),\
                    pd.get_dummies(clean_df["tipo_frontera_xm"], prefix='tipoFrontXm', drop_first=False), \
                    pd.get_dummies(clean_df["zona"], prefix='zona', drop_first=False), \
                    pd.get_dummies(clean_df["depto_pto_servicio"], prefix='deptPtoServ', drop_first=False), \
                    pd.get_dummies(clean_df["desc_tipo_cliente"], prefix='descTipoCliente', drop_first=False), \
                    pd.get_dummies(clean_df["marca_modelo"], prefix='marcaModelo', drop_first=False), \
                    pd.get_dummies(clean_df["nivel_tension_2"], prefix='nivelTension', drop_first=False), \
                    pd.get_dummies(clean_df["operador_red"], prefix='operadorRed', drop_first=False), \
                    pd.get_dummies(clean_df["prop_activo"], prefix='propActivo', drop_first=False), \
                    pd.get_dummies(clean_df["sector"], prefix='sector', drop_first=False), \
                    pd.get_dummies(clean_df["tarifa"], prefix='tarifa', drop_first=False), \
                    pd.get_dummies(clean_df["tipo_acuerdo"], prefix='tipoAcuerdo', drop_first=False), \
                    pd.get_dummies(clean_df["zona_ingreso"], prefix='zonaIngreso', drop_first=False)
                   ], axis=1)
    clean_df['Intercept'] = 1
    clean_df = clean_df.dropna()
    return clean_df


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
    #Loading the model
    #cels_rf = joblib.load(r"C:\Users\rsjes\OneDrive\Documentos\GitHub\DS4A\pages\celsia_random_forest.joblib")
    #data = cleaning_data(df)
    #predicted = cels_rf.predict(data)

    

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

layout = validator_page()
