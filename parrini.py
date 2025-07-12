import streamlit as st
st.set_page_config(page_title="Monitor de Internet", layout="centered")

import pandas as pd
import speedtest
from datetime import datetime
import threading
import time
import os

# ---------- Inicialização de sessão ----------
if "dados" not in st.session_state:
    st.session_state.dados = {
        "DataHora": [],
        "Download": [],
        "Upload": [],
        "Ping": []
    }

if "monitorando" not in st.session_state:
    st.session_state.monitorando = False

# ---------- Função de teste ----------
def testar_velocidade():
    try:
        stt = speedtest.Speedtest()
        stt.get_best_server()
        download = stt.download() / 1_000_000
        upload = stt.upload() / 1_000_000
        ping = stt.results.ping
        agora = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        novo_dado = pd.DataFrame({
            "DataHora": [agora],
            "Download": [download],
            "Upload": [upload],
            "Ping": [ping]
        })

        for col in novo_dado.columns:
            st.session_state.dados[col].append(novo_dado[col].values[0])

        # Salva em CSV
        arquivo = "speedtest_log.csv"
        if os.path.exists(arquivo):
            historico = pd.read_csv(arquivo)
            historico = pd.concat([historico, novo_dado], ignore_index=True)
        else:
            historico = novo_dado

        historico.to_csv(arquivo, index=False)

    except Exception as e:
        st.error(f"Erro ao testar velocidade: {e}")
        raise e

# ---------- Monitoramento automático ----------
def iniciar_monitoramento(intervalo):
    while True:
        if not st.session_state.get("monitorando", False):
            break
        testar_velocidade()
        time.sleep(intervalo)


# ---------- Título e teste manual ----------
st.title("📡 Monitor de Velocidade da Internet")

if st.button("Iniciar Teste Manual"):
    st.write("Executando teste...")
    testar_velocidade()
    st.success("Teste concluído!")

# ---------- Monitoramento contínuo ----------
st.subheader("🔁 Monitoramento Contínuo")
intervalo = st.number_input("Intervalo (segundos) entre testes", min_value=10, value=60, step=10)

if not st.session_state.monitorando:
    if st.button("▶️ Iniciar Monitoramento Contínuo"):
        st.session_state.monitorando = True
        threading.Thread(target=iniciar_monitoramento, args=(intervalo,), daemon=True).start()
        st.success("Monitoramento iniciado.")
else:
    if st.button("⏹️ Parar Monitoramento"):
        st.session_state.monitorando = False
        st.warning("Monitoramento interrompido.")

# ---------- Visualização de resultados ----------
st.subheader("📊 Resultados")

arquivo_csv = "speedtest_log.csv"
df = pd.DataFrame(st.session_state.dados)
if os.path.exists(arquivo_csv):
    df = pd.read_csv(arquivo_csv)

if not df.empty:
    df["DataHora"] = pd.to_datetime(df["DataHora"], errors="coerce")
    df = df.dropna(subset=["DataHora"])

    st.dataframe(df.tail(10))

    st.write("📈 Gráfico de Download/Upload")
    st.line_chart(df.set_index("DataHora")[["Download", "Upload"]])

    st.write("📉 Gráfico de Ping")
    st.line_chart(df.set_index("DataHora")[["Ping"]])

    csv_data = df.to_csv(index=False).encode("utf-8")
    st.download_button("📥 Baixar CSV", data=csv_data, file_name="speedtest_log.csv", mime="text/csv")
else:
    st.info("Nenhum teste realizado ainda.")
