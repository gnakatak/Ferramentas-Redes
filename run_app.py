#!/usr/bin/env python3
"""
Script principal para executar a aplicação Ferramentas de Redes
Backend Flask + Frontend Streamlit (app.py)
"""

import sys
import os
import time
import subprocess
import signal
import requests
from threading import Thread

def check_port_available(port):
    """Verifica se uma porta está disponível"""
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            s.bind(('127.0.0.1', port))
            return True
    except:
        return False

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    print("📦 Verificando dependências...")
    
    required_packages = [
        'flask', 'streamlit', 'pyshark', 'pandas', 'requests'
    ]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - não encontrado")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Pacotes faltando: {', '.join(missing_packages)}")
        print("📥 Execute: pip install -r requirements.txt")
        return False
    
    print("✅ Todas as dependências estão instaladas!")
    return True

def start_backend():
    """Inicia o servidor backend Flask"""
    print("\n🚀 Iniciando backend Flask...")
    
    try:
        backend_process = subprocess.Popen(
            [sys.executable, "backend/server.py"],
            cwd=os.getcwd(),
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            bufsize=1,
            universal_newlines=True
        )
        
        print("⏳ Aguardando backend inicializar...")
        time.sleep(3)
        
        # Testa se o backend está funcionando
        for attempt in range(10):
            try:
                for port in [5000, 5001, 5002, 5003]:
                    try:
                        response = requests.get(f"http://localhost:{port}/api/hello", timeout=2)
                        if response.status_code == 200:
                            print(f"✅ Backend respondendo na porta {port}!")
                            return backend_process, port
                    except:
                        continue
            except:
                pass
            
            print(f"⏳ Tentativa {attempt + 1}/10...")
            time.sleep(1)
        
        print("❌ Backend não respondeu após 10 tentativas")
        return None, None
        
    except Exception as e:
        print(f"❌ Erro ao iniciar backend: {e}")
        return None, None

def start_frontend():
    """Inicia o frontend Streamlit com app.py"""
    print("\n🌐 Iniciando frontend Streamlit...")
    
    try:
        # Verifica se o arquivo app.py existe
        if not os.path.exists("frontend/app.py"):
            print("❌ Arquivo frontend/app.py não encontrado!")
            return None
        
        frontend_process = subprocess.Popen(
            [sys.executable, "-m", "streamlit", "run", 
             "frontend/app.py", 
             "--server.port=8501",
             "--server.headless=false",
             "--browser.gatherUsageStats=false"],
            cwd=os.getcwd()
        )
        
        print("✅ Frontend iniciado com sucesso!")
        print("🌐 Acesse: http://localhost:8501")
        return frontend_process
        
    except Exception as e:
        print(f"❌ Erro ao iniciar frontend: {e}")
        return None

def monitor_backend_output(process):
    """Monitora e exibe output do backend"""
    if not process:
        return
        
    try:
        for line in iter(process.stdout.readline, ''):
            if line:
                print(f"[BACKEND] {line.strip()}")
    except:
        pass

def main():
    print("=" * 65)
    print("🌐 FERRAMENTAS DE REDES - APLICAÇÃO PRINCIPAL")
    print("=" * 65)
    print("Backend (Flask): http://localhost:5000")
    print("Frontend (Streamlit): http://localhost:8501")
    print("App Principal: frontend/app.py")
    print("=" * 65)
    
    # Verifica se estamos no diretório correto
    if not os.path.exists("frontend/app.py") or not os.path.exists("backend/server.py"):
        print("❌ Execute este script a partir do diretório raiz do projeto!")
        print("   Certifique-se de que os arquivos frontend/app.py e backend/server.py existem")
        sys.exit(1)
    
    # Verifica dependências
    if not check_dependencies():
        sys.exit(1)
    
    backend_process = None
    frontend_process = None
    
    try:
        # Inicia backend
        backend_process, backend_port = start_backend()
        if not backend_process:
            print("❌ Falha ao iniciar backend. Verifique os logs acima.")
            sys.exit(1)
        
        # Inicia monitor do backend em thread separada
        monitor_thread = Thread(target=monitor_backend_output, args=(backend_process,), daemon=True)
        monitor_thread.start()
        
        # Aguarda um pouco antes de iniciar o frontend
        time.sleep(2)
        
        # Inicia frontend
        frontend_process = start_frontend()
        if not frontend_process:
            print("❌ Falha ao iniciar frontend.")
            if backend_process:
                backend_process.terminate()
            sys.exit(1)
        
        print(f"\n🎉 APLICAÇÃO INICIADA COM SUCESSO!")
        print(f"🔧 API Backend: http://localhost:{backend_port}/api/hello")
        print(f"🌐 Frontend: http://localhost:8501")
        print(f"📱 App Principal: frontend/app.py")
        print(f"\n💡 Dicas:")
        print(f"   - Acesse o Dashboard para usar todas as ferramentas")
        print(f"   - Use o Sniffer para capturar pacotes de rede")
        print(f"   - Teste a conectividade na aba 'Outras Ferramentas'")
        print(f"\n⏹️  Pressione Ctrl+C para parar")
        
        # Aguarda interrupção
        try:
            frontend_process.wait()
        except KeyboardInterrupt:
            print("\n👋 Interrompido pelo usuário")
            
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    finally:
        print("\n🛑 Finalizando aplicação...")
        
        if frontend_process:
            try:
                frontend_process.terminate()
                frontend_process.wait(timeout=5)
                print("✅ Frontend finalizado")
            except:
                frontend_process.kill()
                print("🔄 Frontend forçado a parar")
        
        if backend_process:
            try:
                backend_process.terminate()
                backend_process.wait(timeout=5)
                print("✅ Backend finalizado")
            except:
                backend_process.kill()
                print("🔄 Backend forçado a parar")
        
        print("🏁 Aplicação finalizada!")

if __name__ == "__main__":
    main()
