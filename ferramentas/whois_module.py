import streamlit as st
import whois  
import requests
import certifi
import urllib3
import datetime

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

def get_ipinfo(ip):
    """Consulta localização e ISP do IP via ipinfo.io"""
    try:
        url = f"https://ipinfo.io/{ip}/json"
        resp = requests.get(url, timeout=5, verify=certifi.where())
        resp.raise_for_status()
        data = resp.json()
        return {
            "IP": data.get("ip", "N/A"),
            "Cidade": data.get("city", "N/A"),
            "Região": data.get("region", "N/A"),
            "País": data.get("country", "N/A"),
            "Organização": data.get("org", "N/A"),
            "Hostname": data.get("hostname", "N/A"),
            "Sucesso": True
        }
    except requests.exceptions.SSLError:
        # Tentativa fallback (não seguro)
        try:
            resp = requests.get(url, timeout=5, verify=False)
            resp.raise_for_status()
            data = resp.json()
            return {
                "IP": data.get("ip", "N/A"),
                "Cidade": data.get("city", "N/A"),
                "Região": data.get("region", "N/A"),
                "País": data.get("country", "N/A"),
                "Organização": data.get("org", "N/A"),
                "Hostname": data.get("hostname", "N/A"),
                "Sucesso": True,
                "Aviso": "SSL verification disabled for ipinfo.io fallback"
            }
        except Exception as e:
            return {"Sucesso": False, "Erro": str(e)}
    except Exception as e:
        return {"Sucesso": False, "Erro": str(e)}

def format_date(date_obj):
    if isinstance(date_obj, list):
        return ", ".join([d.strftime("%Y-%m-%d %H:%M:%S %Z").strip() for d in date_obj if d is not None])
    elif isinstance(date_obj, datetime.datetime):
        return date_obj.strftime("%Y-%m-%d %H:%M:%S %Z").strip()
    return "N/A"

def whois_lookup():
    st.title("🔍 Consulta WHOIS + Localização")
    alvo = st.text_input("Digite um domínio ou IP para análise", "google.com")

    if st.button("Consultar"):
        with st.spinner("Consultando informações..."):
            # Dados WHOIS
            st.subheader("📑 Informações WHOIS")
            try:
                w = whois.whois(alvo)
                st.write(f"**Domínio**: {alvo}")
                st.write(f"**Registrar**: {w.registrar if w.registrar else 'N/A'}")
                
                creation_date = format_date(w.creation_date)
                updated_date = format_date(w.updated_date)
                expiration_date = format_date(w.expiration_date)

                st.write(f"**Criado em**: {creation_date}")
                st.write(f"**Atualizado em**: {updated_date}")
                st.write(f"**Expira em**: {expiration_date}")
                st.write(f"**Registrante**: {w.name if w.name else 'N/A'}")
                st.write(f"**Email(s)**: {', '.join(w.emails) if w.emails else 'N/A'}")
                st.write(f"**Servidores DNS**: {', '.join(w.name_servers) if w.name_servers else 'N/A'}")
                
                if w.status:
                    st.write("**Status:**")
                    for status_item in w.status:
                        st.write(f"- {status_item}")
                else:
                    st.write("**Status**: N/A")

            except Exception as e:
                st.error(f"Erro na consulta WHOIS: {e}")
                # Do not return here, as we still want to try IP lookup
            
            st.markdown("---") # Separator for better readability

            # Dados geográficos via IP
            st.subheader("🌎 Localização do IP/Domínio")
            ip_resolvido = None
            try:
                url_dns_google = f"https://dns.google/resolve?name={alvo}&type=A"
                try:
                    ip_resp = requests.get(url_dns_google, timeout=5, verify=certifi.where())
                except requests.exceptions.SSLError:
                    st.warning("Falha na verificação SSL para dns.google. Tentando sem verificação (não recomendado para produção).")
                    ip_resp = requests.get(url_dns_google, timeout=5, verify=False)
                    
                ip_resp.raise_for_status()
                ip_json = ip_resp.json()

                if ip_json and "Answer" in ip_json and ip_json["Answer"]:
                    ip_resolvido = ip_json["Answer"][0]["data"]
                    st.info(f"**IP Resolvido para {alvo}:** {ip_resolvido}")
                else:
                    st.warning(f"Não foi possível resolver o IP para o domínio: {alvo}")

            except Exception as e:
                st.error(f"Erro ao resolver IP via DNS Google: {e}")

            if ip_resolvido:
                geo = get_ipinfo(ip_resolvido)
                if geo.get("Sucesso"):
                    col1, col2, col3 = st.columns(3)
                    col1.metric("País", geo["País"])
                    col2.metric("Região", geo["Região"])
                    col3.metric("Cidade", geo["Cidade"])
                    
                    st.markdown(f"**ISP / Organização:** {geo['Organização']}")
                    st.markdown(f"**Hostname:** {geo['Hostname']}")
                    if "Aviso" in geo:
                        st.warning(geo["Aviso"])
                else:
                    st.warning(f"Não foi possível obter dados de localização para o IP {ip_resolvido}. Erro: {geo.get('Erro', 'Desconhecido')}")
            else:
                st.info("Não foi possível realizar a consulta de localização sem um IP resolvido.")