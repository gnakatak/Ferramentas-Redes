from flask import Blueprint, jsonify, request
import threading
import ferramentas.metrics.ping as ping_module
import ferramentas.metrics.throughput as tp_module
import ferramentas.firewall.modulo as fw
import ferramentas.sniffer.sniffer as sniffer

api_routes = Blueprint('api_routes', __name__)

# Instância global do sniffer e estado da captura
packet_sniffer = None
capture_thread = None
capture_results = {
    "is_capturing": False,
    "packets": [],
    "stats": {},
    "last_capture_time": None
}
@api_routes.route('/api/hello')
def hello_route():
    return fw.hello()

@api_routes.route('/api/goodbye')
def goodbye():
    return jsonify({"message": "Adeus do backend Flask!"})

# ========== ROTAS DO SNIFFER ==========

@api_routes.route("/api/metrics/ping")
def ping_route():
    host = request.args.get("host", "8.8.8.8")
    count = int(request.args.get("count", "3"))
    result = ping_module.ping(host, count)
    return jsonify(result)

@api_routes.route("/api/metrics/throughput")
def throughput_route():
    result = tp_module.medir_throughput()
    return jsonify(result)

# ========== ROTAS DO SNIFFER ==========

@api_routes.route('/api/sniffer/interfaces', methods=['GET'])
def get_interfaces():
    """Retorna lista de interfaces de rede disponíveis"""
    try:
        print("🔧 DEBUG API: Obtendo interfaces...")
        interfaces = sniffer.get_network_interfaces()
        print(f"🔧 DEBUG API: {len(interfaces)} interfaces encontradas")
        return jsonify({
            "success": True,
            "interfaces": interfaces
        })
    except Exception as e:
        print(f"❌ DEBUG API: Erro ao obter interfaces: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_routes.route('/api/sniffer/start', methods=['POST'])
def start_sniffer():
    """Inicia a captura de pacotes"""
    global packet_sniffer, capture_results
    
    try:
        data = request.get_json() or {}
        interface = data.get('interface')
        filter_expr = data.get('filter')
        packet_count = data.get('packet_count', 50)
        timeout = data.get('timeout', 30)
        
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
        
        return jsonify({
            "success": True,
            "message": "Captura iniciada com sucesso"
        })
        
    except Exception as e:
        print(f"❌ DEBUG: Erro ao iniciar captura: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_routes.route('/api/sniffer/stop', methods=['POST'])
def stop_sniffer():
    """Para a captura de pacotes"""
    global packet_sniffer
    
    print("🔧 DEBUG: Chamando /api/sniffer/stop")
    try:
        if not packet_sniffer:
            print("❌ DEBUG: Nenhum sniffer ativo")
            return jsonify({
                "success": False,
                "error": "Nenhuma captura ativa"
            }), 400

        result = packet_sniffer.stop_capture()
        print(f"🔧 DEBUG: Resultado de stop_capture: {result}")

        if "error" in result:
            print(f"❌ DEBUG: Erro ao parar captura: {result['error']}")
            return jsonify({
                "success": False,
                "error": result["error"]
            }), 400

        print("✅ DEBUG: Captura parada com sucesso")
        return jsonify({
            "success": True,
            "message": result["message"]
        })
    except Exception as e:
        print(f"❌ DEBUG: Exceção no endpoint /api/sniffer/stop: {e}")
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_routes.route('/api/sniffer/status', methods=['GET'])
def get_sniffer_status():
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
                is_running = hasattr(packet_sniffer, 'capture') and packet_sniffer.capture is not None
                status_info["sniffer_running"] = is_running
            except:
                pass
        
        return jsonify(status_info)
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_routes.route('/api/sniffer/packets', methods=['GET'])
def get_packets():
    """Retorna os pacotes capturados"""
    global packet_sniffer, capture_results
    
    try:
        limit = request.args.get('limit', 100, type=int)
        
        # Usa primeiro os resultados globais, depois o sniffer
        if capture_results["packets"]:
            packets = capture_results["packets"][:limit]
            return jsonify({
                "success": True,
                "packets": packets,
                "count": len(packets),
                "total_captured": len(capture_results["packets"]),
                "is_capturing": capture_results["is_capturing"],
                "stats": capture_results.get("stats", {})
            })
        elif packet_sniffer:
            packets = packet_sniffer.get_packets(limit=limit)
            return jsonify({
                "success": True,
                "packets": packets,
                "count": len(packets),
                "is_capturing": capture_results["is_capturing"]
            })
        else:
            return jsonify({
                "success": True,
                "packets": [],
                "count": 0,
                "message": "Nenhuma captura realizada ainda",
                "is_capturing": capture_results["is_capturing"]
            })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_routes.route('/api/sniffer/analyze/http', methods=['GET'])
def analyze_http():
    """Analisa tráfego HTTP"""
    global packet_sniffer
    
    try:
        if not packet_sniffer:
            return jsonify({
                "success": False,
                "error": "Nenhuma captura ativa"
            }), 400
        
        packets = packet_sniffer.get_packets()
        http_packets = sniffer.analyze_http_traffic(packets)
        
        return jsonify({
            "success": True,
            "http_packets": http_packets,
            "count": len(http_packets)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_routes.route('/api/sniffer/analyze/dns', methods=['GET'])
def analyze_dns():
    """Analisa tráfego DNS"""
    global packet_sniffer
    
    try:
        if not packet_sniffer:
            return jsonify({
                "success": False,
                "error": "Nenhuma captura ativa"
            }), 400
        
        packets = packet_sniffer.get_packets()
        dns_packets = sniffer.analyze_dns_traffic(packets)
        
        return jsonify({
            "success": True,
            "dns_packets": dns_packets,
            "count": len(dns_packets)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_routes.route('/api/sniffer/analyze/top-talkers', methods=['GET'])
def get_top_talkers():
    """Retorna os IPs que mais geraram tráfego"""
    global packet_sniffer
    
    try:
        if not packet_sniffer:
            return jsonify({
                "success": False,
                "error": "Nenhuma captura ativa"
            }), 400
        
        limit = request.args.get('limit', 10, type=int)
        packets = packet_sniffer.get_packets()
        top_talkers = sniffer.get_top_talkers(packets, limit=limit)
        
        return jsonify({
            "success": True,
            "top_talkers": [
                {"ip": ip, "bytes": bytes_count}
                for ip, bytes_count in top_talkers
            ]
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500
