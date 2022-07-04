import dash
from dash import html, dash_table, Output, Input
import dash_bootstrap_components as dbc
from services import connection

dash.register_page(__name__)
query = ''


def statistics_page():
    clients = connection.get_clients()
    technical = connection.get_technical()
    return html.Div([
        html.H1('Statistics', style={'textAlign': 'center'}, className='mb-4'),
        render_table(clients, 'Clients info', 'nombre'),
        render_table(technical, 'Technical info'),
        html.Div(id='result')
    ], id='statistics')


def render_table(df, title, column_name=''):
    global query
    if column_name:
        df = df[df[column_name].str.contains(query)]
    return html.Div([
        dbc.Row([
            dbc.Col(html.H3(title, className='m-0'), width='auto'),
            dbc.Col(dbc.Input(id='input', placeholder='Search...', type='text'))
        ], align='center', className='mb-1'),
        dash_table.DataTable(
            df.to_dict('records'),
            [{'name': i, 'id': i, 'selectable': False} for i in df.columns],
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
    ], className='table-container mb-4')


layout = statistics_page()
