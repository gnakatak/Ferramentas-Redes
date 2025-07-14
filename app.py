import streamlit as st
from ferramentas import dashboard, speedtest_module, traceroute_dev, chat, visualizador_ip, postman , whois_module, port_scanner

st.set_page_config(page_title="Ferramentas de Rede", layout="centered")

# Função para resetar estados do SpeedTest
def reset_speedtest_state():
    if "dados" in st.session_state:
        del st.session_state.dados
    if "monitorando" in st.session_state:
        del st.session_state.monitorando
    if "ultimo_teste" in st.session_state:
        del st.session_state.ultimo_teste
    if "proximo_teste" in st.session_state:
        del st.session_state.proximo_teste

# Função para a página inicial
def homepage():
    reset_speedtest_state()
    st.title("Bem-vindo às Ferramentas de Rede")
    st.write("Explore ferramentas para monitoramento de rede, como SpeedTest, Traceroute e Chat em tempo real.")
    
    # Chamar o visualizador de IP
    visualizador_ip.ip_viewer()

def dashboard_page():
    reset_speedtest_state()
    dashboard.render_dashboard() 

def speedtest_page():
    speedtest_module.speedtest_teste()

def traceroute_page():
    reset_speedtest_state()
    traceroute_dev.traceroute_dev()

def chat_page():
    reset_speedtest_state()
    chat.chat_dev()

def postman_page():
    reset_speedtest_state()
    postman.postman_interface()


def whois_page():
    reset_speedtest_state()
    whois_module.whois_lookup()

def port_scanner_page():
    reset_speedtest_state()
    port_scanner.port_scanner()


def about_page():
    reset_speedtest_state()
    st.title("Sobre Nós")
    st.write("Informações sobre o projeto e a equipe.")

# Lógica de Navegação na Barra Lateral
st.sidebar.title("Navegação")
page = st.sidebar.radio("Escolha uma página:", ["Início", "Dashboard", "SpeedTest", "Traceroute", "Chat", "Postman", "Whois", "Port Scanner", "Sobre"])

if page == "Início":
    homepage()
elif page == "Dashboard":
    dashboard_page()
elif page == "SpeedTest":
    speedtest_page()
elif page == "Traceroute":
    traceroute_page()
elif page == "Chat":
    chat_page()
elif page == "Postman":
    postman_page()
elif page == "Whois":
    whois_page()
elif page == "Port Scanner":
    port_scanner_page()
elif page == "Sobre":
    about_page()