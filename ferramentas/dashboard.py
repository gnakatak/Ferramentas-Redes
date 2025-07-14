import streamlit as st
import requests
from ferramentas.ping import ping

# Define a função render_dashboard que conterá todo o código do dashboard
def render_dashboard():
    st.title("Página do Dashboard")
    st.write("Aqui você verá as ferramentas de rede.")


    # ==========================
    # 🎯 MEDIDOR DE LATÊNCIA
    # ==========================
    st.subheader("📍 Medidor de Latência da Rede")

    # 📌 Entrada de dados (IP ou domínio e número de pacotes)
    host = st.text_input("Endereço IP ou domínio", value="8.8.8.8")
    count = st.number_input("Número de pacotes (ping)", min_value=1, max_value=50, value=3)

    if st.button("🔍 Medir Latência (Ping)"):
        try:
            response = ping(host=host, count=count)
            data = response.json()

            if data["success"]:
                st.markdown(f"**Host:** {data['host']}")
                st.markdown(f"**Pacotes enviados:** {data['count']}")
                st.markdown(f"**Latência mínima:** {data['min_latency_ms']} ms")
                st.markdown(f"**Latência máxima:** {data['max_latency_ms']} ms")
                st.markdown(f"**Latência média:** {data['avg_latency_ms']} ms")
                st.code(data["output"])
            else:
                st.error("Erro ao executar o ping.")
        except Exception as e:
            st.error(f"Erro: {e}")

    # ==========================
    # 🚀 VER O PROPRIO PING
    # ==========================
