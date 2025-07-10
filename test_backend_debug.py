#!/usr/bin/env python3
"""
Teste específico para debug do backend separado
"""

import sys
import os
import time
import subprocess
import requests
import json

def test_backend_detailed():
    """Teste detalhado do backend separado"""
    print("🔍 TESTE DETALHADO - BACKEND SEPARADO")
    print("=" * 60)
    
    # Inicia backend
    print("🚀 Iniciando backend...")
    backend_process = subprocess.Popen(
        [sys.executable, "backend/server.py"],
        cwd=os.getcwd(),
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1
    )
    
    # Aguarda inicialização
    time.sleep(5)
    
    try:
        # Teste 1: Conectividade básica
        print("\n🔍 Teste 1: Conectividade")
        try:
            response = requests.get("http://localhost:5000/api/hello", timeout=10)
            if response.status_code == 200:
                print("✅ Backend conectando")
            else:
                print(f"❌ Status: {response.status_code}")
                return False
        except Exception as e:
            print(f"❌ Erro conectividade: {e}")
            return False
        
        # Teste 2: Interfaces
        print("\n🔍 Teste 2: Detecção de interfaces")
        try:
            response = requests.get("http://localhost:5000/api/sniffer/interfaces", timeout=10)
            data = response.json()
            print(f"📊 Response: {json.dumps(data, indent=2)}")
            if data.get('success'):
                interfaces = data.get('interfaces', [])
                print(f"✅ {len(interfaces)} interfaces detectadas")
            else:
                print(f"❌ Erro: {data.get('error')}")
                return False
        except Exception as e:
            print(f"❌ Erro interfaces: {e}")
            return False
        
        # Teste 3: Captura com debug
        print("\n🔍 Teste 3: Captura de pacotes (debug)")
        try:
            payload = {
                "interface": None,  # Auto
                "filter": None,
                "packet_count": 5,
                "timeout": 20
            }
            print(f"📤 Payload: {json.dumps(payload, indent=2)}")
            
            response = requests.post(
                "http://localhost:5000/api/sniffer/start",
                json=payload,
                timeout=25
            )
            
            print(f"📥 Status code: {response.status_code}")
            data = response.json()
            print(f"📊 Response: {json.dumps(data, indent=2)}")
            
            if data.get('success'):
                print("✅ Captura iniciada com sucesso!")
                
                # Aguarda e verifica status várias vezes
                for i in range(5):
                    time.sleep(3)
                    status_response = requests.get("http://localhost:5000/api/sniffer/status", timeout=5)
                    status_data = status_response.json()
                    stats = status_data.get('statistics', {})
                    
                    print(f"📊 Status {i+1}: {stats.get('total_packets', 0)} pacotes, running: {stats.get('is_running', False)}")
                    
                    if stats.get('total_packets', 0) > 0:
                        print("🎉 PACOTES CAPTURADOS!")
                        
                        # Tenta obter os pacotes
                        packets_response = requests.get("http://localhost:5000/api/sniffer/packets?limit=3", timeout=5)
                        packets_data = packets_response.json()
                        
                        if packets_data.get('success'):
                            packets = packets_data.get('packets', [])
                            print(f"📦 {len(packets)} pacotes obtidos")
                            if packets:
                                print(f"🔍 Primeiro pacote: {json.dumps(packets[0], indent=2)}")
                            return True
                        else:
                            print(f"❌ Erro ao obter pacotes: {packets_data.get('error')}")
                            
                if stats.get('total_packets', 0) == 0:
                    print("⚠️ Nenhum pacote capturado")
                    return False
                    
            else:
                print(f"❌ Erro ao iniciar captura: {data.get('error')}")
                return False
                
        except Exception as e:
            print(f"❌ Erro captura: {e}")
            import traceback
            traceback.print_exc()
            return False
            
    finally:
        # Para backend
        try:
            backend_process.terminate()
            backend_process.wait(timeout=5)
            print("\n✅ Backend finalizado")
        except:
            backend_process.kill()
            print("\n⚠️ Backend forçado a parar")

if __name__ == "__main__":
    success = test_backend_detailed()
    
    print("\n" + "=" * 60)
    if success:
        print("🎉 SUCESSO! Backend conseguiu capturar pacotes!")
    else:
        print("❌ FALHA! Backend não conseguiu capturar pacotes")
        print("\n💡 Possíveis soluções:")
        print("1. Execute como administrador")
        print("2. Verifique se PyShark está funcionando")
        print("3. Verifique se tshark está instalado")
        print("4. Use o aplicativo integrado que funciona")
    print("=" * 60)
