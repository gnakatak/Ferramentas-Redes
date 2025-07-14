import streamlit as st
import requests

def ip_viewer():
    """Renderiza um visualizador de IP público, país, cidade e IPs adicionais."""
    st.subheader("📍 Seu Endereço IP e Localização")
    st.write("Aqui você pode ver seu endereço IP público, o país, a cidade e quaisquer IPs adicionais (como proxies) associados (baseados em dados de geolocalização não invasivos).")

    def get_client_ip():
        """Tenta obter o IP principal do cliente e IPs adicionais via headers ou API externa."""
        try:
            # Usando st.query_params para obter X-Forwarded-For (novo método)
            x_forwarded_for = st.query_params.get("x-forwarded-for", None)
            if x_forwarded_for and x_forwarded_for != "Unknown":
                ip_list = [ip.strip() for ip in x_forwarded_for.split(",")]
                primary_ip = ip_list[0]
                additional_ips = ip_list[1:] if len(ip_list) > 1 else []
                st.write(f"[Debug] IP principal via X-Forwarded-For (query params): {primary_ip}")
                if additional_ips:
                    st.write(f"[Debug] IPs adicionais: {additional_ips}")
                return primary_ip, additional_ips

            # Fallback: usar ipify.org para obter o IP público
            st.write("[Debug] Tentando obter IP via ipify.org...")
            response = requests.get("https://api.ipify.org", timeout=5)
            response.raise_for_status() # Lança HTTPError para respostas de erro (4xx ou 5xx)
            primary_ip = response.text.strip()
            st.write(f"[Debug] IP obtido via ipify.org: {primary_ip}")
            return primary_ip, []
        except requests.exceptions.ConnectionError as e:
            st.write(f"[Debug] Erro de Conexão (ipify.org): Verifique sua internet ou DNS. {e}")
            return "Unknown", []
        except requests.exceptions.Timeout:
            st.write("[Debug] Timeout (ipify.org): A requisição demorou demais.")
            return "Unknown", []
        except requests.exceptions.HTTPError as e:
            st.write(f"[Debug] Erro HTTP (ipify.org): {e.response.status_code} - {e.response.text}")
            return "Unknown", []
        except requests.exceptions.RequestException as e:
            st.write(f"[Debug] Erro na Requisição (ipify.org): {e}")
            return "Unknown", []
        except Exception as e:
            st.write(f"[Debug] Erro Inesperado ao obter IP: {str(e)}")
            return "Unknown", []

    def get_city_and_country(ip_address):
        """Obtém a cidade e o país associados ao IP usando ipapi.co."""
        if ip_address == "Unknown" or ip_address.startswith(("10.", "172.16.", "192.168.")):
            st.write(f"[Debug] IP privado detectado, não será geolocalizado: {ip_address}")
            return "N/A", "N/A"
        try:
            st.write(f"[Debug] Tentando obter geolocalização para {ip_address} via ipapi.co...")
            response = requests.get(f"https://ipapi.co/{ip_address}/json/", timeout=5)
            response.raise_for_status() # Lança HTTPError para respostas de erro (4xx ou 5xx)
            data = response.json()

            if data and not data.get("error"):
                city = data.get("city", "N/A")
                country = data.get("country_name", "N/A")
                st.write(f"[Debug] Cidade (ipapi.co): {city}, País (ipapi.co): {country}")
                return city, country
            else:
                reason = data.get('reason', 'Desconhecido')
                st.write(f"[Debug] API ipapi.co retornou falha ou erro: {reason}")
                # Pode indicar limite de requisições excedido ou IP inválido
                return "N/A", "N/A"
        except requests.exceptions.ConnectionError as e:
            st.write(f"[Debug] Erro de Conexão (ipapi.co): Verifique sua internet ou DNS. {e}")
            return "N/A", "N/A"
        except requests.exceptions.Timeout:
            st.write("[Debug] Timeout (ipapi.co): A requisição demorou demais.")
            return "N/A", "N/A"
        except requests.exceptions.HTTPError as e:
            st.write(f"[Debug] Erro HTTP (ipapi.co): {e.response.status_code} - {e.response.text}")
            # Um 429 indica "Too Many Requests" (limite de requisições excedido)
            if e.response.status_code == 429:
                st.warning("Limite de requisições da API de geolocalização excedido. Tente novamente mais tarde.")
            return "N/A", "N/A"
        except requests.exceptions.RequestException as e:
            st.write(f"[Debug] Erro na Requisição (ipapi.co): {e}")
            return "N/A", "N/A"
        except Exception as e:
            st.write(f"[Debug] Erro Inesperado ao obter cidade/país: {str(e)}")
            return "N/A", "N/A"

    try:
        primary_ip, additional_ips = get_client_ip()
        city, country = get_city_and_country(primary_ip)

        col1, col2, col3 = st.columns([2, 1, 1])
        with col1:
            st.metric(label="Seu IP Público", value=primary_ip)
        with col2:
            st.metric(label="País", value=country)
        with col3:
            st.metric(label="Cidade", value=city)

        if additional_ips:
            st.write("**IPs Adicionais (Proxies):**")
            st.text(", ".join(additional_ips))

        if primary_ip == "Unknown":
            st.error("Não foi possível obter o endereço IP.")
        elif city == "N/A" and country == "N/A":
            st.warning("Não foi possível obter a geolocalização para o seu IP. Isso pode ocorrer devido a problemas de rede, limites de API ou IPs privados.")
        else:
            st.info("Nota: Usamos serviços de geolocalização (ipapi.co e ipify.org) para estimar sua cidade e país com base no IP. Nenhum dado pessoal é armazenado.")

    except Exception as e:
        st.error(f"Erro ao obter informações de IP: {str(e)}")