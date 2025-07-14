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
    # Injeta JS para detectar o IP do cliente e preencher o input escondido
    st.markdown("""
    <script>
    (async function() {
        try {
            const res = await fetch('https://api64.ipify.org?format=json');
            const data = await res.json();
            const ip = data.ip;
            const input = window.parent.document.querySelector("input#client_ip_hidden");
            if (input) {
                input.value = ip;
                input.dispatchEvent(new Event("change", { bubbles: true }));
            }
        } catch (e) {
            console.log("Erro ao obter IP do cliente:", e);
        }
    })();
    </script>
    """, unsafe_allow_html=True)

    # Campo oculto para receber IP detectado
    st.markdown("""
    <style>
    input#client_ip_hidden {
        display: none;
    }
    </style>
    """, unsafe_allow_html=True)

    client_ip = st.text_input(
        label="IP oculto para captura via JS",
        key="client_ip_hidden",
        label_visibility="hidden"
    )

    # Usar IP detectado ou fallback para None (que indica o IP do servidor na consulta)
    ip_para_consultar = client_ip if client_ip else None

    # Consulta ipinfo.io para o IP selecionado
    user_info = get_ipinfo_details(ip_para_consultar)

    st.title("🌍 Visualizador de IP e Localização com ipinfo.io")

    # Informações do servidor (host onde a aplicação roda)
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

    # Informações do usuário (cliente)
    st.header("👤 Seu IP e Localização")
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

    st.info("🔎 Dados obtidos pela API pública ipinfo.io. A precisão depende do IP detectado e da infraestrutura da rede.")
