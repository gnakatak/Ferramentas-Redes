import streamlit as st
import requests
import time
import pandas as pd
import json
from datetime import datetime

BACKEND_URL = "http://localhost:5000"

# Configuração da página
st.set_page_config(
    page_title="Ferramentas de Redes",
    page_icon="🌐",
    layout="wide"
)

# Sidebar para navegação
st.sidebar.title("🌐 Ferramentas de Redes")
page = st.sidebar.selectbox(
    "Escolha uma ferramenta:",
    ["Home", "Sniffer de Pacotes", "Firewall", "Métricas", "Mini Chat"]
)

if page == "Home":
    st.title("🌐 Ferramentas de Redes")
    st.markdown("""
    ## Bem-vindo ao conjunto de ferramentas de redes!
    
    ### 🔍 Sniffer de Pacotes
    Capture e analise tráfego de rede em tempo real
    
    ### 🛡️ Firewall
    Configure regras de firewall
    
    ### 📊 Métricas
    Monitore métricas de rede (ping, throughput)
    
    ### 💬 Mini Chat
    Sistema de chat simples
    """)
    
    # Teste de conectividade
    st.subheader("🔗 Teste de Conectividade com Backend")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("Testar Conexão"):
            try:
                response = requests.get(f"{BACKEND_URL}/api/hello")
                data = response.json()
                st.success(f"✅ Backend conectado: {data}") 
            except Exception as e:
                st.error(f"❌ Erro ao conectar com backend: {e}")
    
    with col2:
        if st.button("Testar Despedida"):
            try: 
                response = requests.get(f"{BACKEND_URL}/api/goodbye")
                data = response.json()
                st.success(f"✅ {data['message']}")
            except Exception as e:
                st.error(f"❌ Erro ao conectar com backend: {e}")

elif page == "Sniffer de Pacotes":
    st.title("🔍 Sniffer de Pacotes")
    
    # Status do sniffer
    st.subheader("📊 Status da Captura")
    
    # Container para atualização automática
    status_container = st.container()
    
    # Controles do sniffer
    st.subheader("⚙️ Controles")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        # Botão para listar interfaces
        if st.button("🔍 Listar Interfaces"):
            try:
                response = requests.get(f"{BACKEND_URL}/api/sniffer/interfaces")
                data = response.json()
                if data["success"]:
                    st.session_state.interfaces = data["interfaces"]
                    st.success("Interfaces carregadas!")
                else:
                    st.error(f"Erro: {data.get('error', 'Erro desconhecido')}")
            except Exception as e:
                st.error(f"Erro ao conectar: {e}")
    
    # Configurações de captura
    st.subheader("🛠️ Configurações de Captura")
    
    # Interface selecionada
    interfaces_available = getattr(st.session_state, 'interfaces', [])
    if interfaces_available:
        interface_names = [iface['name'] for iface in interfaces_available]
        selected_interface = st.selectbox("Interface:", ["Auto"] + interface_names)
    else:
        selected_interface = st.selectbox("Interface:", ["Auto"])
    
    # Filtros
    filter_preset = st.selectbox(
        "Filtro Pré-definido:",
        ["Nenhum", "HTTP (port 80)", "HTTPS (port 443)", "DNS (port 53)", "TCP", "UDP", "ICMP"]
    )
    
    custom_filter = st.text_input("Filtro Personalizado (BPF):", placeholder="Ex: tcp port 80")
    
    # Determina o filtro final
    filter_expr = None
    if filter_preset != "Nenhum":
        filter_map = {
            "HTTP (port 80)": "tcp port 80",
            "HTTPS (port 443)": "tcp port 443", 
            "DNS (port 53)": "udp port 53",
            "TCP": "tcp",
            "UDP": "udp",
            "ICMP": "icmp"
        }
        filter_expr = filter_map.get(filter_preset)
    
    if custom_filter:
        filter_expr = custom_filter
    
    # Configurações avançadas
    col1, col2 = st.columns(2)
    with col1:
        packet_count = st.number_input("Máximo de pacotes (0 = ilimitado):", min_value=0, value=100)
    with col2:
        timeout = st.number_input("Timeout (segundos, 0 = sem timeout):", min_value=0, value=30)
    
    # Botões de controle
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Iniciar Captura"):
            try:
                payload = {
                    "interface": selected_interface if selected_interface != "Auto" else None,
                    "filter": filter_expr,
                    "packet_count": packet_count if packet_count > 0 else 0,
                    "timeout": timeout if timeout > 0 else None
                }
                
                response = requests.post(
                    f"{BACKEND_URL}/api/sniffer/start",
                    json=payload
                )
                data = response.json()
                
                if data["success"]:
                    st.success("✅ Captura iniciada!")
                    st.session_state.sniffer_running = True
                else:
                    st.error(f"❌ Erro: {data.get('error', 'Erro desconhecido')}")
            except Exception as e:
                st.error(f"❌ Erro ao iniciar captura: {e}")
    
    with col2:
        if st.button("⏹️ Parar Captura"):
            try:
                response = requests.post(f"{BACKEND_URL}/api/sniffer/stop")
                data = response.json()
                
                if data["success"]:
                    st.success("✅ Captura finalizada!")
                    st.session_state.sniffer_running = False
                else:
                    st.error(f"❌ Erro: {data.get('error', 'Erro desconhecido')}")
            except Exception as e:
                st.error(f"❌ Erro ao parar captura: {e}")
    
    with col3:
        if st.button("🔄 Atualizar Status"):
            st.rerun()
    
    # Exibe status atual
    try:
        response = requests.get(f"{BACKEND_URL}/api/sniffer/status")
        data = response.json()
        
        if data["success"]:
            stats = data["statistics"]
            
            with status_container:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    st.metric("Status", "🟢 Ativo" if stats.get('is_running') else "🔴 Parado")
                
                with col2:
                    st.metric("Total de Pacotes", stats.get('total_packets', 0))
                
                with col3:
                    st.metric("Duração (s)", f"{stats.get('duration', 0):.1f}")
                
                with col4:
                    st.metric("Pacotes/s", f"{stats.get('packets_per_second', 0):.1f}")
                
                # Gráfico de protocolos
                protocols = stats.get('protocols', {})
                if protocols:
                    st.subheader("📊 Distribuição de Protocolos")
                    df_protocols = pd.DataFrame(
                        list(protocols.items()),
                        columns=['Protocolo', 'Quantidade']
                    )
                    st.bar_chart(df_protocols.set_index('Protocolo'))
    
    except Exception as e:
        with status_container:
            st.error(f"❌ Erro ao obter status: {e}")
    
    # Exibir pacotes capturados
    st.subheader("📦 Pacotes Capturados")
    
    limit = st.slider("Número de pacotes a exibir:", 1, 100, 20)
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("📥 Carregar Pacotes"):
            try:
                response = requests.get(f"{BACKEND_URL}/api/sniffer/packets?limit={limit}")
                data = response.json()
                
                if data["success"]:
                    packets = data["packets"]
                    st.session_state.packets = packets
                    st.success(f"✅ {len(packets)} pacotes carregados!")
                else:
                    st.error(f"❌ Erro: {data.get('error', 'Erro desconhecido')}")
            except Exception as e:
                st.error(f"❌ Erro ao carregar pacotes: {e}")
    
    with col2:
        if st.button("💾 Exportar Pacotes"):
            try:
                response = requests.post(
                    f"{BACKEND_URL}/api/sniffer/export",
                    json={"format": "json"}
                )
                data = response.json()
                
                if data["success"]:
                    st.success(f"✅ {data['message']}")
                else:
                    st.error(f"❌ Erro: {data.get('error', 'Erro desconhecido')}")
            except Exception as e:
                st.error(f"❌ Erro ao exportar: {e}")
    
    # Exibe tabela de pacotes
    packets = getattr(st.session_state, 'packets', [])
    if packets:
        # Converte para DataFrame
        df_packets = pd.DataFrame(packets)
        
        # Formata timestamp
        if 'timestamp' in df_packets.columns:
            df_packets['timestamp'] = pd.to_datetime(df_packets['timestamp']).dt.strftime('%H:%M:%S.%f').str[:-3]
        
        # Seleciona colunas para exibir
        display_columns = ['timestamp', 'protocol', 'src_ip', 'dst_ip', 'src_port', 'dst_port', 'length']
        available_columns = [col for col in display_columns if col in df_packets.columns]
        
        st.dataframe(
            df_packets[available_columns],
            use_container_width=True,
            height=400
        )
        
        # Análises especiais
        st.subheader("🔍 Análises Especiais")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🌐 Analisar HTTP"):
                try:
                    response = requests.get(f"{BACKEND_URL}/api/sniffer/analyze/http")
                    data = response.json()
                    if data["success"]:
                        st.write(f"📊 Pacotes HTTP: {data['count']}")
                        if data['http_packets']:
                            st.dataframe(pd.DataFrame(data['http_packets']))
                except Exception as e:
                    st.error(f"Erro: {e}")
        
        with col2:
            if st.button("🔍 Analisar DNS"):
                try:
                    response = requests.get(f"{BACKEND_URL}/api/sniffer/analyze/dns")
                    data = response.json()
                    if data["success"]:
                        st.write(f"📊 Pacotes DNS: {data['count']}")
                        if data['dns_packets']:
                            st.dataframe(pd.DataFrame(data['dns_packets']))
                except Exception as e:
                    st.error(f"Erro: {e}")
        
        with col3:
            if st.button("📈 Top Talkers"):
                try:
                    response = requests.get(f"{BACKEND_URL}/api/sniffer/analyze/top-talkers?limit=5")
                    data = response.json()
                    if data["success"]:
                        st.write("📊 Top 5 IPs por tráfego:")
                        df_top = pd.DataFrame(data['top_talkers'])
                        if not df_top.empty:
                            st.dataframe(df_top)
                except Exception as e:
                    st.error(f"Erro: {e}")
    
    else:
        st.info("📝 Nenhum pacote carregado. Clique em 'Carregar Pacotes' para visualizar.")

elif page == "Firewall":
    st.title("🛡️ Firewall")
    st.info("🚧 Em desenvolvimento")

elif page == "Métricas":
    st.title("📊 Métricas de Rede")
    st.info("🚧 Em desenvolvimento")

elif page == "Mini Chat":
    st.title("💬 Mini Chat")
    st.info("🚧 Em desenvolvimento")
