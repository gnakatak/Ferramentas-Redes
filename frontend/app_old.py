import streamlit as st
import requests

BACKEND_URL = "http://localhost:5000"

st.title("Teste de Integração Frontend-Backend")

if st.button("Pegar mensagem do backend"):
    try:
        response = requests.get(f"{BACKEND_URL}/api/hello")
        data = response.json()
        st.success(data) 
    except Exception as e:
        st.error(f"Erro ao conectar com backend: {e}")

if st.button("Pegar mensagem de despedida"):
    try: 
        response = requests.get(f"{BACKEND_URL}/api/goodbye")
        data = response.json()
        st.success(data["message"])
    except Exception as e:
        st.error(f"Erro ao conectar com backend: {e}")
