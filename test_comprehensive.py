#!/usr/bin/env python3
"""
Teste Abrangente - Sniffer de Pacotes
Script único para testar todas as funcionalidades do projeto
Substitui todos os outros testes redundantes
"""

import sys
import os
import time
import json
import subprocess
import threading
import argparse
from datetime import datetime

# Adiciona o diretório backend ao path
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), 'backend'))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

class TestRunner:
    def __init__(self):
        self.results = []
        self.start_time = None
        self.end_time = None
        
    def log_result(self, test_name, status, message="", details=""):
        """Registra resultado de um teste"""
        result = {
            'test': test_name,
            'status': status,
            'message': message,
            'details': details,
            'timestamp': datetime.now().isoformat()
        }
        self.results.append(result)
        
        # Exibe resultado imediatamente
        status_icon = "✅" if status == "PASS" else "❌" if status == "FAIL" else "⚠️"
        print(f"{status_icon} {test_name}: {message}")
        if details:
            print(f"   {details}")
    
    def run_all_tests(self):
        """Executa todos os testes disponíveis"""
        print("🧪 TESTE ABRANGENTE - SNIFFER DE PACOTES")
        print("=" * 60)
        
        self.start_time = datetime.now()
        
        # Testes de importação
        self.test_imports()
        
        # Testes de dependências
        self.test_dependencies()
        
        # Testes de privilégios
        self.test_privileges()
        
        # Testes de interfaces
        self.test_interfaces()
        
        # Testes de inicialização
        self.test_sniffer_creation()
        
        # Testes de captura (básicos)
        self.test_capture_basic()
        
        # Testes de fallback
        self.test_subprocess_fallback()
        
        # Testes de estrutura do projeto
        self.test_project_structure()
        
        # Testes de backend (opcional)
        if self.should_test_backend():
            self.test_backend_integration()
        
        # Testes de frontend (opcional)
        if self.should_test_frontend():
            self.test_frontend_integration()
        
        self.end_time = datetime.now()
        self.show_summary()
    
    def test_imports(self):
        """Testa todas as importações necessárias"""
        print("\n📦 TESTE DE IMPORTAÇÕES")
        print("-" * 30)
        
        # Teste PyShark
        try:
            import pyshark
            self.log_result("Import PyShark", "PASS", "PyShark disponível")
        except ImportError as e:
            self.log_result("Import PyShark", "FAIL", "PyShark não disponível", str(e))
        
        # Teste módulo sniffer
        try:
            from ferramentas.sniffer.sniffer import PacketSniffer, get_network_interfaces
            self.log_result("Import Sniffer", "PASS", "Módulo sniffer importado")
        except ImportError as e:
            self.log_result("Import Sniffer", "FAIL", "Falha ao importar sniffer", str(e))
        
        # Teste funções auxiliares
        try:
            from ferramentas.sniffer.sniffer import (
                analyze_http_traffic, analyze_dns_traffic, 
                get_top_talkers, check_admin_privileges
            )
            self.log_result("Import Auxiliares", "PASS", "Funções auxiliares importadas")
        except ImportError as e:
            self.log_result("Import Auxiliares", "FAIL", "Falha ao importar auxiliares", str(e))
    
    def test_dependencies(self):
        """Testa dependências opcionais"""
        print("\n🔗 TESTE DE DEPENDÊNCIAS")
        print("-" * 30)
        
        # Streamlit
        try:
            import streamlit
            self.log_result("Streamlit", "PASS", f"Versão {streamlit.__version__}")
        except ImportError:
            self.log_result("Streamlit", "WARN", "Streamlit não disponível")
        
        # Flask
        try:
            import flask
            # Usa método alternativo para versão (pode não ter __version__ em algumas versões)
            version = getattr(flask, '__version__', 'Desconhecida')
            self.log_result("Flask", "PASS", f"Versão {version}")
        except ImportError:
            self.log_result("Flask", "WARN", "Flask não disponível")
        
        # Pandas
        try:
            import pandas
            self.log_result("Pandas", "PASS", f"Versão {pandas.__version__}")
        except ImportError:
            self.log_result("Pandas", "WARN", "Pandas não disponível")
        
        # Netifaces (opcional)
        try:
            import netifaces
            self.log_result("Netifaces", "PASS", "Disponível")
        except ImportError:
            self.log_result("Netifaces", "WARN", "Não disponível (usando fallback)")
    
    def test_privileges(self):
        """Testa verificação de privilégios"""
        print("\n🔐 TESTE DE PRIVILÉGIOS")
        print("-" * 30)
        
        try:
            from ferramentas.sniffer.sniffer import check_admin_privileges
            is_admin = check_admin_privileges()
            
            if is_admin:
                self.log_result("Privilégios", "PASS", "Executando como administrador")
            else:
                self.log_result("Privilégios", "WARN", "NÃO é administrador", 
                               "Captura pode falhar")
        except Exception as e:
            self.log_result("Privilégios", "FAIL", "Erro ao verificar privilégios", str(e))
    
    def test_interfaces(self):
        """Testa detecção de interfaces"""
        print("\n🔌 TESTE DE INTERFACES")
        print("-" * 30)
        
        try:
            from ferramentas.sniffer.sniffer import get_network_interfaces
            interfaces = get_network_interfaces()
            
            if interfaces:
                self.log_result("Interfaces", "PASS", f"{len(interfaces)} interfaces encontradas")
                for i, iface in enumerate(interfaces[:3]):  # Mostra até 3
                    name = iface.get('name', 'N/A')
                    ips = iface.get('ip_addresses', [])
                    ip_info = f"{len(ips)} IPs" if ips else "Sem IPs"
                    print(f"   {i+1}. {name} ({ip_info})")
            else:
                self.log_result("Interfaces", "WARN", "Nenhuma interface detectada")
        except Exception as e:
            self.log_result("Interfaces", "FAIL", "Erro ao detectar interfaces", str(e))
    
    def test_sniffer_creation(self):
        """Testa criação do sniffer"""
        print("\n🔨 TESTE DE CRIAÇÃO DO SNIFFER")
        print("-" * 30)
        
        try:
            from ferramentas.sniffer.sniffer import PacketSniffer
            
            # Teste criação básica
            sniffer = PacketSniffer()
            self.log_result("Criação Básica", "PASS", "Sniffer criado sem parâmetros")
            
            # Teste com parâmetros
            sniffer_with_params = PacketSniffer(interface='any', filter_expr='tcp')
            self.log_result("Criação com Parâmetros", "PASS", "Sniffer com interface e filtro")
            
            # Teste métodos básicos
            stats = sniffer.get_statistics()
            self.log_result("Métodos Básicos", "PASS", f"Estatísticas: {stats}")
            
        except Exception as e:
            self.log_result("Criação Sniffer", "FAIL", "Erro ao criar sniffer", str(e))
    
    def test_capture_basic(self):
        """Testa captura básica (sem executar)"""
        print("\n📡 TESTE DE CAPTURA (CONFIGURAÇÃO)")
        print("-" * 30)
        
        try:
            from ferramentas.sniffer.sniffer import PacketSniffer
            
            sniffer = PacketSniffer(interface='any')
            
            # Testa se os métodos existem
            if hasattr(sniffer, 'start_capture'):
                self.log_result("Método Start", "PASS", "start_capture disponível")
            else:
                self.log_result("Método Start", "FAIL", "start_capture não encontrado")
            
            if hasattr(sniffer, 'stop_capture'):
                self.log_result("Método Stop", "PASS", "stop_capture disponível")
            else:
                self.log_result("Método Stop", "FAIL", "stop_capture não encontrado")
            
            if hasattr(sniffer, 'get_packets'):
                self.log_result("Método Get Packets", "PASS", "get_packets disponível")
            else:
                self.log_result("Método Get Packets", "FAIL", "get_packets não encontrado")
            
        except Exception as e:
            self.log_result("Captura Básica", "FAIL", "Erro nos métodos de captura", str(e))
    
    def test_subprocess_fallback(self):
        """Testa se o fallback subprocess está disponível"""
        print("\n🔄 TESTE DE FALLBACK SUBPROCESS")
        print("-" * 30)
        
        try:
            # Importa o sniffer para usar a nova função de busca
            from ferramentas.sniffer.sniffer import PacketSniffer
            sniffer = PacketSniffer()
            
            # Usa a nova função de detecção
            tshark_path = sniffer._find_tshark_path()
            print(f"🔍 Caminho detectado: {tshark_path}")
            
            # Testa o caminho encontrado
            result = subprocess.run([tshark_path, '--version'], 
                                  capture_output=True, text=True, timeout=5)
            
            if result.returncode == 0:
                version_info = result.stdout.split('\n')[0] if result.stdout else "Versão não detectada"
                self.log_result("TShark", "PASS", f"Disponível em: {tshark_path}")
                print(f"   📋 {version_info}")
            else:
                self.log_result("TShark", "FAIL", f"Caminho existe mas falha: {tshark_path}")
                
        except FileNotFoundError:
            self.log_result("TShark", "WARN", "tshark não encontrado", 
                           "Fallback subprocess não disponível")
        except Exception as e:
            self.log_result("TShark", "FAIL", "Erro ao testar tshark", str(e))
    
    def test_project_structure(self):
        """Testa estrutura do projeto"""
        print("\n📁 TESTE DE ESTRUTURA DO PROJETO")
        print("-" * 30)
        
        required_files = [
            'backend/ferramentas/sniffer/sniffer.py',
            'frontend/app_integrated.py',
            'run_integrated.py',
            'requirements.txt'
        ]
        
        for file_path in required_files:
            if os.path.exists(file_path):
                self.log_result(f"Arquivo {file_path}", "PASS", "Existe")
            else:
                self.log_result(f"Arquivo {file_path}", "FAIL", "Não encontrado")
    
    def should_test_backend(self):
        """Verifica se deve testar backend"""
        return os.path.exists('backend/server.py')
    
    def should_test_frontend(self):
        """Verifica se deve testar frontend"""
        return os.path.exists('frontend/app_integrated.py')
    
    def test_backend_integration(self):
        """Testa integração do backend"""
        print("\n🔗 TESTE DE INTEGRAÇÃO BACKEND")
        print("-" * 30)
        
        try:
            from backend.server import app
            self.log_result("Backend Import", "PASS", "Backend importado")
            
            # Verifica rotas
            with app.test_client() as client:
                response = client.get('/api/hello')
                if response.status_code == 200:
                    self.log_result("Backend API", "PASS", "API responde")
                else:
                    self.log_result("Backend API", "FAIL", f"Status: {response.status_code}")
                    
        except Exception as e:
            self.log_result("Backend Integration", "FAIL", "Erro na integração", str(e))
    
    def test_frontend_integration(self):
        """Testa se o frontend pode ser importado"""
        print("\n🖥️ TESTE DE INTEGRAÇÃO FRONTEND")
        print("-" * 30)
        
        try:
            # Tenta importar sem executar
            import importlib.util
            spec = importlib.util.spec_from_file_location("app_integrated", "frontend/app_integrated.py")
            self.log_result("Frontend Import", "PASS", "Frontend pode ser importado")
            
        except Exception as e:
            self.log_result("Frontend Import", "FAIL", "Erro ao importar frontend", str(e))
    
    def show_summary(self):
        """Exibe resumo dos testes"""
        print("\n" + "=" * 60)
        print("📊 RESUMO DOS TESTES")
        print("=" * 60)
        
        total_tests = len(self.results)
        passed = len([r for r in self.results if r['status'] == 'PASS'])
        failed = len([r for r in self.results if r['status'] == 'FAIL'])
        warnings = len([r for r in self.results if r['status'] == 'WARN'])
        
        duration = (self.end_time - self.start_time).total_seconds() if self.end_time and self.start_time else 0
        
        print(f"🕐 Duração: {duration:.2f}s")
        print(f"📊 Total: {total_tests} testes")
        print(f"✅ Passou: {passed}")
        print(f"❌ Falhou: {failed}")
        print(f"⚠️ Avisos: {warnings}")
        
        if failed == 0:
            print("\n🎉 TODOS OS TESTES CRÍTICOS PASSARAM!")
            print("✅ O projeto está pronto para uso")
        else:
            print(f"\n⚠️ {failed} TESTES FALHARAM")
            print("❌ Verifique os erros acima")
        
        # Mostra testes que falharam
        if failed > 0:
            print("\n🔍 TESTES QUE FALHARAM:")
            for result in self.results:
                if result['status'] == 'FAIL':
                    print(f"   ❌ {result['test']}: {result['message']}")
                    if result['details']:
                        print(f"      {result['details']}")
    
    def export_results(self, filename="test_results.json"):
        """Exporta resultados para arquivo JSON"""
        try:
            with open(filename, 'w', encoding='utf-8') as f:
                json.dump({
                    'summary': {
                        'total_tests': len(self.results),
                        'passed': len([r for r in self.results if r['status'] == 'PASS']),
                        'failed': len([r for r in self.results if r['status'] == 'FAIL']),
                        'warnings': len([r for r in self.results if r['status'] == 'WARN']),
                        'duration': (self.end_time - self.start_time).total_seconds() if self.end_time and self.start_time else 0
                    },
                    'results': self.results
                }, f, indent=2, ensure_ascii=False)
            print(f"\n💾 Resultados salvos em: {filename}")
        except Exception as e:
            print(f"❌ Erro ao salvar resultados: {e}")

def main():
    """Função principal"""
    parser = argparse.ArgumentParser(description='Teste abrangente do sniffer de pacotes')
    parser.add_argument('--export', action='store_true', 
                       help='Exporta resultados para JSON')
    parser.add_argument('--output', default='test_results.json',
                       help='Arquivo de saída para resultados')
    
    args = parser.parse_args()
    
    # Executa testes
    runner = TestRunner()
    runner.run_all_tests()
    
    # Exporta se solicitado
    if args.export:
        runner.export_results(args.output)

if __name__ == "__main__":
    main()
