import streamlit as st
import requests

def ip_viewer():
    """Renderiza um visualizador de IP público, país e cidade do usuário."""
    st.subheader("📍 Seu Endereço IP e Localização")
    st.write("Aqui você pode ver seu endereço IP público, o país e a cidade associados (baseados em dados de geolocalização não invasivos).")

    def get_client_ip():
        """Tenta obter o IP do cliente via headers ou API externa."""
        try:
            # Tenta obter o IP via headers do Streamlit
            headers = st.context.headers if hasattr(st, 'context') else {}
            ip_address = headers.get("X-Forwarded-For", None)
            if ip_address and ip_address != "Unknown":
                st.write(f"[Debug] IP obtido via X-Forwarded-For: {ip_address}")
                return ip_address

            # Fallback: usar ipify.org para obter o IP público
            response = requests.get("https://api.ipify.org", timeout=5)
            response.raise_for_status()
            ip_address = response.text.strip()
            return ip_address
        except Exception as e:
            st.write(f"Erro ao obter IP: {str(e)}")
            return "Unknown"

    def get_city_and_country(ip_address):
        """Obtém a cidade e o país associados ao IP usando ip-api.com."""
        if ip_address == "Unknown":
            return "N/A", "N/A"
        try:
            response = requests.get(f"http://ip-api.com/json/{ip_address}?fields=status,city,country", timeout=5)
            response.raise_for_status()
            data = response.json()
            if data.get("status") == "success":
                city = data.get("city", "N/A")
                country = data.get("country", "N/A")
                return city, country
            else:
                st.write("API ip-api.com retornou status de falha")
                return "N/A", "N/A"
        except Exception as e:
            st.write(f"[Debug] Erro ao obter cidade/país: {str(e)}")
            return "N/A", "N/A"

    try:
        # Obter IP, cidade e país
        ip_address = get_client_ip()
        city, country = get_city_and_country(ip_address)

        # Exibir IP, país e cidade em três colunas com tamanhos ajustados
        col1, col2, col3 = st.columns([2, 1, 1])  # Maior espaço para IP
        with col1:
            st.metric(label="Seu IP Público", value=ip_address)
        with col2:
            st.metric(label="País", value=country)
        with col3:
            st.metric(label="Cidade", value=city)

        if ip_address == "Unknown":
            st.error("Não foi possível obter o endereço IP.")
        else:
            st.info("Nota: Usamos serviços de geolocalização (ip-api.com e ipify.org) para estimar sua cidade e país com base no IP. Nenhum dado pessoal é armazenado.")

    except Exception as e:
        st.error(f"Erro ao obter informações de IP: {str(e)}")