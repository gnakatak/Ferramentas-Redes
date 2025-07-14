# ferramentas/port_scanner_module.py
import streamlit as st
import socket

def scan_port(target_host, port, timeout=1):
    """Tenta conectar a uma porta específica e retorna se está aberta."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(timeout)
        result = s.connect_ex((target_host, port))
        s.close()
        if result == 0:
            return True
        else:
            return False
    except socket.gaierror:
        return None # Hostname could not be resolved
    except socket.error:
        return False # Other socket errors

def get_common_service(port):
    """Retorna um nome de serviço comum para a porta."""
    services = {
        20: "FTP (Data)", 21: "FTP (Control)", 22: "SSH", 23: "Telnet",
        25: "SMTP", 53: "DNS", 67: "DHCP (Server)", 68: "DHCP (Client)",
        80: "HTTP", 110: "POP3", 139: "NetBIOS Session Service", 143: "IMAP",
        443: "HTTPS", 3389: "RDP", 8080: "HTTP Proxy/Alt HTTP"
    }
    return services.get(port, "Serviço Desconhecido")

def port_scanner():
    st.title("🛡️ Verificador de Portas")
    st.write("Verifique quais portas estão abertas em um host.")

    target = st.text_input("Digite o IP ou Domínio do alvo", "scanme.nmap.org")
    
    col1, col2 = st.columns(2)
    start_port = col1.number_input("Porta Inicial", min_value=1, max_value=65535, value=1)
    end_port = col2.number_input("Porta Final", min_value=1, max_value=65535, value=100)

    if st.button("Escanear Portas"):
        if start_port > end_port:
            st.error("A porta inicial não pode ser maior que a porta final.")
            return

        ports_to_scan = range(start_port, end_port + 1)
        open_ports = []
        
        try:
            # Resolva o hostname para IP uma única vez
            ip_address = socket.gethostbyname(target)
            st.info(f"Escaneando {target} ({ip_address}) nas portas {start_port}-{end_port}...")

            progress_bar = st.progress(0)
            status_text = st.empty()

            for i, port in enumerate(ports_to_scan):
                status_text.text(f"Escaneando porta {port}...")
                is_open = scan_port(ip_address, port)
                if is_open:
                    open_ports.append((port, get_common_service(port)))
                
                progress_bar.progress((i + 1) / len(ports_to_scan))

            st.success("Escaneamento concluído!")

            if open_ports:
                st.subheader("Portas Abertas Encontradas:")
                for port, service in open_ports:
                    st.write(f"🟢 Porta {port}: {service}")
            else:
                st.info("Nenhuma porta aberta encontrada no intervalo especificado.")

        except socket.gaierror:
            st.error(f"Não foi possível resolver o hostname: {target}. Verifique se o nome está correto.")
        except Exception as e:
            st.error(f"Ocorreu um erro durante o escaneamento: {e}")