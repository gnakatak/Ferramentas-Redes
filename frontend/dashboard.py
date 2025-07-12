import streamlit as st
import requests

# Define a função render_dashboard que conterá todo o código do dashboard
def render_dashboard(backend_url):


    # ==========================
    # 🎯 MEDIDOR DE LATÊNCIA
    # ==========================
    st.subheader("📍 Medidor de Latência da Rede")

    # 📌 Entrada de dados (IP ou domínio e número de pacotes)
    host = st.text_input("Endereço IP ou domínio", value="8.8.8.8")
    count = st.number_input("Número de pacotes (ping)", min_value=1, max_value=50, value=3)

    if st.button("🔍 Medir Latência (Ping)"):
        try:
            response = requests.get(f"{backend_url}/api/metrics/ping", params={"host": host, "count": count})
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
            response = requests.get(f"{backend_url}/api/metrics/throughput")
            data = response.json()

            if data["success"]:
                st.markdown(f"**Tempo total:** {data['tempo_s']} segundos")
                st.markdown(f"**Dados transferidos:** {data['dados_kB']:,} KB")
                st.markdown(f"**Vazão estimada:** {data['throughput_kbps'] / 1000:.2f} Mbps")
            else:
                st.error("Erro ao medir throughput.")
        except Exception as e:
            st.error(f"Erro: {e}")


    st.subheader("🌐 Medidor de velocidade da Internet (via Speedtest)")

    if st.button("Iniciar medição Speedtest"):
        with st.spinner("Executando medição..."):
            try:
                res = requests.get(f"{backend_url}/api/metrics/speedtest")
                data = res.json()
                if data.get("success"):
                    st.success("Medição concluída com sucesso:")
                    st.markdown(f"- **Ping:** {data['ping_ms']} ms")
                    st.markdown(f"- **Download:** {data['download_mbps']} Mbps")
                    st.markdown(f"- **Upload:** {data['upload_mbps']} Mbps")
                else:
                    st.error(f"Erro ao medir: {data.get('error')}")
            except Exception as e:
                st.error(f"Erro de conexão: {e}")
