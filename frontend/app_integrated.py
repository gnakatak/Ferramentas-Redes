import streamlit as st
import sys
import os
import time
import pandas as pd
import threading
from datetime import datetime

# Adiciona o diretório backend ao path para importar o sniffer
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'backend'))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

# Import do módulo sniffer
try:
    from ferramentas.sniffer.sniffer import (
        PacketSniffer, get_network_interfaces, analyze_http_traffic, 
        analyze_dns_traffic, get_top_talkers, check_admin_privileges,
        get_network_interfaces_detailed, format_packet_info
    )
    SNIFFER_AVAILABLE = True
except ImportError as e:
    st.error(f"❌ Erro ao importar o módulo sniffer: {e}")
    st.error("Certifique-se de que o PyShark está instalado: pip install pyshark")
    SNIFFER_AVAILABLE = False
    
    # Cria funções placeholder para evitar erros
    class PacketSniffer:
        def __init__(self, interface=None, filter_expr=None):
            pass
        def start_capture(self, packet_count=0, timeout=None):
            return {"error": "Sniffer não disponível"}
        def stop_capture(self):
            pass
        def get_statistics(self):
            return {"total_packets": 0, "duration": 0, "packets_per_second": 0, "protocols": {}, "is_running": False}
        def get_packets(self, limit=None):
            return []
        def export_packets(self, format='json', filename=None):
            return {"error": "Sniffer não disponível"}
    
    def get_network_interfaces():
        return [{'name': 'any', 'ip_addresses': []}]
    
    def get_network_interfaces_detailed():
        return [{'name': 'any', 'display_name': 'Não disponível', 'status': 'Error', 'ip_addresses': []}]
    
    def analyze_http_traffic(packets):
        return []
    
    def analyze_dns_traffic(packets):
        return []
    
    def get_top_talkers(packets, limit=10):
        return []
    
    def check_admin_privileges():
        return False
    
    def format_packet_info(packet):
        return "Sniffer não disponível"

# Configuração da página
st.set_page_config(
    page_title="Ferramentas de Redes - Integrado",
    page_icon="🌐",
    layout="wide"
)

# Inicializa o sniffer no session_state
if 'sniffer' not in st.session_state:
    st.session_state.sniffer = None
if 'interfaces' not in st.session_state:
    st.session_state.interfaces = []
if 'packets' not in st.session_state:
    st.session_state.packets = []

# Sidebar para navegação
st.sidebar.title("🛠️ Ferramentas Disponíveis")
tool = st.sidebar.radio(
    "Selecione uma ferramenta:",
    [
        "🏠 Home",
        "📡 Sniffer de Pacotes",
        "🔍 Port Scanner",
        "🌐 Network Scanner",
        "📶 Ping & Traceroute",
        "📊 Bandwidth Monitor",
        "📋 Network Info",
        "⚙️ Configurações"
    ]
)

if tool == "🏠 Home":
    st.header("🏠 Dashboard - Ferramentas de Redes")
    
    # Verificação de disponibilidade
    if SNIFFER_AVAILABLE:
        st.success("✅ Sniffer disponível e pronto para uso!")
    else:
        st.error("❌ Sniffer não disponível. Verifique as dependências.")
        st.code("pip install pyshark")
    
    st.markdown("""
    ## Bem-vindo ao sniffer de pacotes integrado!
    
    ### ✨ **Vantagens desta versão:**
    - 🚀 **Mais simples**: Tudo em um só lugar
    - 📦 **Menos dependências**: Apenas `streamlit` + `pyshark`
    - ⚡ **Mais rápido**: Sem comunicação HTTP
    - 🎯 **Focado**: Apenas no sniffer
    
    ### 🔍 **Funcionalidades disponíveis:**
    - Captura de pacotes em tempo real
    - Análise de protocolos (TCP, UDP, ICMP, HTTP, DNS)
    - Filtros personalizados (BPF)
    - Estatísticas em tempo real
    - Exportação de dados
    - Análises especializadas
    
    ### 📋 **Dependências mínimas:**
    ```
    streamlit
    pyshark
    pandas
    ```
    
    ---
    **👈 Use o menu lateral para navegar para o Sniffer de Pacotes**
    """)

elif tool == "📡 Sniffer de Pacotes":
    st.header("📡 Sniffer de Pacotes")
    
    # Verifica se o sniffer está disponível
    if not SNIFFER_AVAILABLE:
        st.error("❌ Sniffer não está disponível!")
        st.markdown("""
        ### 🔧 Como resolver:
        
        1. **Instale o PyShark:**
        ```bash
        pip install pyshark
        ```
        
        2. **Windows - Instale Npcap:**
        - Baixe: https://nmap.org/npcap/
        - Marque "Install Npcap in WinPcap API-compatible Mode"
        
        3. **Execute como Administrador (Windows) ou com sudo (Linux/Mac)**
        
        4. **Reinicie a aplicação**
        """)
        st.stop()
    
    # Verificação de privilégios
    st.subheader("🔐 Verificação de Privilégios")
    
    try:
        is_admin = check_admin_privileges()
        if is_admin:
            st.success("✅ Executando com privilégios administrativos")
        else:
            st.warning("⚠️ NÃO está executando como administrador")
            st.info("""
            **Para capturar pacotes, você precisa de privilégios administrativos:**
            - **Windows:** Execute como Administrador
            - **Linux/Mac:** Use `sudo streamlit run frontend/app_integrated.py`
            """)
    except Exception as e:
        st.error(f"❌ Erro ao verificar privilégios: {e}")
    
    # Status do sniffer
    st.subheader("📊 Status da Captura")
    
    # Container para status
    status_container = st.container()
    
    # Seção de interfaces
    st.subheader("🔌 Interfaces de Rede")
    
    col1, col2 = st.columns(2)
    
    with col1:
        if st.button("🔍 Detectar Interfaces"):
            with st.spinner("Detectando interfaces..."):
                try:
                    # Usa a versão mais detalhada
                    interfaces = get_network_interfaces_detailed()
                    st.session_state.interfaces = interfaces
                    if interfaces:
                        st.success(f"✅ {len(interfaces)} interfaces encontradas!")
                    else:
                        st.warning("⚠️ Nenhuma interface detectada. Verifique privilégios administrativos.")
                except Exception as e:
                    st.error(f"❌ Erro ao detectar interfaces: {e}")
                    # Fallback para método original
                    try:
                        interfaces = get_network_interfaces()
                        st.session_state.interfaces = interfaces
                        st.info(f"ℹ️ Fallback: {len(interfaces)} interfaces detectadas")
                    except Exception as e2:
                        st.error(f"❌ Erro no fallback: {e2}")
    
    with col2:
        if st.session_state.interfaces:
            st.success(f"📡 {len(st.session_state.interfaces)} interfaces disponíveis")
        else:
            st.info("🔍 Clique em 'Detectar Interfaces' para começar")
    
    # Exibe interfaces encontradas
    if st.session_state.interfaces:
        with st.expander("📋 Detalhes das Interfaces", expanded=False):
            for i, interface in enumerate(st.session_state.interfaces):
                if isinstance(interface, dict):
                    st.write(f"**{i+1}. {interface.get('name', 'Unknown')}**")
                    if 'ip_addresses' in interface and interface['ip_addresses']:
                        st.write("   📍 Endereços IP:")
                        for addr in interface.get('ip_addresses', []):
                            if isinstance(addr, dict):
                                # Formato detalhado com type e address
                                st.write(f"   - {addr.get('type', 'IP')}: {addr.get('address', 'N/A')}")
                            else:
                                # Formato simples (string do IP)
                                st.write(f"   - IP: {addr}")
                    else:
                        st.write("   - Sem endereços IP configurados")
                else:
                    # Formato antigo (string)
                    st.write(f"**{i+1}. {interface}**")
    
    # Configurações de captura
    st.subheader("🛠️ Configurações de Captura")
    
    # Interface selecionada - sempre define a variável
    selected_interface = "Auto (detectar automaticamente)"  # Valor padrão
    
    if st.session_state.interfaces:
        interface_names = []
        for iface in st.session_state.interfaces:
            if isinstance(iface, dict):
                interface_names.append(iface.get('name', str(iface)))
            else:
                interface_names.append(str(iface))
        selected_interface = st.selectbox("Interface:", ["Auto (detectar automaticamente)"] + interface_names)
    else:
        selected_interface = st.selectbox("Interface:", ["Auto (detectar automaticamente)"])
    
    # Filtros
    col1, col2 = st.columns(2)
    
    with col1:
        filter_preset = st.selectbox(
            "Filtro Pré-definido:",
            ["Nenhum", "HTTP (port 80)", "HTTPS (port 443)", "DNS (port 53)", "TCP", "UDP", "ICMP"]
        )
    
    with col2:
        custom_filter = st.text_input("Filtro Personalizado (BPF):", placeholder="Ex: tcp port 80")
    
    # Determina o filtro final
    filter_expr = None
    if filter_preset != "Nenhum":
        filter_map = {
            "HTTP (port 80)": "port 80",
            "HTTPS (port 443)": "port 443", 
            "DNS (port 53)": "port 53",
            "TCP": "tcp",
            "UDP": "udp",
            "ICMP": "icmp"
        }
        filter_expr = filter_map.get(filter_preset)
    
    if custom_filter:
        filter_expr = custom_filter
    
    # Configurações avançadas
    st.subheader("⚙️ Configurações Avançadas")
    col1, col2 = st.columns(2)
    
    with col1:
        packet_count = st.number_input("Máximo de pacotes (0 = ilimitado):", min_value=0, value=50)
    with col2:
        capture_timeout = st.number_input("Timeout da captura (segundos):", min_value=1, value=30)
    
    # Botões de controle
    st.subheader("🎮 Controles")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("▶️ Iniciar Captura", type="primary"):
            try:
                # Interface final
                final_interface = None if selected_interface.startswith("Auto") else selected_interface
                
                # Debug info
                st.info(f"🔧 Configuração: Interface={final_interface}, Filtro={filter_expr}")
                
                # Cria novo sniffer
                with st.spinner("Criando sniffer..."):
                    st.session_state.sniffer = PacketSniffer(
                        interface=final_interface,
                        filter_expr=filter_expr
                    )
                    st.success("✅ Sniffer criado!")
                
                # Inicia captura
                with st.spinner("Iniciando captura..."):
                    result = st.session_state.sniffer.start_capture(
                        packet_count=packet_count,
                        timeout=capture_timeout
                    )
                
                if "message" in result:
                    st.success("✅ Captura iniciada!")
                    st.info("🔄 Use o botão 'Atualizar' para ver os pacotes sendo capturados")
                    st.session_state.capture_running = True
                else:
                    st.error(f"❌ Erro: {result.get('error', 'Erro desconhecido')}")
                    
            except Exception as e:
                st.error(f"❌ Erro ao iniciar captura: {e}")
                import traceback
                st.code(traceback.format_exc())
    
    with col2:
        if st.button("⏹️ Parar Captura"):
            try:
                if st.session_state.sniffer:
                    st.session_state.sniffer.stop_capture()
                    st.success("✅ Captura finalizada!")
                    st.session_state.capture_running = False
                else:
                    st.warning("⚠️ Nenhuma captura ativa")
            except Exception as e:
                st.error(f"❌ Erro ao parar captura: {e}")
    
    with col3:
        if st.button("🔄 Atualizar"):
            st.rerun()
    
    # Exibe status atual
    if st.session_state.sniffer:
        try:
            stats = st.session_state.sniffer.get_statistics()
            
            with status_container:
                col1, col2, col3, col4 = st.columns(4)
                
                with col1:
                    status = "🟢 Ativo" if stats.get('is_running') else "🔴 Parado"
                    st.metric("Status", status)
                
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
    
    # Seção de pacotes
    st.subheader("📦 Pacotes Capturados")
    
    # Feedback sobre a captura ativa
    capture_is_running = False
    if st.session_state.sniffer:
        try:
            stats = st.session_state.sniffer.get_statistics()
            capture_is_running = stats.get('is_running', False)
        except:
            # Fallback: verifica se o atributo existe
            try:
                capture_is_running = getattr(st.session_state.sniffer, 'is_running', False)
            except:
                capture_is_running = False
    
    if capture_is_running:
        st.info("🔄 Captura ativa - Use 'Carregar Pacotes' para ver novos dados")
        
        # Mostra progresso se há limite de pacotes
        try:
            if st.session_state.sniffer:
                current_packets = len(st.session_state.sniffer.get_packets())
                if packet_count > 0:
                    progress = min(current_packets / packet_count, 1.0)
                    st.progress(progress, text=f"Progresso: {current_packets}/{packet_count} pacotes")
                else:
                    st.info(f"📊 Pacotes capturados até agora: {current_packets}")
        except Exception as e:
            st.warning(f"⚠️ Erro ao obter progresso: {e}")
    
    # Controles de pacotes
    col1, col2, col3 = st.columns(3)
    
    with col1:
        display_limit = st.slider("Pacotes a exibir:", 5, 100, 20)
    
    with col2:
        if st.button("📥 Carregar Pacotes"):
            try:
                if st.session_state.sniffer:
                    packets = st.session_state.sniffer.get_packets(limit=display_limit)
                    st.session_state.packets = packets
                    st.success(f"✅ {len(packets)} pacotes carregados!")
                else:
                    st.warning("⚠️ Nenhuma captura ativa")
            except Exception as e:
                st.error(f"❌ Erro ao carregar pacotes: {e}")
    
    with col3:
        if st.button("💾 Exportar"):
            try:
                if st.session_state.sniffer:
                    result = st.session_state.sniffer.export_packets(format='json')
                    if "message" in result:
                        st.success(f"✅ {result['message']}")
                    else:
                        st.error(f"❌ {result.get('error')}")
                else:
                    st.warning("⚠️ Nenhuma captura ativa")
            except Exception as e:
                st.error(f"❌ Erro ao exportar: {e}")
    
    # Exibe tabela de pacotes
    if st.session_state.packets:
        st.subheader("📋 Tabela de Pacotes")
        
        # Converte para DataFrame
        df_packets = pd.DataFrame(st.session_state.packets)
        
        # Formata timestamp se existir
        if 'timestamp' in df_packets.columns:
            try:
                df_packets['timestamp'] = pd.to_datetime(df_packets['timestamp']).dt.strftime('%H:%M:%S.%f').str[:-3]
            except:
                pass  # Mantém formato original se der erro
        
        # Seleciona colunas para exibir
        available_columns = df_packets.columns.tolist()
        display_columns = st.multiselect(
            "Colunas a exibir:",
            available_columns,
            default=available_columns[:6]  # Primeiras 6 colunas por padrão
        )
        
        if display_columns:
            st.dataframe(
                df_packets[display_columns],
                use_container_width=True,
                height=400
            )
        
        # Análises especiais
        st.subheader("🔍 Análises Especiais")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("🌐 Analisar HTTP"):
                try:
                    http_packets = analyze_http_traffic(st.session_state.packets)
                    st.write(f"📊 **Pacotes HTTP encontrados:** {len(http_packets)}")
                    if http_packets:
                        st.dataframe(pd.DataFrame(http_packets))
                    else:
                        st.info("Nenhum pacote HTTP encontrado")
                except Exception as e:
                    st.error(f"Erro: {e}")
        
        with col2:
            if st.button("🔍 Analisar DNS"):
                try:
                    dns_packets = analyze_dns_traffic(st.session_state.packets)
                    st.write(f"📊 **Pacotes DNS encontrados:** {len(dns_packets)}")
                    if dns_packets:
                        st.dataframe(pd.DataFrame(dns_packets))
                    else:
                        st.info("Nenhum pacote DNS encontrado")
                except Exception as e:
                    st.error(f"Erro: {e}")
        
        with col3:
            if st.button("📈 Top Talkers"):
                try:
                    top_talkers = get_top_talkers(st.session_state.packets, limit=5)
                    st.write("📊 **Top 5 IPs por tráfego:**")
                    if top_talkers:
                        df_top = pd.DataFrame(top_talkers, columns=['IP', 'Bytes'])
                        st.dataframe(df_top)
                    else:
                        st.info("Dados insuficientes para análise")
                except Exception as e:
                    st.error(f"Erro: {e}")
    
    else:
        st.info("📝 Nenhum pacote carregado. Inicie uma captura e clique em 'Carregar Pacotes'.")
    
    # Informações adicionais
    with st.expander("ℹ️ Informações e Dicas", expanded=False):
        st.markdown("""
        ### 🎯 Como usar:
        1. **Detectar Interfaces**: Primeiro, detecte as interfaces de rede disponíveis
        2. **Configurar**: Escolha interface, filtros e limites
        3. **Capturar**: Inicie a captura e aguarde alguns segundos
        4. **Visualizar**: Carregue os pacotes para análise
        5. **Analisar**: Use as ferramentas de análise especializada
        
        ### 🔍 Filtros BPF comuns:
        - `port 80` - Tráfego HTTP
        - `port 443` - Tráfego HTTPS
        - `port 53` - Tráfego DNS
        - `tcp` - Apenas TCP
        - `udp` - Apenas UDP
        - `host 192.168.1.1` - Apenas um IP específico
        
        ### ⚠️ Requisitos:
        - **Windows**: Execute como Administrador
        - **Linux/Mac**: Execute com `sudo`
        - **PyShark**: Certifique-se de que está instalado
        """)

elif tool == "🔍 Port Scanner":
    st.header("🔍 Port Scanner")
    st.markdown("""
    ### 🚧 Em desenvolvimento
    
    Esta ferramenta permitirá escanear portas de dispositivos na rede.
    
    **Funcionalidades planejadas:**
    - Escaneamento de portas TCP/UDP
    - Detecção de serviços
    - Exportação de resultados
    
    **Uso:**
    1. Insira o intervalo de IPs ou selecione um dispositivo da rede
    2. Escolha as portas ou intervalos de portas a serem escaneadas
    3. Inicie o escaneamento e aguarde os resultados
    
    **Notas:**
    - O escaneamento pode demorar dependendo do número de portas e dispositivos
    - Certifique-se de ter permissão para escanear os dispositivos na rede
    """)

elif tool == "🌐 Network Scanner":
    st.header("🌐 Network Scanner")
    st.markdown("""
    ### 🚧 Em desenvolvimento
    
    Esta ferramenta permitirá descobrir dispositivos na rede e coletar informações básicas.
    
    **Funcionalidades planejadas:**
    - Descoberta de dispositivos na mesma rede local
    - Coleta de informações como IP, MAC, fabricante, etc.
    - Exibição de dispositivos em formato de lista ou gráfico
    
    **Uso:**
    1. Selecione a interface de rede a ser usada para a descoberta
    2. Inicie a descoberta e aguarde os resultados
    
    **Notas:**
    - A descoberta pode demorar dependendo do tamanho da rede
    - Certifique-se de ter permissão para escanear a rede
    """)

elif tool == "📶 Ping & Traceroute":
    st.header("📶 Ping & Traceroute")
    st.markdown("""
    ### 🚧 Em desenvolvimento
    
    Esta ferramenta permitirá testar a conectividade com dispositivos na rede e na internet.
    
    **Funcionalidades planejadas:**
    - Teste de ping para verificar a disponibilidade de dispositivos
    - Traceroute para mapear a rota até um dispositivo
    - Exibição de estatísticas como tempo médio de resposta, perda de pacotes, etc.
    
    **Uso:**
    1. Insira o endereço IP ou hostname do dispositivo a ser testado
    2. Escolha o número de pacotes a serem enviados no teste de ping
    3. Inicie o teste e aguarde os resultados
    
    **Notas:**
    - O teste de ping pode ser bloqueado por firewalls ou configurações de rede
    - Certifique-se de ter permissão para testar os dispositivos na rede
    """)

elif tool == "📊 Bandwidth Monitor":
    st.header("📊 Bandwidth Monitor")
    st.markdown("""
    ### 🚧 Em desenvolvimento
    
    Esta ferramenta permitirá monitorar a largura de banda da rede em tempo real.
    
    **Funcionalidades planejadas:**
    - Monitoramento da largura de banda de upload e download
    - Exibição de gráficos em tempo real
    - Registro de histórico de uso da largura de banda
    
    **Uso:**
    1. Selecione a interface de rede a ser monitorada
    2. Inicie o monitoramento e visualize os gráficos em tempo real
    
    **Notas:**
    - O monitoramento contínuo pode gerar uma grande quantidade de dados
    - Certifique-se de ter espaço suficiente em disco para o registro dos dados
    """)

elif tool == "📋 Network Info":
    st.header("📋 Network Info")
    st.markdown("""
    ### 🚧 Em desenvolvimento
    
    Esta ferramenta permitirá visualizar informações detalhadas sobre a rede e dispositivos conectados.
    
    **Funcionalidades planejadas:**
    - Exibição de informações da interface de rede (IP, máscara, gateway, DNS, etc.)
    - Listagem de dispositivos conectados à mesma rede
    - Exibição de rotas e tabelas de roteamento
    
    **Uso:**
    1. Selecione a interface de rede a ser analisada
    2. Visualize as informações detalhadas exibidas
    
    **Notas:**
    - Algumas informações podem não estar disponíveis dependendo das configurações da rede e do sistema
    - Certifique-se de ter permissão para visualizar as informações da rede
    """)

elif tool == "⚙️ Configurações":
    st.header("⚙️ Configurações")
    st.markdown("""
    ### Ajustes e Preferências
    
    Esta seção permite ajustar configurações da aplicação e preferências do usuário.
    
    **Configurações disponíveis:**
    - Idioma da aplicação
    - Tema (claro/escuro)
    - Configurações de rede (timeout, retries, etc.)
    
    **Como usar:**
    1. Selecione as opções desejadas em cada configuração
    2. As alterações serão aplicadas imediatamente
    
    **Notas:**
    - Algumas configurações podem exigir reiniciar a aplicação para ter efeito
    - Certifique-se de entender cada configuração antes de alterar
    """)

# Sidebar com informações
st.sidebar.markdown("---")
st.sidebar.markdown("### 📊 Estatísticas da Sessão")

if st.session_state.sniffer:
    try:
        stats = st.session_state.sniffer.get_statistics()
        st.sidebar.metric("Pacotes Capturados", stats.get('total_packets', 0))
        st.sidebar.metric("Status", "🟢 Ativo" if stats.get('is_running') else "🔴 Parado")
    except:
        pass

st.sidebar.markdown("---")
st.sidebar.markdown("""
### 💡 Versão Integrada
- ✅ Sem backend separado
- ✅ Menos dependências  
- ✅ Mais simples
- ✅ Execução direta
""")

# Auto-refresh para capturas ativas
if st.session_state.get('capture_running') and st.session_state.sniffer:
    try:
        stats = st.session_state.sniffer.get_statistics()
        if stats.get('is_running'):
            time.sleep(0.1)  # Pequeno delay
            st.rerun()  # Auto-refresh
    except:
        pass

# Debug information section
if st.checkbox("🐛 Mostrar informações de debug"):
    st.subheader("🔧 Debug")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.write("**Estado da sessão:**")
        st.write(f"- Sniffer criado: {st.session_state.sniffer is not None}")
        st.write(f"- Interfaces detectadas: {len(st.session_state.interfaces)}")
        st.write(f"- PyShark disponível: {SNIFFER_AVAILABLE}")
        
    with col2:
        st.write("**Configuração atual:**")
        try:
            st.write(f"- Interface: {selected_interface}")
        except NameError:
            st.write("- Interface: Não definida")
        try:
            st.write(f"- Filtro: {filter_expr or 'Nenhum'}")
        except NameError:
            st.write("- Filtro: Não definido")
        try:
            st.write(f"- Max pacotes: {packet_count}")
        except NameError:
            st.write("- Max pacotes: Não definido")
        try:
            st.write(f"- Timeout: {capture_timeout}s")
        except NameError:
            st.write("- Timeout: Não definido")
        
    if st.session_state.sniffer:
        st.write("**Status do sniffer:**")
        try:
            debug_stats = st.session_state.sniffer.get_statistics()
            st.json(debug_stats)
        except Exception as e:
            st.error(f"Erro ao obter debug stats: {e}")
