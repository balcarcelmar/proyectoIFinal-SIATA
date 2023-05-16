import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html, Input, Output, State, callback

# Obtener los datos
url = "http://172.17.0.2:5000/niveles?passw=1234"
data = pd.read_json(url, convert_dates='True')

# Leer información de login
login_info = pd.read_csv('/home/ubuntu/usuarios.csv')
login_tuples = [(str(usuario), str(passw)) for usuario, passw in login_info.values]

# Obtener los datos para el gráfico
latr = [dato['coordenadas'][0]['latitud'] for dato in data['datos'][:100]]
lonr = [dato['coordenadas'][0]['longitud'] for dato in data['datos'][:100]]
zr = [dato['porcentajeNivel'] for dato in data['datos'][:100]]

# Configurar el gráfico
fig = go.Figure(go.Densitymapbox(
    lat=latr,
    lon=lonr,
    z=zr,
    radius=20,
    opacity=0.9,
    zmin=0,
    zmax=100
))
fig.update_layout(
    mapbox_style='stamen-terrain',
    mapbox_center_lon=-75.589,
    mapbox_center_lat=6.2429,
    margin={"r": 0, "t": 0, "l": 0, "b": 0}
)
# Creación página web
app = dash.Dash(__name__)
principal_layout = html.Div([
    html.H1("Niveles de agua en Medellin a partir de SIATA"),
    dcc.Location(id='url', refresh=False),
    html.Div(id='page-content')
])
login_layout = html.Div(
    [
        html.H1("Login"),
        html.Label('Nombre de usuario: '),
        dcc.Input(id='usuarios', type='text', value="", persistence=True),
        html.Label('Contraseña: '),
        dcc.Input(id='passw', type='password', value="", persistence=True),
        html.Div(style={'margin-top': '20px'}),
        html.Button("Ingresar", id='btn_ingresar', n_clicks=0),
    ], style={'display': 'flex', 'flexDirection': 'column'}
)
info_estaciones = html.Div([
    html.H3("Información de las estaciones"),
    dcc.Graph(figure=fig)
])

app.layout = principal_layout
app.validation_layout = html.Div([
    principal_layout,
    login_layout,
    info_estaciones
])

@app.callback(Output('page-content', 'children'), [Input('url', 'pathname')])
def display_page(pathname):
    if pathname == "/":
        return login_layout
    elif pathname == "/estaciones":
        return info_estaciones
    else:
        return html.Div([
            html.H1("Acceso denegado"),
            dcc.Link("Regresar", href='/')
        ])
@app.callback(
    Output('url', 'pathname'),
    [Input('btn_ingresar', 'n_clicks')],
    [State('usuarios', 'value'), State('passw', 'value')]
)
def update_page(n_clicks, input_usuarios, input_passw):
    if n_clicks > 0:
        if (input_usuarios, input_passw) in login_tuples:
            return '/estaciones'
        else:
            return '/other'
if __name__ == '__main__':
    app.run_server(host='0.0.0.0',port=80)

