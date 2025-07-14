import streamlit as st
import requests

def get_ipinfo_details(ip=None):
    """Puxa dados da API ipinfo.io para o IP dado ou para o IP público da requisição."""
    base_url = "https://ipinfo.io"
    url = f"{base_url}/{ip}/json" if ip else f"{base_url}/json"
    try:
        resp = requests.get(url, timeout=5)
        resp.raise_for_status()
        data = resp.json()
        return {
            "ip": data.get("ip", "N/A"),
            "city": data.get("city", "N/A"),
            "region": data.get("region", "N/A"),
            "country": data.get("country", "N/A"),
            "org": data.get("org", "N/A"),
            "hostname": data.get("hostname", "N/A"),
            "success": True,
        }
    except Exception as e:
        st.error(f"Erro ao obter dados de ipinfo.io: {e}")
        return {"success": False}

def ip_viewer():
    st.title("🌍 Visualizador de IP e Localização com ipinfo.io")

    # Dados do servidor (aplicação hospedada)
    st.header("💻 Informações do Servidor da Aplicação")
    server_info = get_ipinfo_details()
    if server_info["success"]:
        col1, col2, col3 = st.columns([2,1,1])
        col1.metric("IP do Servidor", server_info["ip"])
        col2.metric("País", server_info["country"])
        col3.metric("Cidade", server_info["city"])
        st.markdown(f"**Região:** {server_info['region']}")
        st.markdown(f"**Hostname:** {server_info['hostname']}")
        st.markdown(f"**Organização / ISP:** {server_info['org']}")
    else:
        st.error("Não foi possível obter as informações do servidor.")

    st.markdown("---")

    # Tenta descobrir IP do usuário a partir do query param 'client_ip' (se houver)
    user_ip = st.query_params.get("client_ip", [None])[0]
    if not user_ip:
        # fallback: pegar o IP detectado pela própria API (ipinfo) sem especificar IP
        user_ip = None

    st.header("👤 Seu IP e Localização")
    user_info = get_ipinfo_details(user_ip)
    if user_info["success"]:
        col1, col2, col3 = st.columns([2,1,1])
        col1.metric("Seu IP Público", user_info["ip"])
        col2.metric("País", user_info["country"])
        col3.metric("Cidade", user_info["city"])
        st.markdown(f"**Região:** {user_info['region']}")
        st.markdown(f"**Hostname:** {user_info['hostname']}")
        st.markdown(f"**Organização / ISP:** {user_info['org']}")
    else:
        st.error("Não foi possível obter as informações do seu IP.")

    st.info(
        "🔎 Dados obtidos pela API pública ipinfo.io. "
        "A precisão depende do IP detectado e da infraestrutura da rede."
    )