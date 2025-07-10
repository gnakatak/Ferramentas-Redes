#!/usr/bin/env python3
"""
Teste da nova detecção de interfaces no sniffer
"""

import sys
import os

# Adiciona o caminho do backend ao sys.path
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from ferramentas.sniffer.sniffer import get_network_interfaces_detailed, get_network_interfaces

def main():
    print("🌐 Teste da Nova Detecção de Interfaces")
    print("=" * 50)
    
    print("\n🔍 Interfaces Detalhadas:")
    detailed_interfaces = get_network_interfaces_detailed()
    
    for i, interface in enumerate(detailed_interfaces, 1):
        print(f"{i}. {interface['name']}")
        print(f"   IPs: {interface['ip_addresses']}")
        print(f"   Ativa: {'✅' if interface['is_up'] else '❌'}")
        if 'simplified_name' in interface:
            print(f"   Nome simplificado: {interface['simplified_name']}")
        print()
    
    print("\n🔍 Interfaces Simples:")
    simple_interfaces = get_network_interfaces()
    
    for i, interface in enumerate(simple_interfaces, 1):
        print(f"{i}. {interface['name']} - IPs: {interface['ip_addresses']}")
    
    print(f"\n📊 Total de interfaces detectadas: {len(detailed_interfaces)}")
    
    # Testa se pelo menos encontrou algumas interfaces comuns
    names = [iface['name'].lower() for iface in detailed_interfaces]
    
    if any('ethernet' in name for name in names):
        print("✅ Interface Ethernet detectada")
    if any(any(x in name for x in ['wi-fi', 'wifi', 'wireless']) for name in names):
        print("✅ Interface Wi-Fi detectada")
    if any('vpn' in name for name in names):
        print("✅ Interface VPN detectada")
    
    if len(detailed_interfaces) > 2:  # Mais que 'any' e 'localhost'
        print("✅ Detecção melhorada funcionando!")
    else:
        print("⚠️ Detecção limitada - usando fallback")

if __name__ == "__main__":
    main()
