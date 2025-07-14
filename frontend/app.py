import streamlit as st
import pandas as pd
import sys
import os
import time
from datetime import datetime

# Adiciona o caminho do backend para importar o sniffer
backend_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'backend')
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Importa o sniffer diretamente
try:
    from ferramentas.sniffer.sniffer import PacketSniffer, get_network_interfaces
    SNIFFER_AVAILABLE = True
except ImportError as e:
    st.error(f"Erro ao importar sniffer: {e}")
    SNIFFER_AVAILABLE = False

# O st.set_page_config() deve ser a PRIMEIRA chamada do Streamlit no seu script principal.
st.set_page_config(page_title="Ferramentas de Rede", layout="centered")

# Estado global para resultados de captura
if 'capture_results' not in st.session_state:
    st.session_state.capture_results = {
        "is_capturing": False,
        "packets": [],
        "stats": {},
        "last_capture_time": None
    }

# --- Funções para simular as páginas ---
def homepage():
    st.title("🏠 Página Inicial")
    st.write("Bem-vindo ao sistema de Ferramentas de Rede!")
    st.info("📱 Aplicação totalmente integrada - sem backend externo necessário!")

def sniffer_page():
    st.title("🔍 Sniffer de Pacotes")
    st.markdown("Capture e analise o tráfego de rede em tempo real")
    
    # Verificação de disponibilidade
    if not SNIFFER_AVAILABLE:
        st.error("❌ Sniffer não disponível! Verifique se PyShark está instalado.")
        st.code("pip install pyshark")
        return
    
    # Layout em colunas para melhor organização
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("🌐 Configuração de Interface")
        
        # Botão para detectar interfaces
        if st.button("🔍 Detectar Interfaces", type="primary"):
            with st.spinner("Detectando interfaces de rede..."):
                try:
                    # Cria instância do sniffer para detectar interfaces
                    temp_sniffer = PacketSniffer()
                    interfaces = temp_sniffer.get_network_interfaces()
                    st.session_state.interfaces = interfaces
                    st.success(f"✅ {len(interfaces)} interfaces detectadas!")
                    
                    # Mostra as interfaces encontradas
                    if interfaces:
                        st.info("🌐 Interfaces disponíveis:")
                        for i, iface in enumerate(interfaces):
                            if isinstance(iface, dict):
                                name = iface.get('name', 'N/A')
                                iface_type = iface.get('type', 'N/A')
                                status = iface.get('status', 'N/A')
                                st.text(f"  {i+1}. {iface_type} {name} ({status})")
                            else:
                                st.text(f"  {i+1}. {str(iface)}")
                                
                except Exception as e:
                    st.error(f"❌ Erro ao detectar interfaces: {str(e)}")
                    st.session_state.interfaces = []
        
        # Seleção de interface
        if 'interfaces' in st.session_state and st.session_state.interfaces:
            interface_options = []
            for i, iface in enumerate(st.session_state.interfaces):
                if isinstance(iface, dict):
                    name = iface.get('name', f'Interface {i+1}')
                    iface_type = iface.get('type', 'N/A')
                    status = iface.get('status', 'N/A')
                    interface_options.append(f"{iface_type} {name} ({status})")
                else:
                    interface_options.append(f"{str(iface)}")
            
            selected_interface = st.selectbox("Escolha a interface:", interface_options)
            
            # Configurações de captura
            st.subheader("⚙️ Configurações de Captura")
            
            col_config1, col_config2 = st.columns(2)
            with col_config1:
                packet_count = st.number_input("Número de pacotes:", min_value=1, max_value=1000, value=50)
                timeout = st.number_input("Timeout (segundos):", min_value=1, max_value=300, value=30)
            
            with col_config2:
                use_filter = st.checkbox("Usar filtro BPF")
                bpf_filter = ""
                if use_filter:
                    bpf_filter = st.text_input("Filtro BPF:", placeholder="tcp port 80")
            
            # Controles de captura
            st.subheader("🎮 Controles")
            
            col_start, col_stop = st.columns(2)
            
            with col_start:
                if st.button("🟢 Iniciar Captura", type="primary"):
                    try:
                        # Verifica se há interface selecionada
                        if not selected_interface:
                            st.error("❌ Selecione uma interface primeiro!")
                            return
                        
                        # Extrai nome da interface a partir do texto selecionado
                        interface_name = None
                        for iface in st.session_state.interfaces:
                            if isinstance(iface, dict):
                                name = iface.get('name', '')
                                iface_type = iface.get('type', '')
                                status = iface.get('status', '')
                                display_text = f"{iface_type} {name} ({status})"
                                
                                if display_text == selected_interface:
                                    interface_name = iface.get('id', name)
                                    break
                        
                        if not interface_name:
                            st.error("❌ Não foi possível identificar a interface selecionada!")
                            return
                        
                        # Configura captura
                        st.session_state.capture_results["is_capturing"] = True
                        
                        with st.spinner("Capturando pacotes..."):
                            try:
                                # Cria sniffer
                                sniffer = PacketSniffer()
                                
                                # Executa captura diretamente (sem thread)
                                result = sniffer.start_capture(
                                    interface=interface_name,
                                    packet_count=packet_count,
                                    timeout=timeout,
                                    bpf_filter=bpf_filter if use_filter else None
                                )
                                
                                # Atualiza resultados
                                st.session_state.capture_results.update({
                                    "is_capturing": False,
                                    "packets": result.get('packets', []),
                                    "stats": result.get('stats', {}),
                                    "last_capture_time": datetime.now()
                                })
                                
                                packets_count = len(result.get('packets', []))
                                if result.get('demo_mode'):
                                    st.info(f"ℹ️ Modo demonstração - {packets_count} pacotes simulados")
                                elif result.get('timeout'):
                                    st.warning(f"⚠️ Timeout na captura - {packets_count} pacotes capturados")
                                else:
                                    st.success(f"✅ Captura concluída! {packets_count} pacotes capturados")
                                    
                                st.rerun()
                                
                            except Exception as e:
                                st.session_state.capture_results.update({
                                    "is_capturing": False,
                                    "error": str(e)
                                })
                                st.error(f"❌ Erro na captura: {str(e)}")
                            
                    except Exception as e:
                        st.error(f"❌ Erro ao configurar captura: {str(e)}")
                        st.session_state.capture_results["is_capturing"] = False
            
            with col_stop:
                if st.button("🔴 Parar Captura"):
                    st.session_state.capture_results["is_capturing"] = False
                    st.success("🔴 Captura interrompida!")
    
    with col2:
        st.subheader("📊 Status da Captura")
        
        # Status em tempo real
        if st.session_state.capture_results["is_capturing"]:
            st.warning("� Captura sendo configurada...")
        else:
            st.success("� Pronto para capturar")
        
        # Métricas da última captura
        if st.session_state.capture_results.get("last_capture_time"):
            st.metric("Última captura", 
                     st.session_state.capture_results["last_capture_time"].strftime("%H:%M:%S"))
        
        if st.session_state.capture_results.get("packets"):
            st.metric("Pacotes capturados", len(st.session_state.capture_results["packets"]))
    
    # Resultados da captura
    if st.session_state.capture_results.get("packets"):
        st.subheader("📋 Resultados da Captura")
        
        packets = st.session_state.capture_results["packets"]
        
        if packets:
            # Estatísticas gerais
            st.success(f"✅ {len(packets)} pacotes capturados")
            
            # Tabela de pacotes
            try:
                packet_data = []
                for i, packet in enumerate(packets[:100]):  # Limitar a 100 para performance
                    packet_info = {
                        'ID': i + 1,
                        'Timestamp': packet.get('timestamp', 'N/A'),
                        'Protocolo': packet.get('protocol', 'N/A'),
                        'Origem': packet.get('src', 'N/A'),
                        'Destino': packet.get('dst', 'N/A'),
                        'Tamanho': packet.get('length', 'N/A')
                    }
                    packet_data.append(packet_info)
                
                if packet_data:
                    df = pd.DataFrame(packet_data)
                    st.dataframe(df, use_container_width=True)
                    
                    # Estatísticas por protocolo
                    protocols = [p.get('protocol', 'Desconhecido') for p in packets]
                    protocol_counts = pd.Series(protocols).value_counts()
                    
                    st.subheader("📈 Estatísticas por Protocolo")
                    col_chart1, col_chart2 = st.columns(2)
                    
                    with col_chart1:
                        st.bar_chart(protocol_counts)
                    
                    with col_chart2:
                        for protocol, count in protocol_counts.head(5).items():
                            st.metric(str(protocol), count)
                
            except Exception as e:
                st.error(f"❌ Erro ao processar dados: {str(e)}")
        
        # Botão para limpar resultados
        if st.button("🗑️ Limpar Resultados"):
            st.session_state.capture_results = {
                "is_capturing": False,
                "packets": [],
                "stats": {},
                "last_capture_time": None
            }
            st.success("✅ Resultados limpos!")
            st.rerun()
    
    # Erro se houver
    if 'error' in st.session_state.capture_results:
        st.error(f"❌ Erro na captura: {st.session_state.capture_results['error']}")

def dashboard_page():
    """
    Página do dashboard com overview das ferramentas
    """
    st.title("📊 Dashboard - Ferramentas de Rede")
    st.markdown("**Visão geral do sistema e ferramentas disponíveis**")
    
    # Métricas principais
    st.subheader("📈 Status do Sistema")
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Sistema", "🟢 Online", delta="Funcionando")
    
    with col2:
        st.metric("Sniffer", "✅ Disponível" if SNIFFER_AVAILABLE else "❌ Indisponível")
    
    with col3:
        total_interfaces = len(getattr(st.session_state, 'interfaces', []))
        st.metric("Interfaces", total_interfaces)
    
    with col4:
        total_packets = len(st.session_state.capture_results.get("packets", []))
        st.metric("Pacotes Capturados", total_packets)
    
    # Seção de ferramentas disponíveis
    st.subheader("🛠️ Ferramentas Disponíveis")
    
    tool_col1, tool_col2 = st.columns(2)
    
    with tool_col1:
        st.info("🔍 **Sniffer de Pacotes**")
        st.write("Capture e analise tráfego de rede em tempo real")
    
    with tool_col2:
        st.info("📈 **Speed Test**")
        st.write("Teste a velocidade da sua conexão")
    
    # Histórico recente
    if st.session_state.capture_results.get("last_capture_time"):
        st.subheader("📋 Última Atividade")
        
        last_time = st.session_state.capture_results["last_capture_time"]
        packets = st.session_state.capture_results.get("packets", [])
        
        st.success(f"✅ Última captura: {last_time.strftime('%H:%M:%S')} - {len(packets)} pacotes")
        
        # Resumo rápido dos protocolos
        if packets:
            protocols = [p.get('protocol', 'Desconhecido') for p in packets]
            protocol_counts = pd.Series(protocols).value_counts().head(3)
            
            st.write("**Top 3 Protocolos:**")
            for protocol, count in protocol_counts.items():
                st.text(f"• {protocol}: {count} pacotes")
    
    # Ajuda rápida
    st.subheader("💡 Ajuda Rápida")
    
    with st.expander("Como usar o Sniffer"):
        st.markdown("""
        1. **Vá para a página Sniffer** 🔍
        2. **Detecte interfaces** disponíveis
        3. **Configure** filtros se necessário
        4. **Inicie a captura** e monitore em tempo real
        5. **Analise os resultados** na tabela e gráficos
        """)
    
    with st.expander("Filtros BPF Úteis"):
        st.code("""
        tcp port 80          # Tráfego HTTP
        tcp port 443         # Tráfego HTTPS
        udp port 53          # DNS
        icmp                 # Ping
        tcp and port 22      # SSH
        """)
    
    # Status das interfaces
    if hasattr(st.session_state, 'interfaces') and st.session_state.interfaces:
        st.subheader("🌐 Interfaces Disponíveis")
        
        for i, iface in enumerate(st.session_state.interfaces[:5]):  # Mostrar só as 5 primeiras
            if isinstance(iface, dict):
                name = iface.get('name', f'Interface {i+1}')
                status = "🟢 Ativa" if iface.get('status') else "⚪ Detectada"
                st.text(f"• {name} - {status}")
            else:
                st.text(f"• {str(iface)}")
        
        if len(st.session_state.interfaces) > 5:
            st.text(f"... e mais {len(st.session_state.interfaces) - 5} interfaces")
    else:
        st.info("💡 Vá para a página Sniffer para detectar interfaces de rede")

def speedtest_page():
    st.title("📊 Speed Test")
    st.write("Teste de velocidade da sua conexão.")
    st.info("🚧 Speed Test em desenvolvimento")
    
    # Placeholder para speedtest
    if st.button("🚀 Executar Speed Test"):
        st.info("Funcionalidade em desenvolvimento. Em breve disponível!")

def about_page():
    st.title("ℹ️ Sobre o Projeto")
    st.write("**Ferramentas de Redes** - Um conjunto completo de utilitários para análise e monitoramento de rede.")
    
    st.markdown("""
    ### 🚀 Funcionalidades:
    - **🔍 Sniffer de Pacotes**: Captura e análise de tráfego de rede em tempo real
    - **📊 Dashboard**: Visualização centralizada de métricas e status
    - **📈 Speed Test**: Teste de velocidade da conexão
    
    ### 🛠️ Tecnologias:
    - **Frontend**: Streamlit
    - **Captura de Pacotes**: PyShark
    - **Visualização**: Pandas, Streamlit Charts
    
    ### 📝 Como usar:
    1. Acesse o Dashboard para ver o status geral
    2. Use o Sniffer para capturar e analisar pacotes
    3. Teste a velocidade da sua conexão no Speed Test
    """)

# --- Lógica de Navegação na Barra Lateral ---
st.sidebar.title("🌐 Navegação")
st.sidebar.markdown("---")
page = st.sidebar.radio("Escolha uma página:", ["🏠 Início", "📊 Dashboard", "🔍 Sniffer", "📈 SpeedTest", "ℹ️ Sobre"])

# Navegação principal
if page == "🏠 Início":
    homepage()
elif page == "📊 Dashboard":
    dashboard_page()
elif page == "🔍 Sniffer":
    sniffer_page()
elif page == "📈 SpeedTest":
    speedtest_page()
elif page == "ℹ️ Sobre":
    about_page()

# Rodapé informativo na sidebar
st.sidebar.markdown("---")
st.sidebar.markdown("### 🔗 Status do Sistema")

# Status da aplicação integrada
st.sidebar.success("✅ Aplicação Integrada")
st.sidebar.info("💡 Sniffer totalmente integrado - sem backend externo necessário")

# Informações do projeto
st.sidebar.markdown("---")
st.sidebar.markdown("**Ferramentas de Redes v2.0**")
st.sidebar.markdown("*Versão totalmente integrada*")
