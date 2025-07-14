import streamlit as st
import requests

def ip_viewer():
    # Injeta JS para detectar IP do cliente e salvar em st.session_state.client_ip (sem input visível)
    ip_detect_js = """
    <script>
    async function getClientIP() {
    try {
        const res = await fetch('https://api64.ipify.org?format=json');
        const data = await res.json();
        const ip = data.ip;
        // Envia para Streamlit via evento de input
        const streamlit_input = window.parent.document.querySelector('input#client_ip_setter');
        if (streamlit_input) {
            streamlit_input.value = ip;
            streamlit_input.dispatchEvent(new Event('change', { bubbles: true }));
        }
    } catch(e) {
        console.log('Erro ao obter IP:', e);
    }
    }
    getClientIP();
    </script>
    """

    st.markdown(ip_detect_js, unsafe_allow_html=True)

    # Campo oculto pra receber o IP detectado via JS (input escondido via CSS)
    st.markdown(
        """
        <style>
        input#client_ip_setter {
            display:none;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )
    ip_from_js = st.text_input("", key="client_ip_setter")

    # Salva o IP detectado na sessão, se mudou
    if ip_from_js and ip_from_js != st.session_state.get("client_ip", ""):
        st.session_state.client_ip = ip_from_js

    st.title("Visualizador de IP")

    st.write("**IP detectado automaticamente:**", st.session_state.get("client_ip", "Não detectado"))

    # Input para o usuário digitar manualmente o IP
    manual_ip = st.text_input("Digite um IP para consultar (opcional):")

    # Decide qual IP consultar: manual > detectado
    ip_para_consultar = manual_ip.strip() if manual_ip.strip() else st.session_state.get("client_ip")

    st.write("IP a ser consultado:", ip_para_consultar if ip_para_consultar else "Nenhum IP válido")

    # Consulta a API ipinfo.io para o IP selecionado
    if ip_para_consultar:
        try:
            response = requests.get(f"https://ipinfo.io/{ip_para_consultar}/json", timeout=5)
            data = response.json()
            st.write("### Resultado da consulta:")
            st.write(f"- IP: {data.get('ip', 'N/A')}")
            st.write(f"- Cidade: {data.get('city', 'N/A')}")
            st.write(f"- Região: {data.get('region', 'N/A')}")
            st.write(f"- País: {data.get('country', 'N/A')}")
            st.write(f"- Organização: {data.get('org', 'N/A')}")
            st.write(f"- Hostname: {data.get('hostname', 'N/A')}")
        except Exception as e:
            st.error(f"Erro ao consultar IP info: {e}")
    else:
        st.info("Digite um IP para consultar ou aguarde a detecção automática.")
