#!/usr/bin/env python3
"""
Script melhorado para executar backend + frontend com melhor tratamento de erros
"""

import sys
import os
import time
import subprocess
import signal
from threading import Thread

class ProcessManager:
    def __init__(self):
        self.backend_process = None
        self.frontend_process = None
        self.running = True

    def start_backend(self):
        """Inicia o servidor backend Flask"""
        print("🚀 Iniciando backend Flask...")
        try:
            self.backend_process = subprocess.Popen(
                [sys.executable, "backend/server.py"],
                cwd=os.getcwd(),
                stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT,  # Redireciona stderr para stdout
                text=True,
                bufsize=1,
                universal_newlines=True
            )
            
            # Monitora a saída por mais tempo
            print("⏳ Aguardando backend inicializar...")
            time.sleep(5)  # Aumenta o tempo de espera
            
            if self.backend_process.poll() is not None:
                stdout, _ = self.backend_process.communicate()
                print("❌ Backend falhou ao iniciar:")
                if stdout:
                    print(f"OUTPUT: {stdout}")
                return False
            
            # Testa se o backend está respondendo
            import requests
            try:
                # Tenta porta 5000 primeiro
                response = requests.get("http://localhost:5000/api/hello", timeout=5)
                if response.status_code == 200:
                    print("✅ Backend iniciado e respondendo na porta 5000!")
                    return True
            except requests.exceptions.RequestException:
                # Se 5000 falhar, tenta outras portas
                for port in range(5001, 5010):
                    try:
                        response = requests.get(f"http://localhost:{port}/api/hello", timeout=2)
                        if response.status_code == 200:
                            print(f"✅ Backend iniciado e respondendo na porta {port}!")
                            # Atualiza URL do frontend se necessário
                            print(f"⚠️ Backend está na porta {port}, não 5000")
                            return True
                    except:
                        continue
                
                print("⚠️ Backend iniciou mas não está respondendo em nenhuma porta")
                # Mostra output do processo para debug
                print("🔧 Tentando obter output do backend para debug...")
                return False
            
        except Exception as e:
            print(f"❌ Erro ao iniciar backend: {e}")
            return False

    def start_frontend(self):
        """Inicia o frontend Streamlit"""
        print("🌐 Iniciando frontend Streamlit...")
        try:
            # Aguarda um pouco para garantir que o backend está rodando
            time.sleep(1)
            
            self.frontend_process = subprocess.Popen(
                [sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port=8501"],
                cwd=os.getcwd(),
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True
            )
            
            print("✅ Frontend iniciado com sucesso!")
            print("🌐 Acesse: http://localhost:8501")
            return True
            
        except Exception as e:
            print(f"❌ Erro ao iniciar frontend: {e}")
            return False

    def monitor_processes(self):
        """Monitora os processos e os reinicia se necessário"""
        while self.running:
            try:
                # Verifica backend
                if self.backend_process and self.backend_process.poll() is not None:
                    print("⚠️  Backend parou inesperadamente, tentando reiniciar...")
                    self.start_backend()
                
                # Verifica frontend
                if self.frontend_process and self.frontend_process.poll() is not None:
                    print("⚠️  Frontend parou inesperadamente, tentando reiniciar...")
                    self.start_frontend()
                
                time.sleep(5)
                
            except KeyboardInterrupt:
                break
            except Exception as e:
                print(f"⚠️  Erro no monitor: {e}")
                time.sleep(5)

    def stop_all(self):
        """Para todos os processos"""
        self.running = False
        
        print("\n🛑 Parando processos...")
        
        if self.frontend_process:
            try:
                self.frontend_process.terminate()
                self.frontend_process.wait(timeout=5)
                print("✅ Frontend parado")
            except subprocess.TimeoutExpired:
                self.frontend_process.kill()
                print("⚠️  Frontend forçado a parar")
            except Exception as e:
                print(f"⚠️  Erro ao parar frontend: {e}")
        
        if self.backend_process:
            try:
                self.backend_process.terminate()
                self.backend_process.wait(timeout=5)
                print("✅ Backend parado")
            except subprocess.TimeoutExpired:
                self.backend_process.kill()
                print("⚠️  Backend forçado a parar")
            except Exception as e:
                print(f"⚠️  Erro ao parar backend: {e}")

def check_dependencies():
    """Verifica se as dependências estão instaladas"""
    print("🔍 Verificando dependências...")
    
    required_packages = ['flask', 'streamlit', 'pyshark']
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
        print("Execute: pip install -r requirements.txt")
        return False
    
    print("✅ Todas as dependências estão instaladas!")
    return True

def main():
    print("=" * 60)
    print("🚀 FERRAMENTAS DE REDES - MODO SEPARADO")
    print("=" * 60)
    print("Backend (Flask): http://localhost:5000")
    print("Frontend (Streamlit): http://localhost:8501")
    print("=" * 60)
    
    # Verifica dependências
    if not check_dependencies():
        sys.exit(1)
    
    manager = ProcessManager()
    
    try:
        # Inicia backend
        if not manager.start_backend():
            print("❌ Falha ao iniciar backend. Verifique os logs acima.")
            sys.exit(1)
        
        # Inicia frontend
        if not manager.start_frontend():
            print("❌ Falha ao iniciar frontend. Verifique os logs acima.")
            manager.stop_all()
            sys.exit(1)
        
        print("\n✅ Aplicação iniciada com sucesso!")
        print("🌐 Frontend: http://localhost:8501")
        print("🔧 API Backend: http://localhost:5000/api/hello")
        print("\n⏹️  Pressione Ctrl+C para parar")
        
        # Inicia monitor em thread separada
        monitor_thread = Thread(target=manager.monitor_processes, daemon=True)
        monitor_thread.start()
        
        # Aguarda interrupção
        while manager.running:
            time.sleep(1)
            
    except KeyboardInterrupt:
        print("\n👋 Interrompido pelo usuário")
    except Exception as e:
        print(f"❌ Erro inesperado: {e}")
    finally:
        manager.stop_all()
        print("🏁 Aplicação finalizada")

if __name__ == "__main__":
    main()
