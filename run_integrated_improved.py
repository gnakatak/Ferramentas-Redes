#!/usr/bin/env python3
"""
Script melhorado para executar a versão integrada do Sniffer
Com detecção automática de dependências e fallbacks
"""

import subprocess
import sys
import os
import platform

def check_tshark():
    """
    Verifica se tshark está disponível e retorna o caminho
    Usa a mesma lógica implementada no sniffer
    """
    system = platform.system()
    
    if system == "Windows":
        # Possíveis localizações do tshark no Windows
        possible_paths = [
            "C:\\Program Files\\Wireshark\\tshark.exe",
            "C:\\Program Files (x86)\\Wireshark\\tshark.exe",
            os.path.expanduser("~\\AppData\\Local\\Programs\\Wireshark\\tshark.exe"),
            # Verifica no PATH
            "tshark.exe",
            "tshark"
        ]
        
        for path in possible_paths:
            if path in ["tshark.exe", "tshark"]:
                # Testa se está no PATH
                try:
                    result = subprocess.run([path, '--version'], 
                                          capture_output=True, timeout=3)
                    if result.returncode == 0:
                        return True, path
                except:
                    continue
            else:
                # Verifica se arquivo existe
                if os.path.exists(path):
                    try:
                        result = subprocess.run([path, '--version'], 
                                              capture_output=True, timeout=3)
                        if result.returncode == 0:
                            return True, path
                    except:
                        continue
        
        # Se não encontrou, tenta buscar no registro do Windows
        try:
            import winreg
            with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                              r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as key:
                for i in range(winreg.QueryInfoKey(key)[0]):
                    try:
                        subkey_name = winreg.EnumKey(key, i)
                        with winreg.OpenKey(key, subkey_name) as subkey:
                            try:
                                display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                if "Wireshark" in display_name:
                                    install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                    tshark_path = os.path.join(install_location, "tshark.exe")
                                    if os.path.exists(tshark_path):
                                        return True, tshark_path
                            except:
                                continue
                    except:
                        continue
        except ImportError:
            pass  # winreg não disponível
        
    elif system in ["Linux", "Darwin"]:
        # Unix-like systems
        possible_paths = [
            "/usr/bin/tshark",
            "/usr/local/bin/tshark",
            "/opt/homebrew/bin/tshark",  # macOS with Homebrew
            "tshark"
        ]
        
        for path in possible_paths:
            if path == "tshark":
                try:
                    result = subprocess.run([path, '--version'], 
                                          capture_output=True, timeout=3)
                    if result.returncode == 0:
                        return True, path
                except:
                    continue
            else:
                if os.path.exists(path):
                    try:
                        result = subprocess.run([path, '--version'], 
                                              capture_output=True, timeout=3)
                        if result.returncode == 0:
                            return True, path
                    except:
                        continue
    
    return False, None

def check_admin_privileges():
    """Verifica se está executando como administrador"""
    try:
        if platform.system() == "Windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            # Para sistemas Unix-like (Linux, macOS)
            try:
                return os.geteuid() == 0
            except AttributeError:
                # Fallback se geteuid não estiver disponível
                return False
    except Exception:
        return False

def print_setup_instructions():
    """Imprime instruções de configuração para o sistema"""
    system = platform.system()
    
    print("\n📋 INSTRUÇÕES DE CONFIGURAÇÃO:")
    print("=" * 50)
    
    if system == "Windows":
        print("🔧 Windows:")
        print("1. Instale Npcap: https://nmap.org/npcap/")
        print("   ✅ Marque 'Install Npcap in WinPcap API-compatible Mode'")
        print("2. Opcionalmente instale Wireshark para tshark fallback")
        print("3. Execute este script como Administrador")
    
    elif system == "Linux":
        print("🔧 Linux:")
        print("1. Instale dependências:")
        print("   sudo apt update")
        print("   sudo apt install wireshark-common tshark")
        print("2. Configure permissões:")
        print("   sudo usermod -a -G wireshark $USER")
        print("3. Execute com sudo:")
        print("   sudo python run_integrated_improved.py")
    
    elif system == "Darwin":  # macOS
        print("🔧 macOS:")
        print("1. Instale Wireshark:")
        print("   brew install wireshark")
        print("2. Execute com sudo:")
        print("   sudo python run_integrated_improved.py")
    
    print("\n💡 DICA: O sniffer funciona melhor com privilégios administrativos!")

def main():
    print("🌐 Sniffer de Pacotes - Versão Integrada Melhorada")
    print("=" * 60)
    
    # Verifica diretório correto
    if not os.path.exists("frontend/app_integrated.py"):
        print("❌ Erro: Execute este script a partir do diretório raiz do projeto")
        sys.exit(1)
    
    # Verifica privilégios
    is_admin = check_admin_privileges()
    if is_admin:
        print("✅ Executando com privilégios administrativos")
    else:
        print("⚠️ NÃO está executando como administrador")
        print("   Algumas funcionalidades podem não estar disponíveis")
    
    # Verifica dependências Python
    missing_deps = []
    deps = [('streamlit', 'streamlit'), ('pyshark', 'pyshark'), ('pandas', 'pandas')]
    
    print("\n📦 Verificando dependências Python...")
    for module_name, pip_name in deps:
        try:
            __import__(module_name)
            print(f"✅ {module_name}")
        except ImportError:
            print(f"❌ {module_name}")
            missing_deps.append(pip_name)
    
    if missing_deps:
        print(f"\n❌ Dependências ausentes: {', '.join(missing_deps)}")
        print("📦 Instale com:")
        print(f"   pip install {' '.join(missing_deps)}")
        print("   OU")
        print("   pip install -r requirements_integrated.txt")
        sys.exit(1)
    
    # Verifica tshark (opcional)
    print("\n🔍 Verificando ferramentas de captura...")
    tshark_available, tshark_path = check_tshark()
    if tshark_available:
        print(f"✅ tshark disponível em: {tshark_path}")
        print("🔄 Fallback subprocess ativado")
    else:
        print("⚠️ tshark não encontrado")
        print("💡 Para melhor compatibilidade, instale Wireshark:")
        print("   https://www.wireshark.org/download.html")
        
    # Informações do sistema
    print(f"\n💻 Sistema: {platform.system()} {platform.release()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    
    # Instruções se não for admin
    if not is_admin:
        print_setup_instructions()
        
        response = input("\n❓ Continuar mesmo assim? (s/N): ").lower()
        if response not in ['s', 'sim', 'y', 'yes']:
            print("👋 Execução cancelada")
            sys.exit(0)
    
    # Inicia aplicação
    print("\n🚀 Iniciando aplicação Streamlit...")
    print("🌐 Acesse: http://localhost:8501")
    print("⏹️ Pressione Ctrl+C para parar")
    print("-" * 60)
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "frontend/app_integrated.py",
            "--server.port=8501",
            "--server.headless=false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Aplicação finalizada pelo usuário")
    except Exception as e:
        print(f"\n❌ Erro ao executar aplicação: {e}")
        print("\n💡 Possíveis soluções:")
        print("1. Verifique se as dependências estão instaladas")
        print("2. Execute como administrador")
        print("3. Verifique as configurações de rede")

if __name__ == "__main__":
    main()
