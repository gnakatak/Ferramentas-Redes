"""
Configurador Automático do Sniffer - Versão Completa
Instala e configura automaticamente todas as dependências necessárias
"""
import subprocess
import sys
import os
import platform
import ctypes
import webbrowser

def is_admin():
    """Verifica se está executando como administrador"""
    try:
        if platform.system() == "Windows":
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            try:
                return os.geteuid() == 0
            except AttributeError:
                return False
    except:
        return False

def check_npcap():
    """Verifica instalação do Npcap"""
    if platform.system() != "Windows":
        return True
    
    npcap_paths = [
        "C:\\Windows\\System32\\Npcap",
        "C:\\Windows\\SysWOW64\\Npcap",
        "C:\\Program Files\\Npcap"
    ]
    
    return any(os.path.exists(path) for path in npcap_paths)

def install_python_deps():
    """Instala dependências Python"""
    print("📦 Instalando dependências Python...")
    try:
        subprocess.check_call([sys.executable, '-m', 'pip', 'install', 
                             'streamlit', 'pyshark', 'pandas'])
        print("✅ Dependências Python instaladas com sucesso!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"❌ Erro ao instalar dependências: {e}")
        return False

def download_npcap():
    """Baixa o Npcap automaticamente"""
    print("📥 Baixando Npcap...")
    try:
        # URL do Npcap (pode mudar - verificar site oficial)
        url = "https://nmap.org/npcap/dist/npcap-1.79.exe"
        
        with tempfile.NamedTemporaryFile(delete=False, suffix=".exe") as tmp_file:
            urllib.request.urlretrieve(url, tmp_file.name)
            print(f"✅ Npcap baixado: {tmp_file.name}")
            return tmp_file.name
    except Exception as e:
        print(f"❌ Erro ao baixar Npcap: {e}")
        return None

def run_as_admin():
    """Verifica se está rodando como administrador"""
    try:
        import ctypes
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def main():
    print("🚀 Setup do Sniffer de Pacotes")
    print("=" * 40)
    
    # Verifica privilégios
    if not run_as_admin():
        print("⚠️  AVISO: Execute este script como Administrador para melhor funcionamento")
    
    # Instala dependências Python
    if not install_python_deps():
        print("❌ Falha na instalação das dependências Python")
        return
    
    # Orientações para Npcap
    print("\n🔧 Próximo passo: Instalar Npcap")
    print("📋 Instruções:")
    print("1. Acesse: https://nmap.org/npcap/")
    print("2. Baixe a versão mais recente")
    print("3. Execute como Administrador")
    print("4. ✅ IMPORTANTE: Marque 'Install Npcap in WinPcap API-compatible mode'")
    
    response = input("\n🌐 Abrir página do Npcap agora? (s/n): ")
    if response.lower() in ['s', 'sim', 'y', 'yes']:
        import webbrowser
        webbrowser.open("https://nmap.org/npcap/")
    
    print("\n🎉 Após instalar o Npcap, execute:")
    print("   python run_integrated.py")

if __name__ == "__main__":
    main()