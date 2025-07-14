import streamlit as st
import requests
from ferramentas import dashboard, speedtest_module, traceroute_dev, chat

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

# Funções para simular as páginas
def homepage():
    reset_speedtest_state()
    st.title("Olá Streamlit")

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

def about_page():
    reset_speedtest_state()
    st.title("Sobre Nós")
    st.write("Informações sobre o projeto e a equipe.")

# Lógica de Navegação na Barra Lateral
st.sidebar.title("Navegação")
page = st.sidebar.radio("Escolha uma página:", ["Início", "Dashboard", "SpeedTest", "Traceroute", "Chat", "Sobre"])

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
elif page == "Sobre":
    about_page()