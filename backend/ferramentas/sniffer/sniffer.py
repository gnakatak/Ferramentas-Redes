"""
Sniffer de pacotes usando subprocess para evitar problemas de event loop
"""
import subprocess
import psutil
import time
import tempfile
import os
from datetime import datetime

class PacketSnifferSubprocess:
    """Sniffer que usa tshark via subprocess para evitar event loop issues"""
    
    def __init__(self):
        self.packets = []
        self.start_time = None
        self.end_time = None
        self.stats = {}

    def get_network_interfaces(self):
        """Obtém interfaces de rede usando psutil"""
        try:
            interfaces = []
            network_interfaces = psutil.net_if_addrs()
            interface_stats = psutil.net_if_stats()
            
            print("🔧 Detectando interfaces de rede...")
            
            for interface_name, addresses in network_interfaces.items():
                try:
                    # Obtém estatísticas da interface
                    stats = interface_stats.get(interface_name, None)
                    is_up = stats.isup if stats else False
                    
                    # Determina tipo e status
                    interface_type = self._get_interface_type(interface_name)
                    status = "🟢 Ativa" if is_up else "🟡 Disponível"
                    
                    interface_info = {
                        'name': interface_name,
                        'id': interface_name,  # Para tshark, usamos o nome diretamente
                        'type': interface_type,
                        'status': status,
                        'is_up': is_up
                    }
                    
                    interfaces.append(interface_info)
                    
                    print(f"✅ Interface: {interface_type} - {interface_name} ({status})")
                    
                except Exception as e:
                    print(f"⚠️ Erro ao processar interface {interface_name}: {e}")
                    continue
            
            print(f"✅ Total: {len(interfaces)} interfaces detectadas")
            return interfaces
            
        except Exception as e:
            print(f"❌ Erro ao detectar interfaces: {e}")
            return []

    def _get_interface_type(self, interface_name):
        """Determina o tipo da interface baseado no nome"""
        name_lower = interface_name.lower()
        
        if 'wi-fi' in name_lower or 'wireless' in name_lower or 'wlan' in name_lower:
            return "📡 Wi-Fi"
        elif 'ethernet' in name_lower or 'local area' in name_lower:
            return "🌐 Ethernet"
        elif 'loopback' in name_lower:
            return "🔄 Loopback"
        elif 'vpn' in name_lower or 'tunnel' in name_lower:
            return "🔒 VPN/Tunnel"
        else:
            return "🔌 Rede"

    def start_capture(self, interface=None, packet_count=50, timeout=30, bpf_filter=None):
        """Inicia captura usando tshark com formato texto simples"""
        if not interface:
            raise ValueError("Interface não especificada")
        
        packet_count = max(int(packet_count or 50), 1)
        timeout = timeout or 30
        
        self.packets = []
        self.start_time = time.time()
        
        print(f"🔧 Iniciando captura - Interface: {interface}, Pacotes: {packet_count}")
        
        try:
            # Comando tshark simplificado - formato texto
            cmd = [
                'tshark',
                '-i', interface,
                '-c', str(packet_count),
                '-T', 'fields',
                '-e', 'frame.time_relative',
                '-e', 'frame.protocols', 
                '-e', 'ip.src',
                '-e', 'ip.dst',
                '-e', 'frame.len',
                '-e', 'tcp.srcport',
                '-e', 'tcp.dstport',
                '-e', 'udp.srcport', 
                '-e', 'udp.dstport',
                '-E', 'header=y',
                '-E', 'separator=|'
            ]
            
            # Adiciona filtro se especificado
            if bpf_filter:
                cmd.extend(['-f', bpf_filter])
            
            # Executa captura
            print(f"🔧 Executando captura com tshark...")
            
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=timeout,
                encoding='utf-8'
            )
            
            if result.returncode != 0:
                error_msg = result.stderr or "Erro no tshark"
                print(f"❌ Erro no tshark: {error_msg}")
                return self._fallback_capture(interface, packet_count, timeout)
            
            # Processa saída texto
            if result.stdout.strip():
                processed_packets = self._parse_tshark_output(result.stdout)
                self.packets = processed_packets
                print(f"📊 Processados {len(processed_packets)} pacotes")
            else:
                print("⚠️ Nenhum dado capturado, usando modo demonstração")
                return self._fallback_capture(interface, packet_count, timeout)
            
            self.end_time = time.time()
            duration = self.end_time - self.start_time
            
            print(f"✅ Captura finalizada - {len(self.packets)} pacotes em {duration:.2f}s")
            
            return {
                'packets': self.packets,
                'stats': self.get_statistics(),
                'duration': duration
            }
            
        except subprocess.TimeoutExpired:
            print(f"⚠️ Timeout na captura após {timeout}s")
            return {
                'packets': self.packets,
                'stats': self.get_statistics(),
                'duration': timeout,
                'timeout': True
            }
        except FileNotFoundError:
            print("❌ tshark não encontrado. Usando modo demonstração...")
            return self._fallback_capture(interface, packet_count, timeout)
        except Exception as e:
            print(f"❌ Erro durante captura: {e}")
            return self._fallback_capture(interface, packet_count, timeout)

    def _parse_tshark_output(self, output):
        """Processa saída do tshark em formato de campos separados"""
        packets = []
        lines = output.strip().split('\n')
        
        # Pula a linha de cabeçalho se existir
        for line_num, line in enumerate(lines):
            if line.startswith('frame.time_relative') or not line.strip():
                continue
                
            try:
                # Separa campos por |
                fields = line.split('|')
                
                # Garante que temos campos suficientes
                while len(fields) < 8:
                    fields.append('')
                
                time_rel = fields[0].strip() if fields[0] else '0'
                protocols = fields[1].strip() if fields[1] else 'Unknown'
                ip_src = fields[2].strip() if fields[2] else 'N/A'
                ip_dst = fields[3].strip() if fields[3] else 'N/A'
                frame_len = fields[4].strip() if fields[4] else '0'
                tcp_srcport = fields[5].strip() if fields[5] else ''
                tcp_dstport = fields[6].strip() if fields[6] else ''
                udp_srcport = fields[7].strip() if fields[7] else ''
                udp_dstport = fields[8].strip() if len(fields) > 8 and fields[8] else ''
                
                # Determina protocolo principal
                protocol = self._extract_main_protocol(protocols)
                
                # Formata endereços com portas se disponível
                src_addr = ip_src
                dst_addr = ip_dst
                
                if protocol == 'TCP' and tcp_srcport and tcp_dstport:
                    src_addr = f"{ip_src}:{tcp_srcport}" if ip_src != 'N/A' else f":{tcp_srcport}"
                    dst_addr = f"{ip_dst}:{tcp_dstport}" if ip_dst != 'N/A' else f":{tcp_dstport}"
                elif protocol == 'UDP' and udp_srcport and udp_dstport:
                    src_addr = f"{ip_src}:{udp_srcport}" if ip_src != 'N/A' else f":{udp_srcport}"
                    dst_addr = f"{ip_dst}:{udp_dstport}" if ip_dst != 'N/A' else f":{udp_dstport}"
                
                packet_info = {
                    'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3],
                    'protocol': protocol,
                    'src': src_addr,
                    'dst': dst_addr,
                    'length': frame_len,
                    'info': f"{protocol} packet",
                    'protocols_full': protocols
                }
                
                packets.append(packet_info)
                
            except Exception as e:
                print(f"⚠️ Erro ao processar linha {line_num}: {e}")
                # Adiciona pacote básico em caso de erro
                packets.append({
                    'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3],
                    'protocol': 'Unknown',
                    'src': 'N/A',
                    'dst': 'N/A',
                    'length': '0',
                    'info': 'Parse error'
                })
                continue
        
        print(f"📝 Parsados {len(packets)} pacotes de {len(lines)} linhas")
        return packets

    def _extract_main_protocol(self, protocols_str):
        """Extrai o protocolo principal da string de protocolos"""
        if not protocols_str:
            return 'Unknown'
        
        protocols_lower = protocols_str.lower()
        
        # Ordem de prioridade dos protocolos
        if 'tcp' in protocols_lower:
            return 'TCP'
        elif 'udp' in protocols_lower:
            return 'UDP'
        elif 'icmp' in protocols_lower:
            return 'ICMP'
        elif 'arp' in protocols_lower:
            return 'ARP'
        elif 'dns' in protocols_lower:
            return 'DNS'
        elif 'http' in protocols_lower:
            return 'HTTP'
        elif 'https' in protocols_lower or 'tls' in protocols_lower:
            return 'HTTPS'
        elif 'ip' in protocols_lower:
            return 'IP'
        else:
            # Retorna o primeiro protocolo da lista
            first_protocol = protocols_str.split(':')[0].strip()
            return first_protocol.upper() if first_protocol else 'Unknown'

    def _fallback_capture(self, interface, packet_count, timeout):
        """Método de fallback para captura básica"""
        print("🔄 Usando método de captura alternativo...")
        
        try:
            # Gera pacotes simulados para demonstração
            fake_packets = []
            for i in range(min(packet_count, 10)):
                fake_packet = {
                    'timestamp': datetime.now().strftime('%H:%M:%S.%f')[:-3],
                    'protocol': ['TCP', 'UDP', 'ICMP', 'ARP'][i % 4],
                    'src': f"192.168.1.{100 + i}",
                    'dst': f"192.168.1.{200 + i}",
                    'length': f"{64 + i * 10}",
                    'info': f"Demo packet {i + 1}"
                }
                fake_packets.append(fake_packet)
            
            self.packets = fake_packets
            self.end_time = time.time()
            
            print(f"✅ Captura de demonstração - {len(fake_packets)} pacotes simulados")
            
            return {
                'packets': self.packets,
                'stats': self.get_statistics(),
                'duration': (self.end_time - self.start_time) if self.start_time else 0,
                'demo_mode': True
            }
            
        except Exception as e:
            print(f"❌ Erro no método alternativo: {e}")
            return {
                'packets': [],
                'stats': {},
                'error': str(e)
            }

    def get_statistics(self):
        """Retorna estatísticas da captura"""
        if not self.packets:
            return {}
        
        stats = {
            'total_packets': len(self.packets),
            'protocols': {},
            'duration': self.end_time - self.start_time if self.end_time and self.start_time else 0
        }
        
        # Conta protocolos
        for packet in self.packets:
            protocol = packet.get('protocol', 'Unknown')
            stats['protocols'][protocol] = stats['protocols'].get(protocol, 0) + 1
        
        return stats

    def stop_capture(self):
        """Para a captura (para compatibilidade)"""
        self.end_time = time.time()
        print("🔴 Captura interrompida")

# Função para compatibilidade
def get_network_interfaces():
    """Função de compatibilidade para obter interfaces"""
    sniffer = PacketSnifferSubprocess()
    return sniffer.get_network_interfaces()

# Alias para compatibilidade
PacketSniffer = PacketSnifferSubprocess
