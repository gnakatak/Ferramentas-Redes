import streamlit as st
import requests

st.title("Teste de Integração Frontend-Backend")

if st.button("Pegar mensagem do backend"):
    try:
        response = requests.get("http://localhost:5000/api/hello")
        data = response.json()
        st.success(data["message"])
    except Exception as e:
        st.error(f"Erro ao conectar com backend: {e}")
