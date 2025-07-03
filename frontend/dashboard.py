import streamlit as st
import requests

st.set_page_config(page_title="Ferramentas de Rede", layout="centered")

BACKEND_URL = "http://127.0.0.1:5000/api"

st.title("📡 Ferramentas de Rede")

host = st.text_input("Endereço IP ou domínio", value="8.8.8.8")
count = st.number_input("Número de pacotes (ping)", min_value=1, max_value=100, value=3)

# ----------------------
if st.button("📶 Medir Latência (Ping)"):
    try:
        res = requests.get(f"{BACKEND_URL}/metrics/ping", params={"host": host, "count": count})
        st.json(res.json())
    except Exception as e:
        st.error(f"Erro: {e}")

# ----------------------
if st.button("📦 Medir Throughput"):
    try:
        res = requests.get(f"{BACKEND_URL}/metrics/throughput")
        st.json(res.json())
    except Exception as e:
        st.error(f"Erro: {e}")
