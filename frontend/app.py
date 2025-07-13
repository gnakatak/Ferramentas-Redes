import streamlit as st
import requests
# Importa o módulo dashboard
import dashboard 
import speedtest_module

# O st.set_page_config() deve ser a PRIMEIRA chamada do Streamlit no seu script principal.
st.set_page_config(page_title="Ferramentas de Rede", layout="centered")

BACKEND_URL = "http://localhost:5000"

# --- Funções para simular as páginas ---
def homepage():
    st.title("Olá Streamlit")
    st.write("Este é o aplicativo básico em Streamlit.")

    if st.button("Pegar mensagem do backend"):
        try:
            response = requests.get(f"{BACKEND_URL}/api/hello")
            data = response.json()
            st.success(data) 
        except Exception as e:
            st.error(f"Erro ao conectar com backend: {e}")

def dashboard_page():
    # Não precisa de st.set_page_config() aqui, pois já foi definido em app.py
    st.title("Página do Dashboard")
    st.write("Aqui você verá as ferramentas de rede.")
    
    # Chama a função render_dashboard() importada do módulo dashboard
    dashboard.render_dashboard(backend_url=BACKEND_URL) 

def dashboard_page():
    # Não precisa de st.set_page_config() aqui, pois já foi definido em app.py
    st.title("Dashboard")
    
    # Chama a função render_dashboard() importada do módulo dashboard
    dashboard.render_dashboard(backend_url=BACKEND_URL) 

def speedtest_page():
    speedtest_module.speedtest_teste()


def about_page():
    st.title("Sobre Nós")
    st.write("Informações sobre o projeto e a equipe.")

# --- Lógica de Navegação na Barra Lateral ---
st.sidebar.title("Navegação")
page = st.sidebar.radio("Escolha uma página:", ["Início", "Dashboard","SpeedTest","Sobre"])

if page == "Início":
    homepage()
elif page == "Dashboard":
    dashboard_page()
elif page == "SpeedTest":
    speedtest_page()
elif page == "Sobre":
    about_page()

# Os botões comentados abaixo não são mais relevantes para a estrutura de navegação com sidebar
# st.link_button("dashboard.py")
# if st.button("Pegar mensagem de despedida"):
#     try: 
#         response = requests.get(f"{BACKEND_URL}/api/goodbye")
#         data = response.json()
#         st.success(data["message"])
#     except Exception as e:
#         st.error(f"Erro ao conectar com backend: {e}")

