import streamlit as st
from ferramentas import dashboard, speedtest_module, traceroute_dev, chat, visualizador_ip, postman , whois_module, port_scanner

st.set_page_config(page_title="Ferramentas de Rede", layout="centered")

def reset_speedtest_state():
    if "dados" in st.session_state:
        del st.session_state.dados
    if "monitorando" in st.session_state:
        del st.session_state.monitorando
    if "ultimo_teste" in st.session_state:
        del st.session_state.ultimo_teste
    if "proximo_teste" in st.session_state:
        del st.session_state.proximo_teste

def homepage():
    reset_speedtest_state()
    st.title("Bem-vindo às Ferramentas de Rede")
    st.write("Explore ferramentas para monitoramento de rede, como SpeedTest, Traceroute e Chat em tempo real.")
    
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
    st.title("👨‍💻 Sobre o Projeto")
    st.write("""
        Ferramentas de Rede é uma aplicação web interativa desenvolvida com Python e Streamlit, que reúne diversas ferramentas úteis para análise, teste e visualização de redes em um só lugar.
        Ela foi criada com foco em educação prática, demonstração de conceitos de redes e facilidade de uso, sendo ideal para estudantes, professores e entusiastas da área.
        Com uma interface intuitiva e organização modular, o projeto é de fácil manutenção e expansão por colaboradores da comunidade.
    """)

st.sidebar.title("Navegação")
page = st.sidebar.radio("📌 Escolha uma página:", [
    "🏠 Início",
    "📊 Dashboard",
    "⚡ SpeedTest",
    "🗺️ Traceroute",
    "💬 Chat",
    "📬 Postman",
    "🔍 Whois",
    "🛡️ Port Scanner",
    "ℹ️ Sobre"
])

match page:
    case "🏠 Início":
        homepage()
    case "📊 Dashboard":
        dashboard_page()
    case "⚡ SpeedTest":
        speedtest_page()
    case "🗺️ Traceroute":
        traceroute_page()
    case "💬 Chat":
        chat_page()
    case "📬 Postman":
        postman_page()
    case "🔍 Whois":
        whois_page()
    case "🛡️ Port Scanner":
        port_scanner_page()
    case "ℹ️ Sobre":
        about_page()