#!/usr/bin/env python3
"""
Teste final para verificar se a correção do comando tshark funciona
"""

from backend.ferramentas.sniffer.sniffer import PacketSniffer
import time

def test_tshark_command_fix():
    print("🧪 TESTE DE CORREÇÃO DO COMANDO TSHARK")
    print("=" * 60)
    
    try:
        # Cria sniffer
        sniffer = PacketSniffer()
        print("✅ Sniffer criado")
        
        # Limpa cache de pacotes antigos
        sniffer.captured_packets = []
        
        # Testa captura subprocess diretamente
        print("\n🚀 Testando captura subprocess com comando corrigido...")
        success = sniffer._capture_via_subprocess(packet_count=5, timeout=15)
        
        if success:
            print(f"✅ SUCESSO! Capturou {len(sniffer.captured_packets)} pacotes")
            for i, packet in enumerate(sniffer.captured_packets[:3]):
                print(f"   📦 Pacote {i+1}: {packet.get('protocol', 'UNKNOWN')} "
                      f"{packet.get('src_ip', '?')} -> {packet.get('dst_ip', '?')}")
            return True
        else:
            print("❌ Captura falhou mesmo com comando corrigido")
            return False
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

if __name__ == "__main__":
    success = test_tshark_command_fix()
    if success:
        print("\n🎉 CORREÇÃO DO COMANDO TSHARK FUNCIONOU!")
        print("✅ O sniffer agora deve funcionar perfeitamente")
    else:
        print("\n❌ CORREÇÃO FALHOU")
        print("   Ainda há problemas no comando tshark")
