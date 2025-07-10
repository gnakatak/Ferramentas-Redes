#!/usr/bin/env python3
"""
Teste rápido dos problemas de captura corrigidos
"""

import sys
import os

# Adiciona o caminho do backend
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from ferramentas.sniffer.sniffer import PacketSniffer

def test_tshark_interfaces():
    """Testa listagem de interfaces do tshark"""
    print("🔧 Testando interfaces do tshark...")
    
    sniffer = PacketSniffer()
    
    # Testa função de busca de tshark
    tshark_path = sniffer._find_tshark_path()
    print(f"📍 tshark encontrado em: {tshark_path}")
    
    # Testa primeira interface
    first_interface = sniffer._get_first_available_interface()
    print(f"🥇 Primeira interface: {first_interface}")
    
    # Testa mapeamento de Wi-Fi
    wifi_mapped = sniffer._get_tshark_interface("Wi-Fi")
    print(f"📡 Wi-Fi mapeado para: {wifi_mapped}")
    
    return first_interface is not None

def test_subprocess_capture():
    """Testa captura via subprocess com correções"""
    print("\n🧪 Testando captura subprocess corrigida...")
    
    sniffer = PacketSniffer()
    
    try:
        print("🚀 Iniciando captura de 1 pacote com timeout de 10s...")
        result = sniffer._capture_via_subprocess(packet_count=1, timeout=10)
        
        if result:
            print("✅ Captura subprocess funcionou!")
            packets = sniffer.get_packets()
            print(f"📦 Pacotes capturados: {len(packets)}")
            return True
        else:
            print("❌ Captura subprocess falhou")
            return False
            
    except Exception as e:
        print(f"❌ Erro na captura: {e}")
        return False

def test_pyshark_simplified():
    """Testa PyShark com configuração mais simples"""
    print("\n🐍 Testando PyShark simplificado...")
    
    try:
        import pyshark
        
        # Teste muito simples - sem interface específica
        print("🔧 Criando LiveCapture sem interface específica...")
        capture = pyshark.LiveCapture()
        
        print("📡 Tentando capturar 1 pacote com timeout de 5s...")
        packets = capture.sniff(timeout=5, packet_count=1)
        
        if packets:
            packet_list = list(packets) if hasattr(packets, '__iter__') else []
            print(f"✅ PyShark capturou {len(packet_list)} pacotes")
            return True
        else:
            print("⚠️ PyShark não capturou pacotes")
            return False
            
    except Exception as e:
        print(f"❌ Erro no PyShark: {e}")
        return False

def main():
    print("🔬 TESTE DAS CORREÇÕES DE CAPTURA")
    print("=" * 40)
    
    # Teste 1: Interfaces do tshark
    tshark_ok = test_tshark_interfaces()
    
    # Teste 2: Captura subprocess
    subprocess_ok = test_subprocess_capture()
    
    # Teste 3: PyShark simplificado
    pyshark_ok = test_pyshark_simplified()
    
    print("\n" + "=" * 40)
    print("📊 RESULTADOS:")
    print(f"🔧 tshark interfaces: {'✅' if tshark_ok else '❌'}")
    print(f"🚀 subprocess capture: {'✅' if subprocess_ok else '❌'}")
    print(f"🐍 PyShark simple: {'✅' if pyshark_ok else '❌'}")
    
    if subprocess_ok or pyshark_ok:
        print("\n🎉 SUCESSO: Pelo menos um método de captura está funcionando!")
        print("   O sniffer deve funcionar agora.")
    else:
        print("\n⚠️ PROBLEMA: Nenhum método de captura funcionou")
        print("   Verifique permissões e conexão de rede.")

if __name__ == "__main__":
    main()
