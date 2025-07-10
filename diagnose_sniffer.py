#!/usr/bin/env python3
"""
Assistente de Diagnóstico e Configuração do Sniffer
Detecta problemas e fornece soluções específicas
"""

import sys
import os
import platform
import subprocess
import ctypes

def check_admin():
    """Verifica privilégios administrativos"""
    try:
        if platform.system() == "Windows":
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            return os.geteuid() == 0
    except:
        return False

def check_npcap():
    """Verifica se Npcap está instalado (Windows)"""
    if platform.system() != "Windows":
        return None
    
    npcap_paths = [
        "C:\\Windows\\System32\\Npcap",
        "C:\\Windows\\SysWOW64\\Npcap",
        "C:\\Program Files\\Npcap"
    ]
    
    for path in npcap_paths:
        if os.path.exists(path):
            return True
    return False

def check_wireshark():
    """Verifica se Wireshark/tshark está instalado"""
    try:
        result = subprocess.run(['tshark', '--version'], 
                              capture_output=True, timeout=5)
        return result.returncode == 0
    except:
        return False

def check_pyshark():
    """Testa PyShark básico"""
    try:
        import pyshark
        # Teste simples de criação
        capture = pyshark.LiveCapture()
        return True
    except ImportError:
        return False
    except Exception:
        return "installed_but_failed"

def print_solution_windows():
    """Soluções específicas para Windows"""
    print("🔧 SOLUÇÕES PARA WINDOWS:")
    print("=" * 50)
    
    is_admin = check_admin()
    npcap_installed = check_npcap()
    wireshark_installed = check_wireshark()
    
    if not is_admin:
        print("1️⃣ EXECUTE COMO ADMINISTRADOR (CRÍTICO)")
        print("   • Clique com botão direito no PowerShell/CMD")
        print("   • Selecione 'Executar como administrador'")
        print("   • OU use: python run_admin.py")
        print("")
    
    if not npcap_installed:
        print("2️⃣ INSTALE NPCAP (OBRIGATÓRIO)")
        print("   • Download: https://nmap.org/npcap/")
        print("   • ✅ IMPORTANTE: Marque 'Install Npcap in WinPcap API-compatible Mode'")
        print("   • Reinicie o computador após instalação")
        print("")
    
    if not wireshark_installed:
        print("3️⃣ INSTALE WIRESHARK (RECOMENDADO)")
        print("   • Download: https://www.wireshark.org/download.html")
        print("   • Inclui tshark para fallback")
        print("   • Escolha versão 64-bit")
        print("")
    
    print("4️⃣ ORDEM DE EXECUÇÃO:")
    print("   1. Instalar Npcap (se não instalado)")
    print("   2. Reiniciar o sistema")
    print("   3. Executar como Administrador:")
    print("      python run_admin.py")
    print("")

def print_solution_linux():
    """Soluções específicas para Linux"""
    print("🔧 SOLUÇÕES PARA LINUX:")
    print("=" * 50)
    
    print("1️⃣ INSTALE DEPENDÊNCIAS:")
    print("   sudo apt update")
    print("   sudo apt install wireshark-common tshark")
    print("")
    
    print("2️⃣ CONFIGURE PERMISSÕES:")
    print("   sudo usermod -a -G wireshark $USER")
    print("   newgrp wireshark")
    print("")
    
    print("3️⃣ EXECUTE COM SUDO:")
    print("   sudo python run_integrated.py")
    print("")

def print_solution_macos():
    """Soluções específicas para macOS"""
    print("🔧 SOLUÇÕES PARA MACOS:")
    print("=" * 50)
    
    print("1️⃣ INSTALE WIRESHARK:")
    print("   brew install wireshark")
    print("")
    
    print("2️⃣ EXECUTE COM SUDO:")
    print("   sudo python run_integrated.py")
    print("")

def test_pyshark_detailed():
    """Teste detalhado do PyShark"""
    print("🧪 TESTE DETALHADO DO PYSHARK:")
    print("=" * 50)
    
    try:
        import pyshark
        print("✅ PyShark importado com sucesso")
        
        # Teste de criação de captura
        try:
            capture = pyshark.LiveCapture()
            print("✅ LiveCapture criado")
            
            # Teste de interfaces
            try:
                from backend.ferramentas.sniffer.sniffer import get_network_interfaces
                interfaces = get_network_interfaces()
                print(f"✅ Interfaces detectadas: {len(interfaces)}")
                for iface in interfaces[:3]:  # Mostra apenas 3 primeiras
                    print(f"   • {iface.get('name', 'Sem nome')}")
            except Exception as e:
                print(f"⚠️ Erro ao detectar interfaces: {e}")
                
        except Exception as e:
            print(f"❌ Erro ao criar LiveCapture: {e}")
            return False
            
    except ImportError:
        print("❌ PyShark não está instalado")
        print("   pip install pyshark")
        return False
    except Exception as e:
        print(f"❌ Erro inesperado no PyShark: {e}")
        return False
    
    return True

def main():
    print("🔍 DIAGNÓSTICO DO SNIFFER DE PACOTES")
    print("=" * 60)
    
    # Informações do sistema
    system = platform.system()
    print(f"💻 Sistema: {system} {platform.release()}")
    print(f"🐍 Python: {sys.version.split()[0]}")
    print(f"👤 Admin: {'✅ Sim' if check_admin() else '❌ Não'}")
    print("")
    
    # Diagnóstico específico por sistema
    if system == "Windows":
        npcap = check_npcap()
        wireshark = check_wireshark()
        
        print("📋 STATUS WINDOWS:")
        print(f"   Npcap: {'✅ Instalado' if npcap else '❌ Não instalado'}")
        print(f"   Wireshark: {'✅ Instalado' if wireshark else '❌ Não instalado'}")
        print("")
        
        if not check_admin() or not npcap:
            print_solution_windows()
            return
            
    elif system == "Linux":
        print_solution_linux()
        return
        
    elif system == "Darwin":
        print_solution_macos()
        return
    
    # Teste PyShark se requisitos básicos atendidos
    print("🧪 TESTANDO PYSHARK...")
    if test_pyshark_detailed():
        print("")
        print("🎉 PYSHARK FUNCIONANDO!")
        print("✅ Você pode executar:")
        print("   python run_integrated.py")
        print("")
        print("💡 Se ainda houver problemas na captura:")
        print("   • Verifique se há tráfego de rede ativo")
        print("   • Tente remover filtros BPF")
        print("   • Use interface 'any' em vez de específica")
    else:
        print("")
        print("❌ PYSHARK COM PROBLEMAS")
        if system == "Windows":
            print_solution_windows()

if __name__ == "__main__":
    main()
