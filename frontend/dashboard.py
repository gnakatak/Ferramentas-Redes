import streamlit as st
import requests

st.set_page_config(page_title="Ferramentas de Rede", layout="centered")

st.title("📡 Ferramentas de Rede")

# 📌 Entrada de dados (IP ou domínio e número de pacotes)
host = st.text_input("Endereço IP ou domínio", value="8.8.8.8")
count = st.number_input("Número de pacotes (ping)", min_value=1, max_value=50, value=3)

# ==========================
# 🎯 MEDIDOR DE LATÊNCIA
# ==========================
st.subheader("📍 Medidor de Latência da Rede")

if st.button("🔍 Medir Latência (Ping)"):
    try:
        response = requests.get("http://127.0.0.1:5000/api/metrics/ping", params={"host": host, "count": count})
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
# 🚀 MEDIDOR DE VAZÃO
# ==========================
st.subheader("🚀 Medidor de Vazão da Rede (Throughput)")

if st.button("📦 Medir Throughput"):
    try:
        response = requests.get("http://127.0.0.1:5000/api/metrics/throughput")
        data = response.json()

        if data["success"]:
            st.markdown(f"**Tempo total:** {data['tempo_s']} segundos")
            st.markdown(f"**Dados transferidos:** {data['dados_kB']:,} KB")
            st.markdown(f"**Vazão estimada:** {data['throughput_kbps'] / 1000:.2f} Mbps")
        else:
            st.error("Erro ao medir throughput.")
    except Exception as e:
        st.error(f"Erro: {e}")
