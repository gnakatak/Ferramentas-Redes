#!/usr/bin/env python3
"""
Teste de detecção de interfaces de rede
"""

import subprocess
import platform
import socket

def test_netifaces():
    """Testa se netifaces está funcionando"""
    print("🔍 Testando netifaces...")
    try:
        import netifaces
        print("✅ netifaces importado com sucesso")
        
        interfaces = netifaces.interfaces()
        print(f"🔧 Interfaces detectadas: {interfaces}")
        
        for iface in interfaces:
            try:
                addrs = netifaces.ifaddresses(iface)
                print(f"   {iface}: {addrs}")
            except Exception as e:
                print(f"   {iface}: erro - {e}")
        
        return True, interfaces
    except ImportError:
        print("❌ netifaces não está instalado")
        return False, []
    except Exception as e:
        print(f"❌ Erro no netifaces: {e}")
        return False, []

def test_psutil():
    """Testa se psutil está funcionando"""
    print("\n🔍 Testando psutil...")
    try:
        import psutil
        print("✅ psutil importado com sucesso")
        
        stats = psutil.net_if_stats()
        addrs = psutil.net_if_addrs()
        
        for iface in stats:
            print(f"   {iface}: {stats[iface]}")
            if iface in addrs:
                print(f"      IPs: {addrs[iface]}")
        
        return True, list(stats.keys())
    except ImportError:
        print("❌ psutil não está instalado")
        return False, []
    except Exception as e:
        print(f"❌ Erro no psutil: {e}")
        return False, []

def test_system_commands():
    """Testa comandos do sistema"""
    print("\n🔍 Testando comandos do sistema...")
    system = platform.system()
    
    if system == "Windows":
        try:
            result = subprocess.run(['ipconfig'], capture_output=True, text=True)
            print("✅ ipconfig executado com sucesso")
            
            # Procura por interfaces
            lines = result.stdout.split('\n')
            interfaces = []
            for line in lines:
                if "adapter" in line.lower() or "ethernet" in line.lower() or "wi-fi" in line.lower():
                    interfaces.append(line.strip())
            
            print(f"🔧 Interfaces encontradas: {interfaces}")
            return True, interfaces
        except Exception as e:
            print(f"❌ Erro no ipconfig: {e}")
            return False, []
    
    elif system in ["Linux", "Darwin"]:
        try:
            result = subprocess.run(['ifconfig'], capture_output=True, text=True)
            print("✅ ifconfig executado com sucesso")
            
            # Procura por interfaces
            lines = result.stdout.split('\n')
            interfaces = []
            for line in lines:
                if line and not line.startswith(' ') and not line.startswith('\t'):
                    iface = line.split(':')[0].strip()
                    if iface:
                        interfaces.append(iface)
            
            print(f"🔧 Interfaces encontradas: {interfaces}")
            return True, interfaces
        except Exception as e:
            print(f"❌ Erro no ifconfig: {e}")
            return False, []
    
    return False, []

def test_socket_method():
    """Testa método usando socket"""
    print("\n🔍 Testando método socket...")
    try:
        hostname = socket.gethostname()
        local_ip = socket.gethostbyname(hostname)
        print(f"✅ Hostname: {hostname}")
        print(f"✅ IP local: {local_ip}")
        
        # Tenta conectar para descobrir interface ativa
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            active_ip = s.getsockname()[0]
            print(f"✅ IP ativo: {active_ip}")
        
        return True, [hostname, local_ip, active_ip]
    except Exception as e:
        print(f"❌ Erro no método socket: {e}")
        return False, []

def main():
    print("🌐 Teste de Detecção de Interfaces de Rede")
    print("=" * 50)
    
    # Testa todos os métodos
    test_netifaces()
    test_psutil()
    test_system_commands()
    test_socket_method()
    
    print("\n" + "=" * 50)
    print("✅ Teste concluído")

if __name__ == "__main__":
    main()
