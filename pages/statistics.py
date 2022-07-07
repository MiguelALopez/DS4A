import dash
from dash import html, dash_table, Output, Input, callback, dcc
import dash_bootstrap_components as dbc
from services import connection
import plotly.express as px

global clients
global technical


def statistics_page():
    global clients
    global technical
    clients = connection.get_clients()
    technical = connection.get_technical()
    return html.Div([
        html.H1('Statistics', style={'textAlign': 'center'}, className='mb-4'),
        html.Div([
            dbc.Row([
                dbc.Col(html.H3('Clients info', className='m-0'), width='auto'),
                dbc.Col(dbc.Input(id='client-input', placeholder='Search by nombre...', type='text'))
            ], align='center', className='mb-1'),
            html.Div(render_table(clients, 'nombre'), id='clients-table')
        ], className='table-container mb-4'),
        html.Div([
            dbc.Row([
                dbc.Col(html.H3('Technical info', className='m-0'), width='auto'),
                dbc.Col(dbc.Input(id='technical-input', placeholder='Search by nombre_frontera...', type='text'))
            ], align='center', className='mb-1'),
            html.Div(render_table(technical), id='technical-table')
        ], className='table-container mb-4'),
        html.Div(id='result'),
        dcc.Graph(
            id='hist-client',
            figure=render_client_histogram('tipo_cliente', 'Histograma de tipo de cliente'),
            className='table-container mb-4'
        ),
        dcc.Graph(
            id='hist-business',
            figure=render_client_histogram('empresa', 'Histograma por empresa'),
            className='table-container mb-4'
        ),
        dcc.Graph(
            id='hist-start_date',
            figure=render_client_histogram('fecha_inicio', 'Fecha de inicio del servicio a cada empresa'),
            className='table-container mb-4'
        ),
        dcc.Graph(
            id='hist-uen',
            figure=render_client_histogram('uen', 'Histograma de UEN'),
            className='table-container mb-4'
        ),
        dcc.Graph(
            id='hist-sector',
            figure=render_client_histogram('sector', 'Sector del cliente'),
            className='table-container mb-4'
        ),
        dcc.Graph(
            id='hist-depto',
            figure=render_client_histogram('depto_pto_servicio', 'Histograma de departamento'),
            className='table-container mb-4'
        ),
        dcc.Graph(
            id='hist-stress',
            figure=render_client_histogram('nivel_tension', 'Histograma nivel de tension'),
            className='table-container mb-4'
        ),
        dcc.Graph(
            id='hist-brand',
            figure=render_client_histogram('marca', 'Histograma de marca'),
            className='table-container mb-4'
        ),
        dcc.Graph(
            id='hist-agreement',
            figure=render_client_histogram('tipo_acuerdo', 'Histograma tipo de acuerdo'),
            className='table-container mb-4'
        ),
        dcc.Graph(
            id='hist-agreement',
            figure=render_client_histogram('prop_trafo', 'Histograma de propiedad del transformador'),
            className='table-container mb-4'
        )

    ], id='statistics')


def render_client_histogram(column, title):
    return px.histogram(clients[column], title=title)


def render_table(df, column_name='', query=''):
    if column_name and query:
        df = df[df[column_name].str.contains('(?i)'+query)]
    return dash_table.DataTable(
        df.to_dict('records'),
        [{'name': i, 'id': i, 'selectable': False} for i in df.columns],
        sort_action='native',
        page_size=10,
        style_table={
            'overflowX': 'auto',
            'fontFamily': '"Assistant Arial", sans-serif', 'fontStyle': 'normal',
            'fontSize': '14px'
        },
        row_selectable=False,
        cell_selectable=False,
        style_cell={
            'fontFamily': '"Assistant Arial", sans-serif', 'fontStyle': 'normal',
            'fontSize': '14px',
            'fontWeight': '400',
            'lineHeight': '18px',
            'color': '#394457',
            'border': 'none',
            'padding': '0 17px'
        },
        style_data_conditional=[
            {
                'if': {'row_index': 'even'},
                'backgroundColor': '#F5F7FA',
                'borderRadius: ': '12px'
            }
        ],
        style_header={
            'backgroundColor': 'white',
            'fontFamily': '"Assistant Arial", sans-serif', 'fontStyle': 'normal',
            'fontWeight': '600',
            'fontSize': '14px',
            'color': '#8F9CB4',
            'border': 'none',
            'borderLeft': '1px'
        }
    )


@callback(
    Output(component_id='clients-table', component_property='children'),
    Input(component_id='client-input', component_property='value')
)
def update_client_table(value):
    return render_table(clients, 'nombre', value)


@callback(
    Output(component_id='technical-table', component_property='children'),
    Input(component_id='technical-input', component_property='value')
)
def update_technical_table(value):
    return render_table(technical, 'nombre_frontera', value)
