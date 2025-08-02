import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="IPCA por Ano", layout="centered")
st.title('📊 Consulta IPCA - API')

ano = st.number_input('Escolha um ano:', min_value=2000, max_value=2100, step=1, value=2022)

if st.button("Buscar dados"):
    try:
        url_base = "http://localhost:8000"

        resp_dados = requests.get(f"{url_base}/indicadores/ipca", params={"ano": ano})
        resp_media = requests.get(f"{url_base}/indicadores/ipca/media", params={"ano": ano})

        if resp_dados.status_code == 404:
            st.warning("Ano não encontrado na base de dados.")
        else:
            dados = pd.DataFrame(resp_dados.json())
            media = resp_media.json()["media_ipca"]

            st.subheader(f"📅 IPCA do ano {ano}")
            st.dataframe(dados)

            st.success(f"Média do IPCA: {media:.2f} %")

    except Exception as e:
        st.error(f"Erro ao conectar com a API {e}")