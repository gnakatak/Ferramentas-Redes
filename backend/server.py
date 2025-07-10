# server.py
import sys
import os
import socket
from flask import Flask

# Adiciona o diretório backend ao path para imports relativos
backend_dir = os.path.dirname(os.path.abspath(__file__))
if backend_dir not in sys.path:
    sys.path.insert(0, backend_dir)

def check_port_available(port):
    """Verifica se a porta está disponível"""
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind(('localhost', port))
            return True
    except OSError:
        return False

def find_available_port(start_port=5000):
    """Encontra uma porta disponível"""
    for port in range(start_port, start_port + 10):
        if check_port_available(port):
            return port
    return None

try:
    from routes import api_routes
except ImportError as e:
    print(f"❌ Erro ao importar routes: {e}")
    print("Certifique-se de que o arquivo routes.py existe e está correto")
    sys.exit(1)

app = Flask(__name__)
app.register_blueprint(api_routes)

if __name__ == '__main__':
    print("🚀 Iniciando servidor Flask...")
    
    # Verifica se a porta 5000 está disponível
    port = 5000
    if not check_port_available(port):
        print(f"⚠️  Porta {port} está ocupada, procurando porta alternativa...")
        port = find_available_port(5001)  # Começa em 5001
        if port is None:
            print("❌ Não foi possível encontrar uma porta disponível")
            sys.exit(1)
        else:
            print(f"✅ Usando porta alternativa: {port}")
    
    try:
        print(f"📡 Servidor Flask iniciado na porta {port}")
        print(f"🌐 Acesse: http://localhost:{port}/api/hello")
        print("⏹️  Pressione Ctrl+C para parar")
        print("🔧 Debug mode ativado para troubleshooting")
        
        app.run(host='0.0.0.0', port=port, debug=True, use_reloader=False, threaded=True)
        
    except KeyboardInterrupt:
        print("\n👋 Servidor finalizado pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao iniciar servidor: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
