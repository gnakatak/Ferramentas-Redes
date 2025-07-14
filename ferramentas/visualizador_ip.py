import streamlit as st
import requests

def ip_viewer():
    """Renderiza um visualizador de IP público, país, cidade e IPs adicionais, separados por servidor e usuário."""
    st.subheader("📍 Seu Endereço IP e Localização")
    st.write("Aqui você pode ver seu endereço IP público, o país, a cidade e quaisquer IPs adicionais (como proxies) associados (baseados em dados de geolocalização não invasivos).")

    @st.cache_data(ttl=3600) # Cachear resultados para evitar excesso de requisições às APIs
    def get_public_ip_from_api(api_url="https://api.ipify.org"):
        """Obtém um IP público de uma API externa."""
        try:
            response = requests.get(api_url, timeout=5)
            response.raise_for_status()
            return response.text.strip()
        except requests.exceptions.ConnectionError as e:
            st.error(f"Erro de Conexão: Verifique sua internet ou DNS ({api_url}).")
            return "Erro de Conexão"
        except requests.exceptions.Timeout:
            st.error(f"Timeout: A requisição demorou demais ({api_url}).")
            return "Timeout"
        except requests.exceptions.HTTPError as e:
            st.error(f"Erro HTTP: {e.response.status_code} - {e.response.text} ({api_url}).")
            return "Erro HTTP"
        except requests.exceptions.RequestException as e:
            st.error(f"Erro na Requisição: {e} ({api_url}).")
            return "Erro Requisição"
        except Exception as e:
            st.error(f"Erro inesperado ao obter IP de {api_url}: {str(e)}")
            return "Erro Inesperado"

    @st.cache_data(ttl=3600) # Cachear resultados para evitar excesso de requisições às APIs
    def get_geolocation(ip_address):
        """Obtém a cidade e o país associados ao IP usando ipapi.co."""
        if not ip_address or ip_address in ["Unknown", "Erro de Conexão", "Timeout", "Erro HTTP", "Erro Requisição", "Erro Inesperado"] or ip_address.startswith(("10.", "172.16.", "192.168.")):
            return "N/A", "N/A", [] # Não tentar geolocalizar IPs privados ou inválidos

        try:
            response = requests.get(f"https://ipapi.co/{ip_address}/json/", timeout=5)
            response.raise_for_status()
            data = response.json()

            if data and not data.get("error"):
                city = data.get("city", "N/A")
                country = data.get("country_name", "N/A")
                # Adicione informações de ISP ou organização se disponíveis e úteis
                org = data.get("org", "N/A")
                isp = data.get("isp", "N/A")
                additional_info = []
                if org and org != "N/A":
                    additional_info.append(f"Org: {org}")
                if isp and isp != "N/A":
                    additional_info.append(f"ISP: {isp}")
                return city, country, additional_info
            else:
                reason = data.get('reason', 'Desconhecido')
                st.write(f"[Debug] API ipapi.co retornou falha ou erro para {ip_address}: {reason}")
                return "N/A", "N/A", []
        except requests.exceptions.ConnectionError as e:
            st.write(f"[Debug] Erro de Conexão (ipapi.co): {e}")
            return "N/A", "N/A", []
        except requests.exceptions.Timeout:
            st.write("[Debug] Timeout (ipapi.co).")
            return "N/A", "N/A", []
        except requests.exceptions.HTTPError as e:
            st.write(f"[Debug] Erro HTTP (ipapi.co): {e.response.status_code} - {e.response.text}")
            if e.response.status_code == 429:
                st.warning("Limite de requisições da API de geolocalização excedido.")
            return "N/A", "N/A", []
        except requests.exceptions.RequestException as e:
            st.write(f"[Debug] Erro na Requisição (ipapi.co): {e}")
            return "N/A", "N/A", []
        except Exception as e:
            st.write(f"[Debug] Erro inesperado ao obter geolocalização para {ip_address}: {str(e)}")
            return "N/A", "N/A", []

    # --- Seção: Informações do Servidor da Aplicação ---
    st.markdown("---")
    st.subheader("💻 Informações do Servidor da Aplicação")
    st.info("Este é o endereço IP e a localização do servidor onde esta aplicação está hospedada. É o IP que ela usa para acessar a internet.")

    server_ip = get_public_ip_from_api()
    server_city, server_country, server_additional_info = get_geolocation(server_ip)

    col_s1, col_s2, col_s3 = st.columns([2, 1, 1])
    with col_s1:
        st.metric(label="IP do Servidor", value=server_ip)
    with col_s2:
        st.metric(label="País (Servidor)", value=server_country)
    with col_s3:
        st.metric(label="Cidade (Servidor)", value=server_city)
    if server_additional_info:
        st.caption(f"Detalhes: {', '.join(server_additional_info)}")


    # --- Seção: Seu IP (Acessado do seu Navegador) ---
    st.markdown("---")
    st.subheader("👤 Seu IP (Visualizado pelo Servidor)")
    st.info("Este é o endereço IP que o servidor da aplicação detecta do seu navegador. Ele pode ser diferente do seu IP real se você estiver usando VPN, proxy, ou devido à configuração da sua rede.")

    user_ip_from_headers = st.query_params.get("x-forwarded-for", None)
    user_additional_ips = []
    if user_ip_from_headers and user_ip_from_headers != "Unknown":
        ip_list = [ip.strip() for ip in user_ip_from_headers.split(",")]
        primary_user_ip = ip_list[0]
        user_additional_ips = ip_list[1:] if len(ip_list) > 1 else []
    else:
        # Fallback se X-Forwarded-For não estiver presente ou for "Unknown"
        # Neste caso, o IP do usuário é o mesmo do servidor que faz a requisição
        # (o que pode ser enganoso, mas é o melhor que se pode fazer sem JS cliente-side)
        primary_user_ip = server_ip # Assume que o IP do servidor é o que o navegador está vendo se XFF falha
        st.warning("Não foi possível detectar seu IP direto via cabeçalhos. Exibindo o IP do servidor como referência.")


    user_city, user_country, user_additional_info = get_geolocation(primary_user_ip)

    col_u1, col_u2, col_u3 = st.columns([2, 1, 1])
    with col_u1:
        st.metric(label="Seu IP Público", value=primary_user_ip)
    with col_u2:
        st.metric(label="País (Você)", value=user_country)
    with col_u3:
        st.metric(label="Cidade (Você)", value=user_city)
    if user_additional_ips:
        st.caption(f"IPs Adicionais (Proxies/Encaminhadores): {', '.join(user_additional_ips)}")
    if user_additional_info:
        st.caption(f"Detalhes: {', '.join(user_additional_info)}")


    st.markdown("---")
    st.info("Nota Geral: Usamos serviços de geolocalização (ipapi.co e ipify.org) para estimar a localização baseada no IP. Nenhum dado pessoal é armazenado.")