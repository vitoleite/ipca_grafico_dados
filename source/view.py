import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from .transform import dataFormat

def data_copy() -> pd.DataFrame:
    df_original = dataFormat().dataTransform()
    df_copy = df_original.copy()

    # Realizando um filtro para selecionar informações posteriores a 1999 para apenas o mês de Dezembro
    df_copy = df_copy[(df_copy['Ano'] > 1999) & (df_copy['Mês'].str.contains('dezembro'))]
    return df_copy

def view_graph():
    df_copy = data_copy()
    # Utilizando algumas features do Plotly para criar um gráfico

    # Passando o DataFrame como fonte de dados e escolhendo os eixos devidos
    fig = px.bar(df_copy, x = 'Ano', y = 'Variação anual (%)', text_auto = '.1f')

    # Definindo os rótulos de dados como fonte 10 e alocados fora das colunas internas
    fig.update_traces(textfont_size = 7, textangle = 0, textposition = 'outside', marker_color='midnightblue')

    # Ajustando as informações do gráfico, adicionando título, centralizando e formatando eixos
    fig.update_layout(
        title = {
            'text':'Inflação nos últimos anos <br><sup>Variação anual, em %',
            'y': 0.95,
            'x': 0.5,
            'xanchor': 'center',
            'yanchor': 'top',
            'font': {'size':20, 'color': 'darkslategrey', 'family': 'luminari, fantasy'}
        },
        yaxis = dict(
            title = '(%)',
            titlefont_size=12),
        xaxis = dict(
            title = 'Período',
            titlefont_size = 12,
            type = 'category'),
        uniformtext_minsize = 10,
        uniformtext_mode = 'hide',
        paper_bgcolor='rgb(255,255,255)',
        plot_bgcolor='rgb(255,255,255)',
    )

    # Ajustando o ângulo do eixo X
    fig.update_xaxes(tickangle=-60)

    return fig

def saving_graph():
    fig = view_graph()
    fig.write_image('output/figura_final.jpeg', width=1280, height=720)