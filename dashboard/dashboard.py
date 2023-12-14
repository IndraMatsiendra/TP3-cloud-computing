from dash import Dash, html, dcc, callback, Output, Input
import plotly.express as px
import pandas as pd
import redis
import json
from datetime import datetime, timedelta

# Inicializar o aplicativo Dash
app = Dash(__name__)

# Inicializar a conexão com o Redis
redis_client = redis.StrictRedis(host='192.168.121.66', port=6379)

#Dados de todas as CPUs monitoradas nos últimos 10 minutos
graph_data = {}

# Layout do aplicativo
app.layout = html.Div([
    html.H1(children='Monitoring Dashboard', style={'textAlign': 'center'}),
    dcc.Dropdown(options=[{'label': cpu, 'value': cpu} for cpu, value in graph_data.items()], value='avg-util-cpu0-60sec', id='dropdown-selection'),
    dcc.Graph(id='live-update-graph'),
    dcc.Interval(
        id='interval-component',
        interval=5*1000,  # em milissegundos
        n_intervals=0
    ),
])

# Callback para atualizar o gráfico
@app.callback(Output('live-update-graph', 'figure'), Output('dropdown-selection', 'options'),
              Input('interval-component', 'n_intervals'), Input('dropdown-selection', 'value'))
def update_graph(interval, selectedCPU):
    # Obter os dados mais recentes do Redis
    json_data = redis_client.get('etelvinaoliveira-proj3-output')
    if json_data:
        data = json.loads(json_data)
    else:
        data = {}

    # Adicionar dados às listas correspondentes
    for cpu, value in data.items():
        if graph_data.get(cpu):
            graph_data[cpu].append(value)

            # Manter apenas os últimos 10 minutos (120 pontos com intervalo de 5 segundos)
            graph_data[cpu] = graph_data[cpu][-120:]
        else:
            graph_data[cpu] = [value]

    # Construir o gráfico Plotly
    x_data = list(range(len(graph_data[selectedCPU])))
    y_data = graph_data[selectedCPU]

    df = pd.DataFrame({'X': x_data, 'Y': y_data})
    fig = px.line(df, x='X', y='Y', title=f'Monitoring - {selectedCPU}') #x='timestamp', y='usage' --> depois

    return fig, [{'label': cpu, 'value': cpu} for cpu, value in graph_data.items()]

if __name__ == '__main__':
    app.run_server(host='0.0.0.0', port=32179, debug=True)
