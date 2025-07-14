import streamlit as st
import requests
from datetime import datetime

# Função para obter dados do ipinfo.io para um IP específico
@st.cache_data(ttl=3600)
def get_ip_details(ip=None, token=None):
    base_url = "https://ipinfo.io"
    url = f"{base_url}/{ip}/json" if ip else f"{base_url}/json"
    if token:
        url += f"?token={token}"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return data
    except Exception as e:
        st.error(f"Erro ao buscar dados do ipinfo.io: {e}")
        return {}

# Função que injeta JS para capturar IP público do cliente via api.ipify.org
def get_client_ip_js():
    st.markdown("""
    <script>
    async function getIp() {
        const response = await fetch('https://api.ipify.org?format=json');
        const data = await response.json();
        window.parent.postMessage({func: 'setClientIp', ip: data.ip}, '*');
    }
    getIp();
    </script>
    """, unsafe_allow_html=True)

# Função principal do visualizador
def ip_viewer():
    st.title("🌍 Visualizador de IP e Localização com ipinfo.io")

    if "client_ip" not in st.session_state:
        st.session_state["client_ip"] = None

    get_client_ip_js()  # Injeta JS para pegar IP do cliente

    # Aqui você pode colocar um input oculto para atualizar o IP no estado
    client_ip = st.text_input("IP detectado (via JS):", key="client_ip", value=st.session_state["client_ip"])

    if client_ip:
        st.session_state["client_ip"] = client_ip
        details = get_ip_details(client_ip)  # Consulta ipinfo com o IP do cliente
        st.write(f"**IP:** {details.get('ip', 'N/A')}")
        st.write(f"**Cidade:** {details.get('city', 'N/A')}")
        st.write(f"**Região:** {details.get('region', 'N/A')}")
        st.write(f"**País:** {details.get('country', 'N/A')}")
        st.write(f"**Organização:** {details.get('org', 'N/A')}")
        st.write(f"**Hostname:** {details.get('hostname', 'N/A')}")

    else:
        st.info("Detectando seu IP público via JavaScript...")
