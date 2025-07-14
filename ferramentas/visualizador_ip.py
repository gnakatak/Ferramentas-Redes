import streamlit as st
import requests

def ip_viewer():
    """Renderiza um visualizador de IP público, país, cidade e IPs adicionais."""
    st.subheader("📍 Seu Endereço IP e Localização")
    st.write("Aqui você pode ver seu endereço IP público, o país, a cidade e quaisquer IPs adicionais (como proxies) associados (baseados em dados de geolocalização não invasivos).")

    def get_client_ip():
        """Tenta obter o IP principal do cliente e IPs adicionais via headers ou API externa."""
        try:
            # Tenta obter o IP via headers do Streamlit
            headers = st.context.headers if hasattr(st, 'context') else {}
            x_forwarded_for = headers.get("X-Forwarded-For", None)
            if x_forwarded_for and x_forwarded_for != "Unknown":
                # Dividir IPs em uma lista, removendo espaços
                ip_list = [ip.strip() for ip in x_forwarded_for.split(",")]
                primary_ip = ip_list[0]  # Primeiro IP é o cliente
                additional_ips = ip_list[1:] if len(ip_list) > 1 else []
                st.write(f"[Debug] IP principal via X-Forwarded-For: {primary_ip}")
                if additional_ips:
                    st.write(f"[Debug] IPs adicionais: {additional_ips}")
                return primary_ip, additional_ips

            # Fallback: usar ipify.org para obter o IP público
            response = requests.get("https://api.ipify.org", timeout=5)
            response.raise_for_status()
            primary_ip = response.text.strip()
            st.write(f"[Debug] IP obtido via ipify.org: {primary_ip}")
            return primary_ip, []
        except Exception as e:
            st.write(f"[Debug] Erro ao obter IP: {str(e)}")
            return "Unknown", []

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
                st.write(f"[Debug] Cidade: {city}, País: {country}")
                return city, country
            else:
                st.write("[Debug] API ip-api.com retornou status de falha")
                return "N/A", "N/A"
        except Exception as e:
            st.write(f"[Debug] Erro ao obter cidade/país: {str(e)}")
            return "N/A", "N/A"

    try:
        # Obter IP principal e IPs adicionais
        primary_ip, additional_ips = get_client_ip()
        city, country = get_city_and_country(primary_ip)

        # Exibir IP principal, país e cidade em três colunas com tamanhos ajustados
        col1, col2, col3 = st.columns([2, 1, 1])  # Maior espaço para IP
        with col1:
            st.metric(label="Seu IP Público", value=primary_ip)
        with col2:
            st.metric(label="País", value=country)
        with col3:
            st.metric(label="Cidade", value=city)

        # Exibir IPs adicionais (se houver) abaixo
        if additional_ips:
            st.write("**IPs Adicionais (Proxies):**")
            st.text(", ".join(additional_ips))

        if primary_ip == "Unknown":
            st.error("Não foi possível obter o endereço IP.")
        else:
            st.info("Nota: Usamos serviços de geolocalização (ip-api.com e ipify.org) para estimar sua cidade e país com base no IP. Nenhum dado pessoal é armazenado. df")

    except Exception as e:
        st.error(f"Erro ao obter informações de IP: {str(e)}")