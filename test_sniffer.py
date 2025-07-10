#!/usr/bin/env python3
"""
Exemplo de uso do Sniffer de Pacotes
Script para demonstrar as funcionalidades do sniffer
"""

import sys
import os
import time
import json
import argparse

# Adiciona o diretório backend ao path para importar os módulos
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend'))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from backend.ferramentas.sniffer.sniffer import (
    PacketSniffer,
    get_network_interfaces,
    format_packet_info,
    analyze_http_traffic,
    analyze_dns_traffic,
    get_top_talkers
)

def main():
    print("=== SNIFFER DE PACOTES ===\n")
    
    # Lista interfaces disponíveis
    print("1. Interfaces de rede disponíveis:")
    interfaces = get_network_interfaces()
    for i, interface in enumerate(interfaces):
        print(f"   {i+1}. {interface['name']}")
        for addr in interface['ip_addresses']:
            print(f"      {addr['type']}: {addr['address']}")
    
    if not interfaces:
        print("   Nenhuma interface encontrada!")
        return
    
    print("\n" + "="*50)
    
    # Escolhe uma interface (primeira disponível para exemplo)
    selected_interface = interfaces[0]['name']
    print(f"2. Usando interface: {selected_interface}")
    
    # Cria o sniffer
    sniffer = PacketSniffer(interface=selected_interface)
    
    try:
        print("\n3. Iniciando captura por 10 segundos...")
        print("   (Pressione Ctrl+C para parar antes)")
        
        # Inicia captura
        result = sniffer.start_capture(timeout=10)
        if "error" in result:
            print(f"   Erro: {result['error']}")
            return
        
        print("   Captura iniciada!")
        
        # Aguarda um pouco para capturar alguns pacotes
        time.sleep(2)
        
        # Mostra estatísticas durante a captura
        for i in range(8):
            stats = sniffer.get_statistics()
            print(f"   Pacotes capturados: {stats['total_packets']} "
                  f"({stats['packets_per_second']:.1f} pps)")
            time.sleep(1)
        
        # Para a captura
        sniffer.stop_capture()
        print("\n4. Captura finalizada!")
        
        # Estatísticas finais
        final_stats = sniffer.get_statistics()
        print(f"\nEstatísticas finais:")
        print(f"   Total de pacotes: {final_stats['total_packets']}")
        print(f"   Duração: {final_stats['duration']:.2f} segundos")
        print(f"   Taxa média: {final_stats['packets_per_second']:.2f} pps")
        
        # Protocolos encontrados
        if final_stats['protocols']:
            print(f"\nProtocolos encontrados:")
            for protocol, count in final_stats['protocols'].items():
                print(f"   {protocol}: {count} pacotes")
        
        # Mostra alguns pacotes capturados
        packets = sniffer.get_packets(limit=5)
        if packets:
            print(f"\nÚltimos 5 pacotes capturados:")
            for packet in packets[-5:]:
                formatted = format_packet_info(packet)
                print(f"   {formatted}")
        
        # Exporta para arquivo
        print(f"\n5. Exportando pacotes...")
        # Tráfego HTTP
        http_packets = analyze_http_traffic(packets)
        print(f"   Pacotes HTTP: {len(http_packets)}")
        
        # Tráfego HTTP
        # Importações relativas corrigidas para funcionar com o backend_path já adicionado ao sys.path
        # (Import já realizado no início do arquivo)

        http_packets = analyze_http_traffic(packets)
        print(f"   Pacotes HTTP: {len(http_packets)}")
        
        # Tráfego DNS
        dns_packets = analyze_dns_traffic(packets)
        print(f"   Pacotes DNS: {len(dns_packets)}")
        
        # Top talkers
        top_talkers = get_top_talkers(packets, limit=3)
        if top_talkers:
            print(f"   Top 3 IPs por tráfego:")
            for ip, bytes_count in top_talkers:
                print(f"     {ip}: {bytes_count} bytes")
        
        print(f"\n=== TESTE CONCLUÍDO ===")
        
    except KeyboardInterrupt:
        print(f"\n\nCaptura interrompida pelo usuário!")
        sniffer.stop_capture()
    except Exception as e:
        print(f"\nErro durante a execução: {e}")
        sniffer.stop_capture()

def test_without_capture():
    """
    Testa funcionalidades que não requerem captura real
    """
    print("=== TESTE SEM CAPTURA ===\n")
    
    print("1. Testando detecção de interfaces...")
    interfaces = get_network_interfaces()
    print(f"   Encontradas {len(interfaces)} interfaces")
    
    print("\n2. Testando criação do sniffer...")
    sniffer = PacketSniffer()
    print("   Sniffer criado com sucesso")
    
    print("\n3. Testando estatísticas iniciais...")
    stats = sniffer.get_statistics()
    print(f"   Status: {stats.get('error', 'OK')}")
    
    print("\n=== TESTE BÁSICO CONCLUÍDO ===")

if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description="Exemplo de uso do Sniffer")
    parser.add_argument('--no-capture', action='store_true', 
                       help='Executa apenas testes sem captura real')
    
    args = parser.parse_args()
    
    if args.no_capture:
        test_without_capture()
    else:
        main()
