import streamlit as st
import pandas as pd
import speedtest
from datetime import datetime
import time
import logging

# Configurar logging para depuração
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def speedtest_teste():
    # Inicialização de sessão
    if "dados" not in st.session_state:
        st.session_state.dados = {
            "DataHora": [],
            "Download": [],
            "Upload": [],
            "Ping": []
        }

    if "monitorando" not in st.session_state:
        st.session_state.monitorando = False

    # Função de teste com tratamento de erros
    def testar_velocidade():
        try:
            with st.spinner("Realizando teste de velocidade..."):
                stt = speedtest.Speedtest(timeout=30)
                logger.info("Selecionando melhor servidor...")
                stt.get_best_server()
                logger.info(f"Servidor selecionado: {stt.results.server['host']}")
                
                logger.info("Testando download...")
                download = stt.download() / 1_000_000
                logger.info("Testando upload...")
                upload = stt.upload() / 1_000_000
                logger.info("Testando ping...")
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

                logger.info(f"Teste concluído: Download={download:.1f} Mbps, Upload={upload:.1f} Mbps, Ping={ping:.0f} ms")
                return True

        except Exception as e:
            logger.error(f"Erro no teste de velocidade: {str(e)}")
            st.error(f"Erro ao testar velocidade: {str(e)}")
            return False

    # Título e teste manual
    st.title("📡 Monitor de Velocidade da Internet")

    col_teste, col_limpar = st.columns([3, 1])

    with col_teste:
        if st.button("🚀 Iniciar Teste Manual", use_container_width=True):
            st.write("Executando teste...")
            if testar_velocidade():
                st.success("Teste concluído!")

    with col_limpar:
        if st.button("🗑️ Limpar Dados", use_container_width=True):
            st.session_state.dados = {
                "DataHora": [],
                "Download": [],
                "Upload": [],
                "Ping": []
            }
            st.success("Dados limpos!")
            st.rerun()

    # Monitoramento contínuo
    st.subheader("🔁 Monitoramento Contínuo")

    if "ultimo_teste" not in st.session_state:
        st.session_state.ultimo_teste = None

    if "proximo_teste" not in st.session_state:
        st.session_state.proximo_teste = None

    intervalo = st.number_input("Intervalo (segundos) entre testes", min_value=10, value=10, step=10)

    col1, col2 = st.columns(2)

    with col1:
        if not st.session_state.monitorando:
            if st.button("▶️ Iniciar Monitoramento Contínuo"):
                st.session_state.monitorando = True
                st.session_state.ultimo_teste = datetime.now()
                st.session_state.proximo_teste = st.session_state.ultimo_teste + pd.Timedelta(seconds=intervalo)
                st.success("Monitoramento iniciado.")
                st.rerun()
        else:
            if st.button("⏹️ Parar Monitoramento"):
                st.session_state.monitorando = False
                st.session_state.ultimo_teste = None
                st.session_state.proximo_teste = None
                st.warning("Monitoramento interrompido.")
                st.rerun()

    with col2:
        if st.session_state.monitorando:
            agora = datetime.now()
            if st.session_state.proximo_teste and agora >= st.session_state.proximo_teste:
                if testar_velocidade():
                    st.session_state.ultimo_teste = agora
                    st.session_state.proximo_teste = agora + pd.Timedelta(seconds=intervalo)
                    st.success(f"Teste automático realizado às {agora.strftime('%H:%M:%S')}")
                    st.rerun()
            
            if st.session_state.proximo_teste:
                tempo_restante = (st.session_state.proximo_teste - agora).total_seconds()
                if tempo_restante > 0:
                    st.info(f"⏰ Próximo teste em: {int(tempo_restante)}s")
                    if st.button("🔄 Atualizar Status"):
                        st.rerun()
                else:
                    st.info("⏰ Executando teste...")
            
            st.info("💡 Dica: A página atualizará automaticamente quando for hora do próximo teste.")
            st.caption(f"Status: Monitoramento ativo - Última verificação: {agora.strftime('%H:%M:%S')}")
            
            if st.session_state.proximo_teste:
                tempo_para_teste = (st.session_state.proximo_teste - agora).total_seconds()
                if 0 < tempo_para_teste <= 10:
                    time.sleep(2)
                    st.rerun()

    # Visualização de resultados
    st.subheader("📊 Resultados")

    df = pd.DataFrame(st.session_state.dados)

    if not df.empty:
        df["DataHora"] = pd.to_datetime(df["DataHora"], errors="coerce")
        df = df.dropna(subset=["DataHora"])

        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric(
                label="📈 Download Médio", 
                value=f"{df['Download'].mean():.1f} Mbps",
                delta=f"Max: {df['Download'].max():.1f}"
            )
        
        with col2:
            st.metric(
                label="📤 Upload Médio", 
                value=f"{df['Upload'].mean():.1f} Mbps",
                delta=f"Max: {df['Upload'].max():.1f}"
            )
        
        with col3:
            st.metric(
                label="🏓 Ping Médio", 
                value=f"{df['Ping'].mean():.0f} ms",
                delta=f"Min: {df['Ping'].min():.0f}"
            )

        st.dataframe(df.tail(10), use_container_width=True)

        st.write("📈 Gráfico de Download/Upload")
        st.line_chart(df.set_index("DataHora")[["Download", "Upload"]])

        st.write("📉 Gráfico de Ping")
        st.line_chart(df.set_index("DataHora")[["Ping"]])

        csv_data = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "📥 Baixar Dados da Sessão (CSV)", 
            data=csv_data, 
            file_name=f"speedtest_session_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv", 
            mime="text/csv",
            help="⚠️ Dados são apenas da sessão atual e serão perdidos ao recarregar a página"
        )
    else:
        st.info("Nenhum teste realizado ainda.")
        st.warning("💡 **Nota**: Os dados são armazenados apenas durante esta sessão e serão perdidos ao recarregar a página.")