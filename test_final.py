#!/usr/bin/env python3
"""
Teste das correções finais do sniffer
"""

import sys
import os

# Adiciona backend ao path
backend_dir = os.path.join(os.getcwd(), 'backend')
sys.path.insert(0, backend_dir)

def test_imports():
    """Testa imports do sniffer"""
    print("🧪 Testando imports do sniffer...")
    
    try:
        from ferramentas.sniffer.sniffer import (
            PacketSniffer, get_network_interfaces, analyze_http_traffic, 
            analyze_dns_traffic, get_top_talkers, check_admin_privileges,
            get_network_interfaces_detailed, format_packet_info
        )
        print("✅ Todos os imports funcionaram!")
        
        # Testa criação de instância
        sniffer = PacketSniffer()
        print("✅ PacketSniffer criado")
        
        # Testa funções auxiliares
        interfaces = get_network_interfaces()
        print(f"✅ get_network_interfaces: {len(interfaces)} interfaces")
        
        admin = check_admin_privileges()
        print(f"✅ check_admin_privileges: {admin}")
        
        # Testa com dados vazios
        empty_packets = []
        http_traffic = analyze_http_traffic(empty_packets)
        dns_traffic = analyze_dns_traffic(empty_packets)
        top_talkers = get_top_talkers(empty_packets)
        
        print("✅ Funções de análise funcionaram")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("🔧 TESTE FINAL DAS CORREÇÕES")
    print("=" * 50)
    
    if test_imports():
        print("\n🎉 SUCESSO! Todas as correções funcionaram!")
        print("✅ O sniffer está pronto para uso.")
        print("✅ Agora você pode executar:")
        print("   - python run_integrated.py")
        print("   - Ou usar as tasks do VS Code")
    else:
        print("\n❌ Ainda há problemas com os imports")
        print("⚠️  Verifique os erros acima")
    
    input("\nPressione Enter para sair...")
