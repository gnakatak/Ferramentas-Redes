"""
Módulo de ferramentas de rede - Versão integrada sem Flask
Funções Python puras para uso direto no Streamlit
"""
import threading
import ferramentas.metrics.ping as ping_module
import ferramentas.metrics.throughput as tp_module
import ferramentas.firewall.modulo as fw
import ferramentas.sniffer.sniffer as sniffer

# Instância global do sniffer e estado da captura
packet_sniffer = None
capture_thread = None
capture_results = {
    "is_capturing": False,
    "packets": [],
    "stats": {},
    "last_capture_time": None
}
def hello():
    """Função de teste"""
    return fw.hello()

def goodbye():
    """Função de despedida"""
    return {"message": "Sistema integrado sem Flask!"}

# ========== FUNÇÕES DE MÉTRICAS ==========

def ping_host(host="8.8.8.8", count=3):
    """Executa ping para um host"""
    result = ping_module.ping(host, count)
    return result

def get_throughput():
    """Mede throughput da rede"""
    result = tp_module.medir_throughput()
    return result

# ========== FUNÇÕES DO SNIFFER ==========

def get_network_interfaces():
    """Retorna lista de interfaces de rede disponíveis"""
    try:
        print("🔧 DEBUG API: Obtendo interfaces...")
        interfaces = sniffer.get_network_interfaces()
        print(f"🔧 DEBUG API: {len(interfaces)} interfaces encontradas")
        return {
            "success": True,
            "interfaces": interfaces
        }
    except Exception as e:
        print(f"❌ DEBUG API: Erro ao obter interfaces: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def start_packet_capture(interface=None, filter_expr=None, packet_count=50, timeout=30):
    """Inicia a captura de pacotes"""
    global packet_sniffer, capture_results
    
    try:
        print(f"🔧 DEBUG: Iniciando captura - Interface: {interface}, Pacotes: {packet_count}")
        
        # Cria nova instância do sniffer
        packet_sniffer = sniffer.PacketSniffer(
            interface=interface,
            filter_expr=filter_expr
        )

        print("✅ DEBUG: Sniffer criado")
        
        def run_capture():
            global capture_results
            try:
                capture_results["is_capturing"] = True
                capture_results["packets"] = []
                
                result = packet_sniffer.start_capture(
                    interface=interface,
                    packet_count=packet_count if packet_count > 0 else 50,
                    timeout=timeout
                )
                
                # Atualiza os resultados globais
                capture_results["packets"] = packet_sniffer.get_packets()
                capture_results["stats"] = packet_sniffer.get_statistics()
                capture_results["last_capture_time"] = result.get("duration", 0)
                
                print(f"✅ DEBUG: Captura concluída - {len(capture_results['packets'])} pacotes")
                
            except Exception as e:
                print(f"❌ DEBUG: Erro na captura: {e}")
            finally:
                capture_results["is_capturing"] = False
        
        capture_thread = threading.Thread(target=run_capture, daemon=True)
        capture_thread.start()
        
        return {
            "success": True,
            "message": "Captura iniciada com sucesso"
        }
        
    except Exception as e:
        print(f"❌ DEBUG: Erro ao iniciar captura: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def stop_packet_capture():
    """Para a captura de pacotes"""
    global packet_sniffer
    
    print("🔧 DEBUG: Chamando stop_packet_capture")
    try:
        if not packet_sniffer:
            print("❌ DEBUG: Nenhum sniffer ativo")
            return {
                "success": False,
                "error": "Nenhuma captura ativa"
            }

        result = packet_sniffer.stop_capture()
        print(f"🔧 DEBUG: Resultado de stop_capture: {result}")

        if result and "error" in result:
            print(f"❌ DEBUG: Erro ao parar captura: {result['error']}")
            return {
                "success": False,
                "error": result["error"]
            }

        print("✅ DEBUG: Captura parada com sucesso")
        return {
            "success": True,
            "message": result.get("message", "Captura finalizada") if result else "Captura finalizada"
        }
    except Exception as e:
        print(f"❌ DEBUG: Exceção no stop_packet_capture: {e}")
        return {
            "success": False,
            "error": str(e)
        }

def get_capture_status():
    """Retorna o status e estatísticas da captura"""
    global packet_sniffer, capture_results
    
    try:
        status_info = {
            "success": True,
            "is_capturing": capture_results["is_capturing"],
            "packets_captured": len(capture_results["packets"]),
            "last_capture_duration": capture_results.get("last_capture_time", 0),
            "statistics": capture_results.get("stats", {})
        }
        
        if packet_sniffer:
            # Adiciona estatísticas do sniffer se disponível
            try:
                sniffer_stats = packet_sniffer.get_statistics()
                status_info["sniffer_stats"] = sniffer_stats
                # Adiciona flag is_running
                is_running = hasattr(packet_sniffer, 'capture') and getattr(packet_sniffer, 'capture', None) is not None
                status_info["sniffer_running"] = is_running
            except:
                pass
        
        return status_info
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def get_captured_packets(limit=100):
    """Retorna os pacotes capturados"""
    global packet_sniffer, capture_results
    
    try:
        # Usa primeiro os resultados globais, depois o sniffer
        if capture_results["packets"]:
            packets = capture_results["packets"][:limit]
            return {
                "success": True,
                "packets": packets,
                "count": len(packets),
                "total_captured": len(capture_results["packets"]),
                "is_capturing": capture_results["is_capturing"],
                "stats": capture_results.get("stats", {})
            }
        elif packet_sniffer:
            packets = packet_sniffer.get_packets(limit=limit)
            return {
                "success": True,
                "packets": packets,
                "count": len(packets),
                "is_capturing": capture_results["is_capturing"]
            }
        else:
            return {
                "success": True,
                "packets": [],
                "count": 0,
                "message": "Nenhuma captura realizada ainda",
                "is_capturing": capture_results["is_capturing"]
            }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def analyze_http_packets():
    """Analisa tráfego HTTP"""
    global packet_sniffer
    
    try:
        if not packet_sniffer:
            return {
                "success": False,
                "error": "Nenhuma captura ativa"
            }
        
        packets = packet_sniffer.get_packets()
        http_packets = sniffer.analyze_http_traffic(packets)
        
        return {
            "success": True,
            "http_packets": http_packets,
            "count": len(http_packets)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def analyze_dns_packets():
    """Analisa tráfego DNS"""
    global packet_sniffer
    
    try:
        if not packet_sniffer:
            return {
                "success": False,
                "error": "Nenhuma captura ativa"
            }
        
        packets = packet_sniffer.get_packets()
        dns_packets = sniffer.analyze_dns_traffic(packets)
        
        return {
            "success": True,
            "dns_packets": dns_packets,
            "count": len(dns_packets)
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }

def get_top_talkers_analysis(limit=10):
    """Retorna os IPs que mais geraram tráfego"""
    global packet_sniffer
    
    try:
        if not packet_sniffer:
            return {
                "success": False,
                "error": "Nenhuma captura ativa"
            }
        
        packets = packet_sniffer.get_packets()
        top_talkers = sniffer.get_top_talkers(packets, limit=limit)
        
        return {
            "success": True,
            "top_talkers": [
                {"ip": ip, "bytes": bytes_count}
                for ip, bytes_count in top_talkers
            ]
        }
        
    except Exception as e:
        return {
            "success": False,
            "error": str(e)
        }
