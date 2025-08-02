import pandas as pd

def carregar_dados():
    return pd.read_csv('indicadores.csv')

def filtrar_por_ano(df: pd.DataFrame, ano: int):
    return df[df['ano'] == ano]

def calcular_media_ipca(df: pd.DataFrame):
    return round(df['ipca'].mean(), 2)