import streamlit as st
import requests

st.set_page_config(page_title="Classificador de Conteúdo", layout="centered")

st.title("🔍 Classificador de Conteúdo por URL")

# Entrada do usuário
url_input = st.text_input("Informe a URL que deseja classificar:")

if st.button("Classificar"):
    if url_input:
        try:
            # Fazendo a chamada para a API (ajuste o endpoint conforme necessário)
            api_url = "http://localhost:8000/classificar"  # Substitua pela URL da sua API
            response = requests.post(api_url, json={"url": url_input})

            if response.status_code == 200:
                resultado = response.json().get("classificacao", "Nenhum resultado retornado.")
                st.text_area("Resultado da Classificação:", resultado, height=200)
            else:
                st.error(f"Erro ao consultar a API: {response.status_code}")
        except Exception as e:
            st.error(f"Ocorreu um erro: {e}")
    else:
        st.warning("Por favor, insira uma URL antes de classificar.")
