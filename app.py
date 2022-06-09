from dash import Dash, dcc, html, Input, Output

app = Dash(__name__)
app.title = 'Celsia Data Validator'
app.layout = html.Div([
    html.H1('Hola mundo', style={'textAlign': 'center'})

])

if __name__ == '__main__':
    app.run_server(debug=True)
