# Dashboard per l'analisi delle prestazioni aziendali nel settore primario
# Autore: Carmelo Panepinto
# Versione: 1.0
# Ultima modifica: 13/02/2024

import dash
from dash import dcc, html
import plotly.express as px
import pandas as pd
import dash_bootstrap_components as dbc
from dash.dependencies import Input, Output

# Caricamento dati
df = pd.read_csv("./Simulatore/dati_simulati.csv")

# Parametri selezionabili
parametri = [
    'Temperatura (°C)', 'Umidità (%)', 'Precipitazioni (mm)', 'Ore di Luce (h)',
    'Tempi Crescita Grano (giorni)', 'Uso Fertilizzanti Grano (kg/ha)', 'Consumo Acqua Grano (litri)'
]

# Inizializzazione dell'app Dash
app = dash.Dash(__name__, external_stylesheets=[dbc.themes.BOOTSTRAP])

# Layout
app.layout = dbc.Container([
    html.H1("Dashboard Analisi Aziendale"),
    dbc.Row([
        dbc.Col([
            html.Label("Seleziona Parametri:"),
            dcc.Dropdown(id='parametri', options=[{'label': p, 'value': p} for p in parametri],
                         value=['Temperatura (°C)'], multi=True),
        ], width=6),
        dbc.Col([
            html.Label("Intervallo Giorni:"),
            dcc.RangeSlider(id='intervallo-giorni', min=1, max=len(df), step=1,
                            value=[1, len(df)], marks={i: str(i) for i in range(1, len(df)+1, len(df)//5)})
        ], width=6)
    ]),
    html.Div(id='grafici-parametri'),
    dcc.Graph(id='grafico-produzione'),
    dcc.Graph(id='grafico-correlazione')
])

# Callback per aggiornare i grafici
@app.callback(
    Output('grafici-parametri', 'children'),
    [Input('intervallo-giorni', 'value'), Input('parametri', 'value')]
)
def aggiorna_grafici(intervallo, selezione):
    # Filtra i dati per l'intervallo selezionato
    df_filtro = df.iloc[intervallo[0]-1:intervallo[1]]
    return [dcc.Graph(figure=px.line(df_filtro, x='Giorno', y=p, title=f'Andamento {p}')) for p in selezione]

@app.callback(
    Output('grafico-produzione', 'figure'),
    Input('intervallo-giorni', 'value')
)
def aggiorna_produzione(intervallo):
    # Filtra i dati per l'intervallo selezionato
    df_filtro = df.iloc[intervallo[0]-1:intervallo[1]]
    # Melt i dati per creare un grafico a barre
    df_melt = df_filtro.melt(id_vars=['Giorno'], value_vars=['Raccolto Grano (kg)'],
                              var_name='Coltura', value_name='Produzione')
    return px.line(df_melt, x='Giorno', y='Produzione', color='Coltura', title='Andamento Produzione')

@app.callback(
    Output('grafico-correlazione', 'figure'),
    Input('intervallo-giorni', 'value')
)
def aggiorna_correlazione(intervallo):
    # Filtra i dati per l'intervallo selezionato
    df_filtro = df.iloc[intervallo[0]-1:intervallo[1]]
    return px.scatter(df_filtro, x='Umidità (%)', y='Consumo Acqua Grano (litri)',
                       title='Correlazione Umidità e Consumo Acqua', trendline='ols')

# Esecuzione
if __name__ == '__main__':
    app.run_server(debug=True)

