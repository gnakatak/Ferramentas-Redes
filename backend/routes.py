from flask import Blueprint, jsonify, request
import ferramentas.firewall.modulo as fw
import ferramentas.sniffer.sniffer as sniffer
import asyncio
import threading

api_routes = Blueprint('api_routes', __name__)

# Instância global do sniffer
packet_sniffer = None

@api_routes.route('/api/hello')
def hello_route():
    return fw.hello()

@api_routes.route('/api/goodbye')
def goodbye():
    return jsonify({"message": "Adeus do backend Flask!"})

# ========== ROTAS DO SNIFFER ==========

@api_routes.route('/api/sniffer/interfaces', methods=['GET'])
def get_interfaces():
    """Retorna lista de interfaces de rede disponíveis"""
    try:
        interfaces = sniffer.get_network_interfaces()
        return jsonify({
            "success": True,
            "interfaces": interfaces
        })
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_routes.route('/api/sniffer/start', methods=['POST'])
def start_sniffer():
    """Inicia a captura de pacotes"""
    global packet_sniffer
    
    try:
        data = request.get_json() or {}
        interface = data.get('interface')
        filter_expr = data.get('filter')
        packet_count = data.get('packet_count', 0)
        timeout = data.get('timeout', 30)
        
        print(f"🔧 DEBUG: Iniciando captura com:")
        print(f"   - Interface: {interface}")
        print(f"   - Filtro: {filter_expr}")
        print(f"   - Pacotes: {packet_count}")
        print(f"   - Timeout: {timeout}")
        
        # Cria nova instância do sniffer
        packet_sniffer = sniffer.PacketSniffer(
            interface=interface,
            filter_expr=filter_expr
        )
        print("✅ Sniffer criado")
        
        # Usa APENAS o método subprocess que sabemos que funciona 100%
        print("🔧 Usando método subprocess (único que funciona)")
        
        def run_capture():
            """Executa captura em thread separada"""
            try:
                success = packet_sniffer._capture_via_subprocess(
                    packet_count=packet_count if packet_count > 0 else 50,
                    timeout=timeout
                )
                print(f"🔧 Captura via subprocess resultado: {success}")
                return success
            except Exception as e:
                print(f"❌ Erro na captura subprocess: {e}")
                return False
        
        # Executa em thread separada para não bloquear o Flask
        capture_thread = threading.Thread(target=run_capture, daemon=True)
        capture_thread.start()
        
        # Aguarda um pouco para a captura começar
        import time
        time.sleep(1)
        
        print("✅ Captura iniciada em thread separada")
        return jsonify({
            "success": True,
            "message": "Captura iniciada com sucesso"
        })
        
    except Exception as e:
        print(f"❌ Exceção durante captura: {e}")
        import traceback
        traceback.print_exc()
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_routes.route('/api/sniffer/stop', methods=['POST'])
def stop_sniffer():
    """Para a captura de pacotes"""
    global packet_sniffer
    
    try:
        if not packet_sniffer:
            return jsonify({
                "success": False,
                "error": "Nenhuma captura ativa"
            }), 400
        
        result = packet_sniffer.stop_capture()
        
        if "error" in result:
            return jsonify({
                "success": False,
                "error": result["error"]
            }), 400
        
        return jsonify({
            "success": True,
            "message": result["message"]
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_routes.route('/api/sniffer/status', methods=['GET'])
def get_sniffer_status():
    """Retorna o status e estatísticas da captura"""
    global packet_sniffer
    
    try:
        if not packet_sniffer:
            return jsonify({
                "success": True,
                "status": "inactive",
                "statistics": {}
            })
        
        stats = packet_sniffer.get_statistics()
        
        return jsonify({
            "success": True,
            "statistics": stats
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_routes.route('/api/sniffer/packets', methods=['GET'])
def get_packets():
    """Retorna os pacotes capturados"""
    global packet_sniffer
    
    try:
        if not packet_sniffer:
            return jsonify({
                "success": False,
                "error": "Nenhuma captura ativa"
            }), 400
        
        limit = request.args.get('limit', 100, type=int)
        packets = packet_sniffer.get_packets(limit=limit)
        
        return jsonify({
            "success": True,
            "packets": packets,
            "count": len(packets)
        })
        
    except Exception as e:
        return jsonify({
            "success": False,
            "error": str(e)
        }), 500

@api_routes.route('/api/sniffer/export', methods=['POST'])
def export_packets():
    """Exporta os pacotes capturados"""
    global packet_sniffer
    
    try:
        if not packet_sniffer:
            return jsonify({
                "success": False,
                "error": "Nenhuma captura ativa"
            }), 400
        
        data = request.get_json() or {}
        filename = data.get('filename')
        format_type = data.get('format', 'json')
        
        result = packet_sniffer.export_packets(
            filename=filename,
            format=format_type
        )
        
        if "error" in result:
            return jsonify({
                "success": False,
                "error": result["error"]
            }), 400
        
        return jsonify({
            "success": True,
            "message": result["message"]
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
