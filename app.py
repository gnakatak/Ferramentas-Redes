import streamlit as st
import requests
# Importa o módulo dashboard
from  ferramentas import dashboard, speedtest_module, traceroute_dev, chat

st.set_page_config(page_title="Ferramentas de Rede", layout="centered")

# --- Funções para simular as páginas ---
def homepage():
    st.title("Olá Streamlit")

def dashboard_page():
    dashboard.render_dashboard() 

def speedtest_page():
    speedtest_module.speedtest_teste()

def traceroute_page():
    traceroute_dev.traceroute_dev()

def chat_page():
    chat.chat_dev()

def about_page():
    st.title("Sobre Nós")
    st.write("Informações sobre o projeto e a equipe.")

# --- Lógica de Navegação na Barra Lateral ---
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
