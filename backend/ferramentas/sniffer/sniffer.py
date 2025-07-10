"""
Sniffer de Pacotes
Ferramenta para captura e análise de tráfego de rede usando PyShark
"""

import threading
import time
import os
import socket
from datetime import datetime
from collections import defaultdict
import json
import subprocess
import platform

try:
    import pyshark
    PYSHARK_AVAILABLE = True
except ImportError:
    PYSHARK_AVAILABLE = False
    print("PyShark não está disponível. Instale com: pip install pyshark")

class PacketSniffer:
    """
    Classe principal para captura e análise de pacotes de rede usando PyShark
    """
    
    def __init__(self, interface=None, filter_expr=None):
        """
        Inicializa o sniffer
        
        Args:
            interface (str): Interface de rede para capturar (ex: 'eth0', 'wlan0')
            filter_expr (str): Filtro de captura (ex: 'tcp port 80', 'udp')
        """
        self.interface = interface
        self.filter_expr = filter_expr
        self.is_running = False
        self.captured_packets = []
        self.packet_stats = defaultdict(int)
        self.protocols = defaultdict(int)
        self.start_time = None
        self.stop_time = None
        self.capture_thread = None
        self.max_packets = 1000  # Limite de pacotes para evitar uso excessivo de memória
        self.capture = None
        
    def _get_available_interfaces(self):
        """
        Obtém lista de interfaces disponíveis para PyShark
        
        Returns:
            list: Lista de nomes de interfaces
        """
        try:
            if PYSHARK_AVAILABLE:
                # Tenta obter interfaces via PyShark
                import pyshark
                # Interface padrão sempre disponível
                interfaces = ['any']
                
                # Tenta detectar outras interfaces
                try:
                    # Método alternativo usando get_network_interfaces
                    detected = get_network_interfaces()
                    for iface in detected:
                        name = iface.get('name', '')
                        if name and name not in interfaces:
                            interfaces.append(name)
                except:
                    pass
                
                return interfaces
            else:
                return ['any']
        except Exception:
            return ['any']
        
    def start_capture(self, packet_count=0, timeout=None):
        """
        Inicia a captura de pacotes com fallback para subprocess
        
        Args:
            packet_count (int): Número máximo de pacotes a capturar (0 = ilimitado)
            timeout (int): Timeout em segundos (None = sem timeout)
            
        Returns:
            dict: Status da operação
        """
        if self.is_running:
            return {"error": "Captura já está em execução"}
        
        # Tenta método PyShark primeiro
        if PYSHARK_AVAILABLE:
            print("🎯 Tentando captura com PyShark...")
            
            # Verifica se a interface existe
            if self.interface and self.interface != 'any':
                available_interfaces = self._get_available_interfaces()
                if self.interface not in available_interfaces:
                    print(f"⚠️ Interface '{self.interface}' não encontrada")
                    print(f"   Interfaces disponíveis: {', '.join(available_interfaces)}")
                    print("   Usando interface 'any' como fallback")
                    self.interface = 'any'
            
            try:
                # Inicializa estado da captura
                self.is_running = True
                self.start_time = datetime.now()
                self.captured_packets = []
                self.packet_stats = defaultdict(int)
                self.protocols = defaultdict(int)
                
                # Inicia thread de captura com método totalmente síncrono
                self.capture_thread = threading.Thread(
                    target=self._capture_packets_sync,
                    args=(packet_count or 50, timeout or 30)  # Limites padrão
                )
                self.capture_thread.daemon = True
                self.capture_thread.start()
                
                # Aguarda um pouco para verificar se a thread funcionou
                time.sleep(1)
                if not self.capture_thread.is_alive() and not self.captured_packets:
                    raise Exception("Thread PyShark falhou rapidamente")
                
                return {"message": "Captura PyShark iniciada com sucesso"}
                
            except Exception as e:
                print(f"❌ PyShark falhou: {e}")
                self.is_running = False
                print("🔄 Tentando método subprocess...")
        
        # Fallback para subprocess (tshark)
        print("🚀 Usando método subprocess como fallback...")
        return self.start_capture_subprocess(
            packet_count=packet_count or 10,
            timeout=timeout or 30
        )
    
    def _capture_packets_sync(self, packet_count, timeout):
        """
        Método totalmente síncrono para capturar pacotes
        Funciona de forma estável em Flask e Streamlit
        """
        import asyncio
        import threading
        
        count = 0
        start_time = time.time()
        capture = None
        
        try:
            # CORREÇÃO: Configura event loop para thread
            try:
                loop = asyncio.get_event_loop()
            except RuntimeError:
                # Se não há event loop, cria um novo
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                print("✅ Event loop criado para thread")
            
            print(f"🔧 DEBUG: Iniciando captura")
            print(f"   - Interface: {self.interface}")
            print(f"   - Filtro: {self.filter_expr}")
            print(f"   - Max pacotes: {packet_count}")
            print(f"   - Timeout: {timeout}s")
            
            # Configurações de captura simples
            capture_args = {}
            
            # CORREÇÃO: No Windows, usar interface numérica ou None para auto
            if self.interface and self.interface != 'any':
                # Tenta mapear nome para número de interface
                interface_to_use = self._map_interface_name(self.interface)
                if interface_to_use:
                    capture_args['interface'] = interface_to_use
                    print(f"✓ Usando interface específica: {interface_to_use}")
                else:
                    print(f"⚠️ Interface '{self.interface}' não mapeada, usando auto-detect")
            else:
                print("✓ Usando interface padrão (auto-detect)")
            
            if self.filter_expr:
                capture_args['bpf_filter'] = self.filter_expr
                print(f"✓ Aplicando filtro BPF: {self.filter_expr}")
            else:
                print("✓ Sem filtros (captura tudo)")
            
            # CORREÇÃO: Adiciona configurações mais robustas
            capture_args['use_json'] = True  # Força JSON output
            capture_args['include_raw'] = False  # Reduz overhead
            
            # Cria captura com event loop explícito
            print("🔨 Criando LiveCapture...")
            capture_args['eventloop'] = loop
            capture = pyshark.LiveCapture(**capture_args)
            self.capture = capture
            print("✅ LiveCapture criado com sucesso")
            
            # Estratégia mais agressiva de captura
            print("📡 Iniciando captura contínua...")
            
            # Método 1: Tentar sniff_continuously primeiro
            try:
                print("🎯 Tentativa 1: sniff_continuously")
                packet_iterator = capture.sniff_continuously()
                
                for packet in packet_iterator:
                    if not self.is_running:
                        print("🛑 Captura interrompida pelo usuário")
                        break
                    
                    try:
                        print(f"📦 Processando pacote {count + 1}: {str(packet)[:100]}...")
                        self._process_packet(packet)
                        count += 1
                        
                        # Limita pacotes em memória
                        if len(self.captured_packets) > self.max_packets:
                            self.captured_packets.pop(0)
                            
                    except Exception as e:
                        print(f"⚠️ Erro ao processar pacote: {e}")
                        continue
                    
                    # Verifica limites
                    if packet_count > 0 and count >= packet_count:
                        print(f"🎯 Limite de {packet_count} pacotes atingido")
                        break
                    
                    if timeout and (time.time() - start_time) >= timeout:
                        print(f"⏰ Timeout de {timeout}s atingido")
                        break
                        
            except Exception as e1:
                error_msg = str(e1) if str(e1).strip() else "Erro desconhecido ou permissão insuficiente"
                print(f"❌ sniff_continuously falhou: {error_msg}")
                print("🔄 Tentativa 2: sniff com timeout")
                
                # Método 2: Fallback para sniff com timeout
                try:
                    attempts = 0
                    max_attempts = 10
                    consecutive_errors = 0
                    
                    while self.is_running and (time.time() - start_time) < (timeout or 300) and attempts < max_attempts:
                        attempts += 1
                        try:
                            print(f"🔍 Tentativa {attempts}/{max_attempts} - Capturando...")
                            packets = capture.sniff(timeout=3, packet_count=5)
                            
                            # Reset contador de erros em caso de sucesso
                            consecutive_errors = 0
                            
                            # Conversão defensiva para garantir iterabilidade
                            if packets is not None:
                                try:
                                    packet_list = list(packets) if hasattr(packets, '__iter__') else []
                                except (TypeError, ValueError):
                                    packet_list = []
                                    
                                if packet_list:
                                    print(f"📦 Batch {attempts}: {len(packet_list)} pacotes capturados")
                                    for packet in packet_list:
                                        if not self.is_running:
                                            break
                                        try:
                                            self._process_packet(packet)
                                            count += 1
                                            print(f"✅ Pacote {count} processado")
                                            if len(self.captured_packets) > self.max_packets:
                                                self.captured_packets.pop(0)
                                        except Exception as e:
                                            print(f"⚠️ Erro ao processar pacote {count}: {e}")
                                            continue
                                else:
                                    print(f"ℹ️ Batch {attempts}: Nenhum pacote capturado")
                            else:
                                print(f"ℹ️ Batch {attempts}: Sniff retornou None")
                                        
                            # Verifica limite
                            if packet_count > 0 and count >= packet_count:
                                print(f"🎯 Meta de {packet_count} pacotes atingida")
                                break
                                
                        except Exception as e2:
                            consecutive_errors += 1
                            error_msg = str(e2) if str(e2).strip() else "Erro vazio (possível problema de permissão)"
                            
                            if "timeout" not in error_msg.lower():
                                print(f"⚠️ Erro na tentativa {attempts}: {error_msg}")
                                
                                # Se muitos erros consecutivos, para
                                if consecutive_errors >= 5:
                                    print("❌ Muitos erros consecutivos - abortando método PyShark")
                                    break
                            
                            time.sleep(1)
                            
                except Exception as e3:
                    error_msg = str(e3) if str(e3).strip() else "Erro grave no PyShark"
                    print(f"❌ Método batch também falhou: {error_msg}")
                    print("🔄 Tentando fallback para subprocess...")
                
            # Se chegou aqui e não capturou nada, tenta subprocess automaticamente
            if count == 0:
                print("⚠️ PyShark não capturou nenhum pacote")
                print("🔄 Iniciando fallback automático para subprocess...")
                
                # Para o PyShark primeiro
                if capture:
                    try:
                        capture.close()
                    except:
                        pass
                
                # Reset do estado para subprocess
                self.is_running = True
                
                # Chama subprocess de forma síncrona na mesma thread
                try:
                    subprocess_result = self._capture_via_subprocess(packet_count or 10, timeout or 30)
                    if subprocess_result:
                        count = len(self.captured_packets)
                        print(f"✅ Fallback subprocess capturou {count} pacotes")
                    else:
                        print("❌ Fallback subprocess também falhou")
                except Exception as e_sub:
                    print(f"❌ Erro no fallback subprocess: {e_sub}")
                
        except KeyboardInterrupt:
            print("⏹️ Captura interrompida manualmente")
        except Exception as e:
            print(f"❌ Erro geral na captura: {e}")
            import traceback
            traceback.print_exc()
        finally:
            print(f"🏁 Finalizando captura. Pacotes capturados: {count}")
            self.is_running = False
            self.stop_time = datetime.now()
            if capture:
                try:
                    capture.close()
                    print("✅ Captura fechada")
                except Exception as e:
                    print(f"⚠️ Erro ao fechar captura: {e}")
            self.capture = None
            
            # Cleanup do event loop se foi criado nesta thread
            try:
                current_loop = asyncio.get_event_loop()
                if current_loop and not current_loop.is_running():
                    current_loop.close()
                    print("✅ Event loop fechado")
            except Exception as e:
                print(f"⚠️ Erro ao fechar event loop: {e}")
    
    def _process_packet(self, packet):
        """
        Processa um pacote capturado
        """
        try:
            packet_info = {
                'timestamp': datetime.now(),
                'length': int(packet.length) if hasattr(packet, 'length') else 0,
                'protocol': self._get_highest_protocol(packet),
                'src_ip': None,
                'dst_ip': None,
                'src_port': None,
                'dst_port': None,
                'info': str(packet)[:200]  # Limita o tamanho da informação
            }
            
            # Extrai informações de IP
            if hasattr(packet, 'ip'):
                packet_info['src_ip'] = packet.ip.src
                packet_info['dst_ip'] = packet.ip.dst
            
            # Extrai informações de porta (TCP/UDP)
            if hasattr(packet, 'tcp'):
                packet_info['src_port'] = int(packet.tcp.srcport)
                packet_info['dst_port'] = int(packet.tcp.dstport)
            elif hasattr(packet, 'udp'):
                packet_info['src_port'] = int(packet.udp.srcport)
                packet_info['dst_port'] = int(packet.udp.dstport)
            
            # Adiciona à lista
            self.captured_packets.append(packet_info)
            
            # Atualiza estatísticas
            self.packet_stats['total_packets'] += 1
            self.protocols[packet_info['protocol']] += 1
            
        except Exception as e:
            print(f"Erro ao processar pacote: {e}")
    
    def _get_highest_protocol(self, packet):
        """
        Determina o protocolo de mais alto nível do pacote
        """
        try:
            # Lista de protocolos em ordem de prioridade
            protocols = ['http', 'https', 'dns', 'tcp', 'udp', 'icmp', 'arp', 'ip']
            
            for proto in protocols:
                if hasattr(packet, proto):
                    return proto.upper()
            
            return 'UNKNOWN'
        except:
            return 'UNKNOWN'
    
    def stop_capture(self):
        """
        Para a captura de pacotes
        
        Returns:
            dict: Status da operação
        """
        if not self.is_running:
            return {"message": "Captura não estava em execução"}
        
        self.is_running = False
        self.stop_time = datetime.now()
        
        if self.capture:
            try:
                self.capture.close()
            except:
                pass
        
        if self.capture_thread and self.capture_thread.is_alive():
            self.capture_thread.join(timeout=2)
        
        return {"message": "Captura finalizada"}
    
    def get_packets(self, limit=None):
        """
        Retorna os pacotes capturados
        
        Args:
            limit (int): Número máximo de pacotes a retornar
            
        Returns:
            list: Lista de pacotes
        """
        if limit:
            return self.captured_packets[-limit:]
        return self.captured_packets.copy()
    
    def get_statistics(self):
        """
        Retorna estatísticas da captura
        
        Returns:
            dict: Estatísticas
        """
        duration = 0
        if self.start_time:
            end_time = self.stop_time or datetime.now()
            duration = (end_time - self.start_time).total_seconds()
        
        total_packets = self.packet_stats.get('total_packets', 0)
        packets_per_second = total_packets / duration if duration > 0 else 0
        
        return {
            'total_packets': total_packets,
            'duration': duration,
            'packets_per_second': packets_per_second,
            'protocols': dict(self.protocols),
            'is_running': self.is_running
        }
    
    def export_packets(self, format='json', filename=None):
        """
        Exporta pacotes capturados
        
        Args:
            format (str): Formato de exportação ('json', 'csv')
            filename (str): Nome do arquivo (opcional)
            
        Returns:
            dict: Status da operação
        """
        if not self.captured_packets:
            return {"error": "Nenhum pacote foi capturado"}
        
        if not filename:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"packets_{timestamp}.{format}"
        
        try:
            if format.lower() == 'json':
                # Converte datetime para string para serialização JSON
                packets_for_export = []
                for packet in self.captured_packets:
                    packet_copy = packet.copy()
                    packet_copy['timestamp'] = packet_copy['timestamp'].isoformat()
                    packets_for_export.append(packet_copy)
                
                with open(filename, 'w', encoding='utf-8') as f:
                    json.dump(packets_for_export, f, indent=2, ensure_ascii=False)
                
                return {"message": f"Pacotes exportados para {filename}"}
            
            elif format.lower() == 'csv':
                import csv
                with open(filename, 'w', newline='', encoding='utf-8') as f:
                    writer = csv.writer(f)
                    # Cabeçalho
                    writer.writerow(['timestamp', 'protocol', 'src_ip', 'dst_ip', 
                                   'src_port', 'dst_port', 'length', 'info'])
                    
                    # Dados
                    for packet in self.captured_packets:
                        writer.writerow([
                            packet['timestamp'].isoformat(),
                            packet['protocol'],
                            packet['src_ip'],
                            packet['dst_ip'],
                            packet['src_port'],
                            packet['dst_port'],
                            packet['length'],
                            packet['info']
                        ])
                
                return {"message": f"Pacotes exportados para {filename}"}
            
            else:
                return {"error": f"Formato não suportado: {format}"}
                
        except Exception as e:
            return {"error": f"Erro ao exportar: {str(e)}"}

    def _find_tshark_path(self):
        """
        Encontra o caminho do tshark no sistema
        
        Returns:
            str: Caminho para tshark ou 'tshark' se não encontrar
        """
        system = platform.system()
        
        if system == "Windows":
            # Possíveis localizações do tshark no Windows
            possible_paths = [
                "C:\\Program Files\\Wireshark\\tshark.exe",
                "C:\\Program Files (x86)\\Wireshark\\tshark.exe",
                "C:\\Program Files\\Wireshark\\tshark.exe",
                os.path.expanduser("~\\AppData\\Local\\Programs\\Wireshark\\tshark.exe"),
                # Verifica no PATH
                "tshark.exe",
                "tshark"
            ]
            
            for path in possible_paths:
                if path in ["tshark.exe", "tshark"]:
                    # Testa se está no PATH
                    try:
                        result = subprocess.run([path, '--version'], 
                                              capture_output=True, timeout=3)
                        if result.returncode == 0:
                            return path
                    except:
                        continue
                else:
                    # Verifica se arquivo existe
                    if os.path.exists(path):
                        return path
            
            # Se não encontrou, tenta buscar no registro do Windows
            try:
                import winreg
                with winreg.OpenKey(winreg.HKEY_LOCAL_MACHINE, 
                                  r"SOFTWARE\Microsoft\Windows\CurrentVersion\Uninstall") as key:
                    for i in range(winreg.QueryInfoKey(key)[0]):
                        try:
                            subkey_name = winreg.EnumKey(key, i)
                            with winreg.OpenKey(key, subkey_name) as subkey:
                                try:
                                    display_name = winreg.QueryValueEx(subkey, "DisplayName")[0]
                                    if "Wireshark" in display_name:
                                        install_location = winreg.QueryValueEx(subkey, "InstallLocation")[0]
                                        tshark_path = os.path.join(install_location, "tshark.exe")
                                        if os.path.exists(tshark_path):
                                            return tshark_path
                                except:
                                    continue
                        except:
                            continue
            except ImportError:
                pass  # winreg não disponível
            
        elif system in ["Linux", "Darwin"]:
            # Unix-like systems
            possible_paths = [
                "/usr/bin/tshark",
                "/usr/local/bin/tshark",
                "/opt/homebrew/bin/tshark",  # macOS with Homebrew
                "tshark"
            ]
            
            for path in possible_paths:
                if path == "tshark":
                    try:
                        result = subprocess.run([path, '--version'], 
                                              capture_output=True, timeout=3)
                        if result.returncode == 0:
                            return path
                    except:
                        continue
                else:
                    if os.path.exists(path):
                        return path
        
        # Fallback - retorna tshark e deixa o sistema resolver
        return "tshark"

    def _capture_via_subprocess(self, packet_count=10, timeout=30):
        """
        Método interno para captura via subprocess (síncrono) com fallbacks inteligentes
        
        Args:
            packet_count (int): Número de pacotes a capturar
            timeout (int): Timeout em segundos
            
        Returns:
            bool: True se capturou pacotes, False caso contrário
        """
        try:
            print(f"🚀 Executando captura subprocess (tshark)")
            print(f"   - Pacotes: {packet_count}")
            print(f"   - Timeout: {timeout}s")
            
            # Encontra o caminho do tshark
            tshark_path = self._find_tshark_path()
            print(f"🔧 Usando tshark: {tshark_path}")
            
            # Lista de interfaces para tentar (priorizando Wi-Fi e Ethernet)
            interfaces_to_try = []
            
            # CORREÇÃO: Interface - sempre especifica uma interface
            if self.interface and self.interface not in ['any', 'auto']:
                # Mapeia nome para interface real
                mapped_interface = self._get_tshark_interface(self.interface)
                if mapped_interface:
                    interfaces_to_try.append(mapped_interface)
                    print(f"🔧 Interface mapeada: {self.interface} -> {mapped_interface}")
            
            # Adiciona interfaces ativas conhecidas como prioridade
            for priority_interface in ['4', '9']:  # 4=Wi-Fi, 9=Ethernet
                if priority_interface not in interfaces_to_try:
                    interfaces_to_try.append(priority_interface)
            
            # Adiciona primeira interface disponível como fallback
            first_interface = self._get_first_available_interface()
            if first_interface and first_interface not in interfaces_to_try:
                interfaces_to_try.append(first_interface)
                print(f"🔧 Adicionando interface fallback: {first_interface}")
            
            # Adiciona outras interfaces comuns como fallback adicional
            for common_interface in ['1', '2', '3', '5', '6', '7', '8']:
                if common_interface not in interfaces_to_try:
                    interfaces_to_try.append(common_interface)
            
            # Tenta cada interface até encontrar uma que funcione
            for interface in interfaces_to_try:
                print(f"🎯 Tentando interface: {interface}")
                
                # Constrói comando tshark
                cmd = [tshark_path, '-i', interface]
                
                # Filtro
                if self.filter_expr:
                    cmd.extend(['-f', self.filter_expr])
                
                # Configurações
                cmd.extend([
                    '-c', str(packet_count),  # Número de pacotes
                    '-T', 'json',             # Saída em JSON
                    '-t', 'a',                # Timestamp absoluto
                    '-l'                      # Line buffered output
                ])
                
                print(f"🔧 Comando: {' '.join(cmd)}")
                
                try:
                    # Primeiro faz um teste rápido com timeout menor e menos pacotes
                    test_timeout = min(10, timeout // 3)  # Timeout reduzido para teste
                    test_packets = min(3, packet_count)   # Menos pacotes para teste
                    
                    # CORREÇÃO: Constrói comando de teste corretamente
                    test_cmd = [tshark_path, '-i', interface, '-c', str(test_packets), '-T', 'json', '-t', 'a', '-l']
                    
                    # Filtro (se houver)
                    if self.filter_expr:
                        test_cmd.extend(['-f', self.filter_expr])
                    
                    print(f"🧪 Teste rápido: {test_packets} pacotes, {test_timeout}s timeout")
                    print(f"🔧 Comando teste: {' '.join(test_cmd)}")
                    
                    # Executa teste
                    result = subprocess.run(
                        test_cmd,
                        capture_output=True,
                        text=True,
                        timeout=test_timeout
                    )
                    
                    if result.returncode == 0:
                        print(f"✅ Interface {interface} funcionou no teste!")
                        
                        # Se o teste funcionou, executa captura completa
                        if result.stdout and result.stdout.strip():
                            print("✅ Teste capturou dados, executando captura completa...")
                            
                            # Executa captura completa
                            result = subprocess.run(
                                cmd,
                                capture_output=True,
                                text=True,
                                timeout=timeout
                            )
                        
                        if result.returncode == 0 and result.stdout:
                            print("✅ Captura subprocess concluída")
                            self._process_tshark_output(result.stdout)
                            return len(self.captured_packets) > 0
                        else:
                            print(f"⚠️ Interface {interface} teste OK, mas captura completa falhou")
                            continue
                    else:
                        print(f"⚠️ Interface {interface} falhou no teste: {result.stderr[:100]}")
                        continue
                        
                except subprocess.TimeoutExpired:
                    print(f"⏰ Timeout na interface {interface}")
                    continue
                except Exception as e:
                    print(f"⚠️ Erro na interface {interface}: {e}")
                    continue
            
            print("❌ Todas as interfaces falharam")
            return False
                
        except FileNotFoundError:
            print("❌ tshark não encontrado. Instale o Wireshark.")
            return False
        except Exception as e:
            print(f"❌ Erro no subprocess: {e}")
            return False

    def start_capture_subprocess(self, packet_count=10, timeout=30):
        """
        Método alternativo de captura usando subprocess para evitar problemas de event loop
        
        Args:
            packet_count (int): Número máximo de pacotes a capturar
            timeout (int): Timeout em segundos
            
        Returns:
            dict: Status da operação
        """
        if self.is_running:
            return {"error": "Captura já está em execução"}
        
        try:
            import subprocess
            import json
            
            self.is_running = True
            self.start_time = datetime.now()
            self.captured_packets = []
            self.packet_stats = defaultdict(int)
            self.protocols = defaultdict(int)
            
            print(f"🚀 Iniciando captura via subprocess (tshark)")
            print(f"   - Pacotes: {packet_count}")
            print(f"   - Timeout: {timeout}s")
            print(f"   - Interface: {self.interface or 'auto'}")
            
            # Encontra o caminho do tshark
            tshark_path = self._find_tshark_path()
            print(f"🔧 Usando tshark: {tshark_path}")
            
            # Constrói comando tshark
            cmd = [tshark_path]
            
            # Interface
            if self.interface and self.interface != 'any':
                cmd.extend(['-i', self.interface])
            else:
                cmd.extend(['-i', 'any'])
            
            # Filtro
            if self.filter_expr:
                cmd.extend(['-f', self.filter_expr])
            
            # Configurações
            cmd.extend([
                '-c', str(packet_count),  # Número de pacotes
                '-T', 'json',             # Saída em JSON
                '-t', 'a',                # Timestamp absoluto
            ])
            
            print(f"🔧 Comando: {' '.join(cmd)}")
            
            # Executa captura em thread
            def run_subprocess():
                try:
                    result = subprocess.run(
                        cmd,
                        capture_output=True,
                        text=True,
                        timeout=timeout
                    )
                    
                    if result.returncode == 0:
                        print("✅ Captura concluída com sucesso")
                        self._process_tshark_output(result.stdout)
                    else:
                        print(f"❌ tshark falhou: {result.stderr}")
                        print(f"   Return code: {result.returncode}")
                        
                except subprocess.TimeoutExpired:
                    print("⏰ Timeout na captura")
                except FileNotFoundError:
                    print("❌ tshark não encontrado. Instale o Wireshark.")
                except Exception as e:
                    print(f"❌ Erro no subprocess: {e}")
                finally:
                    self.is_running = False
                    self.stop_time = datetime.now()
            
            # Inicia thread
            self.capture_thread = threading.Thread(target=run_subprocess)
            self.capture_thread.daemon = True
            self.capture_thread.start()
            
            return {"message": "Captura subprocess iniciada com sucesso"}
            
        except Exception as e:
            self.is_running = False
            return {"error": f"Erro ao iniciar captura subprocess: {str(e)}"}
    
    def _process_tshark_output(self, json_output):
        """
        Processa a saída JSON do tshark
        
        Args:
            json_output (str): Saída JSON do tshark
        """
        try:
            import json
            
            # CORREÇÃO: O tshark retorna um array JSON, não linhas separadas
            json_output = json_output.strip()
            
            # Remove possível texto de status inicial
            if json_output.startswith('[Capturing on'):
                lines = json_output.split('\n')
                # Encontra onde começa o JSON real (geralmente com '[')
                json_start = -1
                for i, line in enumerate(lines):
                    if line.strip().startswith('['):
                        json_start = i
                        break
                
                if json_start >= 0:
                    json_output = '\n'.join(lines[json_start:])
            
            # Tenta parsear como array JSON completo
            try:
                if json_output.startswith('[') and json_output.endswith(']'):
                    packets_data = json.loads(json_output)
                    processed_count = 0
                    
                    for packet_data in packets_data:
                        processed_packet = self._parse_tshark_packet(packet_data)
                        
                        if processed_packet:
                            self.captured_packets.append(processed_packet)
                            
                            # Atualiza estatísticas
                            protocol = processed_packet.get('protocol', 'UNKNOWN')
                            self.protocols[protocol] += 1
                            self.packet_stats['total_packets'] += 1
                            
                            processed_count += 1
                            
                            # Limita pacotes em memória
                            if len(self.captured_packets) > self.max_packets:
                                self.captured_packets.pop(0)
                    
                    print(f"✅ Processados {processed_count} pacotes do array JSON")
                    return
                    
            except json.JSONDecodeError:
                print("⚠️ Não é um array JSON válido, tentando linha por linha...")
            
            # Fallback: tenta linha por linha (formato antigo)
            lines = json_output.strip().split('\n')
            processed_count = 0
            
            for line in lines:
                if not line.strip():
                    continue
                
                try:
                    packet_data = json.loads(line)
                    processed_packet = self._parse_tshark_packet(packet_data)
                    
                    if processed_packet:
                        self.captured_packets.append(processed_packet)
                        
                        # Atualiza estatísticas
                        protocol = processed_packet.get('protocol', 'UNKNOWN')
                        self.protocols[protocol] += 1
                        self.packet_stats['total_packets'] += 1
                        
                        processed_count += 1
                        
                        # Limita pacotes em memória
                        if len(self.captured_packets) > self.max_packets:
                            self.captured_packets.pop(0)
                        
                except json.JSONDecodeError as e:
                    # Ignora linhas que não são JSON válido (como status do tshark)
                    continue
                except Exception as e:
                    print(f"⚠️ Erro ao processar pacote: {e}")
                    continue
            
            print(f"✅ Processados {processed_count} pacotes (linha por linha)")
            
        except Exception as e:
            print(f"❌ Erro ao processar saída do tshark: {e}")
    
    def _parse_tshark_packet(self, packet_data):
        """
        Converte dados do tshark para formato interno
        
        Args:
            packet_data (dict): Dados do pacote do tshark
            
        Returns:
            dict: Pacote no formato interno
        """
        try:
            layers = packet_data.get('_source', {}).get('layers', {})
            
            # Informações básicas
            frame = layers.get('frame', {})
            timestamp_str = frame.get('frame.time_epoch', '')
            
            if timestamp_str:
                timestamp = datetime.fromtimestamp(float(timestamp_str))
            else:
                timestamp = datetime.now()
            
            length = int(frame.get('frame.len', 0))
            
            # Protocolo
            protocols = frame.get('frame.protocols', '').split(':')
            highest_protocol = protocols[-1].upper() if protocols else 'UNKNOWN'
            
            # IPs
            src_ip = None
            dst_ip = None
            
            if 'ip' in layers:
                ip = layers['ip']
                src_ip = ip.get('ip.src')
                dst_ip = ip.get('ip.dst')
            elif 'ipv6' in layers:
                ipv6 = layers['ipv6']
                src_ip = ipv6.get('ipv6.src')
                dst_ip = ipv6.get('ipv6.dst')
            
            # Portas
            src_port = None
            dst_port = None
            
            for proto in ['tcp', 'udp']:
                if proto in layers:
                    layer = layers[proto]
                    src_port = int(layer.get(f'{proto}.srcport', 0)) or None
                    dst_port = int(layer.get(f'{proto}.dstport', 0)) or None
                    break
            
            return {
                'timestamp': timestamp,
                'length': length,
                'protocol': highest_protocol,
                'src_ip': src_ip,
                'dst_ip': dst_ip,
                'src_port': src_port,
                'dst_port': dst_port,
                'info': f"{highest_protocol} packet {length} bytes"
            }
            
        except Exception as e:
            print(f"⚠️ Erro ao parsear pacote tshark: {e}")
            return None

    def _map_interface_name(self, interface_name):
        """
        Mapeia nome de interface para formato aceito pelo PyShark
        
        Args:
            interface_name (str): Nome da interface (ex: 'Wi-Fi', 'Ethernet')
            
        Returns:
            str: Interface mapeada ou None se não encontrar
        """
        try:
            import subprocess
            
            # Tenta listar interfaces do tshark se disponível
            tshark_path = self._find_tshark_path()
            try:
                result = subprocess.run([tshark_path, '-D'], 
                                      capture_output=True, text=True, timeout=5)
                if result.returncode == 0:
                    for line in result.stdout.split('\n'):
                        if line.strip():
                            # Formato: "1. \Device\NPF_{GUID} (Interface Name)"
                            if interface_name.lower() in line.lower():
                                # Extrai o número da interface
                                parts = line.split('.')
                                if parts and parts[0].isdigit():
                                    return parts[0]
            except:
                pass
            
            # Fallback: mapear nomes comuns
            interface_map = {
                'wi-fi': 'Wi-Fi',
                'wifi': 'Wi-Fi', 
                'ethernet': 'Ethernet',
                'vpn': None,  # VPN interfaces podem ser problemáticas
                'any': None   # Deixa None para auto-detect
            }
            
            mapped = interface_map.get(interface_name.lower())
            return mapped if mapped != interface_name else None
            
        except Exception:
            return None

    def _get_tshark_interface(self, interface_name):
        """
        Obtém interface válida para tshark baseada no nome
        
        Args:
            interface_name (str): Nome da interface
            
        Returns:
            str: Interface válida para tshark ou None
        """
        try:
            tshark_path = self._find_tshark_path()
            result = subprocess.run([tshark_path, '-D'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.strip():
                        # Procura por nome da interface na linha
                        if interface_name.lower() in line.lower():
                            # Extrai o número da interface (formato: "1. ...")
                            parts = line.split('.', 1)
                            if parts and parts[0].strip().isdigit():
                                return parts[0].strip()
        except Exception:
            pass
        return None

    def _get_first_available_interface(self):
        """
        Obtém primeira interface disponível no tshark
        
        Returns:
            str: Primeira interface ou None
        """
        try:
            tshark_path = self._find_tshark_path()
            result = subprocess.run([tshark_path, '-D'], 
                                  capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                for line in result.stdout.split('\n'):
                    if line.strip() and '. ' in line:
                        # Primeira linha válida (formato: "1. ...")
                        parts = line.split('.', 1)
                        if parts and parts[0].strip().isdigit():
                            return parts[0].strip()
        except Exception:
            pass
        
        # Fallback para interface padrão
        return "1"

# Alias para manter compatibilidade
NetworkSniffer = PacketSniffer

# Funções auxiliares standalone

def check_admin_privileges():
    """
    Verifica se o usuário está executando com privilégios administrativos
    
    Returns:
        bool: True se executando como admin, False caso contrário
    """
    try:
        if platform.system() == "Windows":
            import ctypes
            return ctypes.windll.shell32.IsUserAnAdmin() != 0
        else:
            # Linux/Mac - verifica se é root
            try:
                return os.geteuid() == 0
            except AttributeError:
                # Fallback se geteuid não estiver disponível
                return False
    except Exception:
        return False

def get_network_interfaces_detailed():
    """
    Retorna lista detalhada de interfaces de rede usando múltiplos métodos
    
    Returns:
        list: Lista de interfaces com detalhes
    """
    interfaces = []
    
    try:
        # Método 1: Tenta usar netifaces se disponível
        try:
            import netifaces
            
            for interface in netifaces.interfaces():
                try:
                    addrs = netifaces.ifaddresses(interface)
                    
                    # Extrai IPs IPv4
                    ip_addresses = []
                    if netifaces.AF_INET in addrs:
                        for addr in addrs[netifaces.AF_INET]:
                            ip_addresses.append(addr['addr'])
                    
                    # Extrai IPs IPv6
                    if netifaces.AF_INET6 in addrs:
                        for addr in addrs[netifaces.AF_INET6]:
                            ip_addresses.append(addr['addr'])
                    
                    interfaces.append({
                        'name': interface,
                        'ip_addresses': ip_addresses,
                        'is_up': True
                    })
                    
                except Exception:
                    interfaces.append({
                        'name': interface,
                        'ip_addresses': [],
                        'is_up': False
                    })
            
            if interfaces:  # Se netifaces funcionou, retorna resultado
                return interfaces
                
        except ImportError:
            pass  # netifaces não disponível
        
        # Método 2: Tenta usar psutil se disponível
        try:
            import psutil
            
            stats = psutil.net_if_stats()
            addrs = psutil.net_if_addrs()
            
            for iface in stats:
                ip_addresses = []
                if iface in addrs:
                    for addr in addrs[iface]:
                        if addr.family in [socket.AF_INET, socket.AF_INET6]:
                            ip_addresses.append(addr.address)
                
                interfaces.append({
                    'name': iface,
                    'ip_addresses': ip_addresses,
                    'is_up': stats[iface].isup
                })
            
            if interfaces:  # Se psutil funcionou, retorna resultado
                return interfaces
                
        except ImportError:
            pass  # psutil não disponível
        
        # Método 3: Usa comandos do sistema
        system = platform.system()
        
        if system == "Windows":
            try:
                result = subprocess.run(['ipconfig', '/all'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    current_interface = None
                    current_ips = []
                    
                    for line in lines:
                        line = line.strip()
                        
                        # Detecta nova interface
                        if "adapter" in line.lower() and ":" in line:
                            if current_interface:
                                # Salva interface anterior
                                clean_name = current_interface.replace("Adaptador", "").replace("adapter", "").strip()
                                clean_name = clean_name.replace(":", "").strip()
                                if clean_name.startswith("de Rede sem Fio"):
                                    clean_name = "Wi-Fi"
                                elif clean_name.startswith("Ethernet"):
                                    clean_name = "Ethernet"
                                elif "VPN" in clean_name.upper():
                                    clean_name = "VPN"
                                elif "Wi-Fi" in clean_name:
                                    clean_name = "Wi-Fi"
                                elif "Wireless" in clean_name:
                                    clean_name = "Wi-Fi"
                                
                                interfaces.append({
                                    'name': clean_name,
                                    'ip_addresses': current_ips.copy(),
                                    'is_up': len(current_ips) > 0
                                })
                            
                            current_interface = line
                            current_ips = []
                        
                        # Detecta IPs (busca por endereços IPv4 válidos)
                        elif "IPv4" in line and ":" in line:
                            ip_part = line.split(":")[-1].strip()
                            # Remove sufixos como "(Preferencial)"
                            ip_clean = ip_part.split("(")[0].strip()
                            # Verifica se é um IP válido (formato xxx.xxx.xxx.xxx)
                            if "." in ip_clean and len(ip_clean.split(".")) == 4:
                                try:
                                    parts = ip_clean.split(".")
                                    if all(0 <= int(part) <= 255 for part in parts):
                                        current_ips.append(ip_clean)
                                except ValueError:
                                    pass  # Não é um IP válido
                    
                    # Salva última interface
                    if current_interface:
                        clean_name = current_interface.replace("Adaptador", "").replace("adapter", "").strip()
                        clean_name = clean_name.replace(":", "").strip()
                        if clean_name.startswith("de Rede sem Fio"):
                            clean_name = "Wi-Fi"
                        elif clean_name.startswith("Ethernet"):
                            clean_name = "Ethernet"
                        elif "VPN" in clean_name.upper():
                            clean_name = "VPN"
                        elif "Wi-Fi" in clean_name:
                            clean_name = "Wi-Fi"
                        elif "Wireless" in clean_name:
                            clean_name = "Wi-Fi"
                        
                        interfaces.append({
                            'name': clean_name,
                            'ip_addresses': current_ips.copy(),
                            'is_up': len(current_ips) > 0
                        })
                    
                    # Remove duplicatas e mantém apenas interfaces com nomes únicos
                    unique_interfaces = []
                    seen_names = set()
                    
                    for iface in interfaces:
                        name = iface['name']
                        if name not in seen_names:
                            seen_names.add(name)
                            unique_interfaces.append(iface)
                        else:
                            # Se já existe, merge os IPs
                            for existing in unique_interfaces:
                                if existing['name'] == name:
                                    existing['ip_addresses'].extend(iface['ip_addresses'])
                                    existing['ip_addresses'] = list(set(existing['ip_addresses']))  # Remove duplicatas
                                    existing['is_up'] = existing['is_up'] or iface['is_up']
                                    break
                    
                    interfaces = unique_interfaces
                        
            except Exception:
                pass
                
        elif system in ["Linux", "Darwin"]:
            try:
                result = subprocess.run(['ifconfig'], capture_output=True, text=True, timeout=10)
                if result.returncode == 0:
                    lines = result.stdout.split('\n')
                    current_interface = None
                    current_ips = []
                    
                    for line in lines:
                        if line and not line.startswith(' ') and not line.startswith('\t'):
                            if current_interface:
                                interfaces.append({
                                    'name': current_interface,
                                    'ip_addresses': current_ips.copy(),
                                    'is_up': len(current_ips) > 0
                                })
                            
                            current_interface = line.split(':')[0].strip()
                            current_ips = []
                        
                        elif 'inet ' in line:
                            parts = line.split()
                            for i, part in enumerate(parts):
                                if part == 'inet' and i + 1 < len(parts):
                                    ip = parts[i + 1]
                                    if ip != '127.0.0.1':
                                        current_ips.append(ip)
                    
                    if current_interface:
                        interfaces.append({
                            'name': current_interface,
                            'ip_addresses': current_ips.copy(),
                            'is_up': len(current_ips) > 0
                        })
                        
            except Exception:
                pass
        
        # Método 4: Fallback usando socket
        if not interfaces:
            try:
                hostname = socket.gethostname()
                local_ip = socket.gethostbyname(hostname)
                
                # Tenta descobrir IP ativo
                active_ip = local_ip
                try:
                    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
                        s.connect(("8.8.8.8", 80))
                        active_ip = s.getsockname()[0]
                except:
                    pass
                
                interfaces = [
                    {'name': 'any', 'ip_addresses': [active_ip], 'is_up': True},
                    {'name': 'localhost', 'ip_addresses': ['127.0.0.1'], 'is_up': True}
                ]
                
                if active_ip != local_ip:
                    interfaces.append({'name': 'auto-detected', 'ip_addresses': [local_ip], 'is_up': True})
                    
            except Exception:
                interfaces = [
                    {'name': 'any', 'ip_addresses': [], 'is_up': True}
                ]
                
    except Exception:
        # Fallback final
        interfaces = [
            {'name': 'any', 'ip_addresses': [], 'is_up': True}
        ]
    
    # Sempre inclui 'any' no início se não estiver presente
    if not any(iface['name'] == 'any' for iface in interfaces):
        interfaces.insert(0, {'name': 'any', 'ip_addresses': [], 'is_up': True})
    
    return interfaces
    
    return interfaces

def get_network_interfaces():
    """
    Retorna lista simples de interfaces de rede
    
    Returns:
        list: Lista de interfaces básicas
    """
    try:
        detailed = get_network_interfaces_detailed()
        return [{'name': iface['name'], 'ip_addresses': iface['ip_addresses']} 
                for iface in detailed]
    except Exception:
        return [{'name': 'any', 'ip_addresses': []}]

def analyze_http_traffic(packets):
    """
    Analisa tráfego HTTP nos pacotes
    
    Args:
        packets (list): Lista de pacotes
        
    Returns:
        list: Pacotes HTTP filtrados
    """
    http_packets = []
    for packet in packets:
        if packet.get('protocol', '').upper() in ['HTTP', 'HTTPS']:
            http_packets.append(packet)
        elif packet.get('dst_port') in [80, 443, 8080]:
            http_packets.append(packet)
        elif packet.get('src_port') in [80, 443, 8080]:
            http_packets.append(packet)
    return http_packets

def analyze_dns_traffic(packets):
    """
    Analisa tráfego DNS nos pacotes
    
    Args:
        packets (list): Lista de pacotes
        
    Returns:
        list: Pacotes DNS filtrados
    """
    dns_packets = []
    for packet in packets:
        if packet.get('protocol', '').upper() == 'DNS':
            dns_packets.append(packet)
        elif packet.get('dst_port') == 53:
            dns_packets.append(packet)
        elif packet.get('src_port') == 53:
            dns_packets.append(packet)
    return dns_packets

def get_top_talkers(packets, limit=10):
    """
    Identifica os IPs que mais geram tráfego
    
    Args:
        packets (list): Lista de pacotes
        limit (int): Número máximo de IPs a retornar
        
    Returns:
        list: Lista de top talkers
    """
    from collections import Counter
    
    ip_stats = Counter()
    
    for packet in packets:
        src_ip = packet.get('src_ip')
        dst_ip = packet.get('dst_ip')
        length = packet.get('length', 0)
        
        if src_ip:
            ip_stats[src_ip] += length
        if dst_ip:
            ip_stats[dst_ip] += length
    
    top_talkers = []
    for ip, bytes_count in ip_stats.most_common(limit):
        top_talkers.append({
            'ip': ip,
            'bytes': bytes_count,
            'packets': sum(1 for p in packets if p.get('src_ip') == ip or p.get('dst_ip') == ip)
        })
    
    return top_talkers

def format_packet_info(packet):
    """
    Formata informações de um pacote para exibição
    
    Args:
        packet (dict): Informações do pacote
        
    Returns:
        str: String formatada
    """
    timestamp = packet['timestamp'].strftime("%H:%M:%S.%f")[:-3]
    protocol = packet['protocol']
    src = f"{packet['src_ip']}:{packet['src_port']}" if packet['src_port'] else packet['src_ip']
    dst = f"{packet['dst_ip']}:{packet['dst_port']}" if packet['dst_port'] else packet['dst_ip']
    length = packet['length']
    
    return f"[{timestamp}] {protocol} {src} -> {dst} ({length} bytes)"
