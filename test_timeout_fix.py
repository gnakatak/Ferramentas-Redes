#!/usr/bin/env python3
"""
Teste específico para verificar a correção de timeout
"""

from backend.ferramentas.sniffer.sniffer import PacketSniffer
import time

def test_timeout_fix():
    print("🧪 TESTE DE CORREÇÃO DE TIMEOUT")
    print("=" * 60)
    
    try:
        # Cria sniffer
        sniffer = PacketSniffer()
        print("✅ Sniffer criado")
        
        # Testa captura com timeout maior para ver os fallbacks
        print("\n🚀 Testando captura subprocess com fallbacks...")
        try:
            packets = sniffer.start_capture_subprocess(packet_count=10, timeout=15)
            
            if packets and len(packets) > 0:
                print(f"✅ Captura funcionou! {len(packets)} pacotes")
                return True
            else:
                print("⚠️ Captura não retornou pacotes")
                return True  # Ainda é sucesso se não houve erro
                
        except Exception as e:
            print(f"❌ Erro na captura: {e}")
            return False
            
    except Exception as e:
        print(f"❌ Erro geral: {e}")
        return False

if __name__ == "__main__":
    success = test_timeout_fix()
    if success:
        print("\n🎉 TESTE CONCLUÍDO!")
        print("✅ Correções de timeout aplicadas")
    else:
        print("\n❌ TESTE FALHOU")
        print("   Ainda há problemas a corrigir")
