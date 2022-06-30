from dash import html, dash_table
from services import connection


def statistics_page():
    clients = connection.get_clients()

    return html.Div([
        html.H1('Statistics', style={'textAlign': 'center'}),
        dash_table.DataTable(
            clients.to_dict('records'),
            [{"name": i, "id": i} for i in clients.columns],
            page_size=10)
    ])
