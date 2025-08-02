from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel
from typing import List
import pandas as pd

from utils import carregar_dados, filtrar_por_ano, calcular_media_ipca

app = FastAPI(title="API de Indicadores Econômicos")

# Modelos de resposta
class Indicador(BaseModel):
    ano: int
    mes: int
    ipca: float

class MediaIPCA(BaseModel):
    ano: int
    media_ipca: float

@app.get("/")
def raiz():
    return {"mensagem": "Bem-vindo à API de Indicadores Econômicos"}

@app.get("/indicadores")
def listar_indicadores():
    df = carregar_dados()
    return df.to_dict(orient="records")

@app.get("/indicadores/ipca", response_model=List[Indicador])
def ipca_por_ano(ano: int = Query(..., description="Ano desejado, ex: 2023")):
    df = carregar_dados()
    dados_filtrados = df[df['ano'] == ano]
    if dados_filtrados.empty:
        raise HTTPException(status_code=404, detail=f"Nenhum dado encontrado para o ano {ano}")
    return dados_filtrados.to_dict(orient="records")

@app.get("/indicadores/ipca/media", response_model=MediaIPCA)
def media_ipca(ano: int = Query(..., description="Ano desejado para média")):
    df = carregar_dados()
    dados_filtrados = df[df['ano'] == ano]
    if dados_filtrados.empty:
        raise HTTPException(status_code=404, detail=f"Não há IPCA disponível para o ano {ano}")
    media = dados_filtrados['ipca'].mean()
    return {
        "ano": ano
        , "media_ipca": round(media, 2)
    }