#!/usr/bin/env python3
"""
Teste específico para verificar se o backend está funcionando corretamente
"""

import requests
import time
import subprocess
import sys
import os

def test_backend_sniffer():
    """Testa se o backend consegue capturar pacotes"""
    print("🧪 TESTE DO BACKEND - MODO SEPARADO")
    print("=" * 50)
    
    # Inicia o backend
    print("🚀 Iniciando backend...")
    backend_process = subprocess.Popen(
        [sys.executable, "backend/server.py"],
        cwd=os.getcwd(),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # Aguarda backend inicializar
    time.sleep(3)
    
    try:
        # Testa conectividade
        print("🔍 Testando conectividade...")
        response = requests.get("http://localhost:5000/api/hello", timeout=5)
        if response.status_code == 200:
            print("✅ Backend está respondendo")
        else:
            print("❌ Backend não está respondendo corretamente")
            return False
        
        # Testa detecção de interfaces
        print("🔍 Testando detecção de interfaces...")
        response = requests.get("http://localhost:5000/api/sniffer/interfaces", timeout=10)
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                interfaces = data.get('interfaces', [])
                print(f"✅ {len(interfaces)} interfaces detectadas")
            else:
                print("❌ Erro ao detectar interfaces:", data.get('error'))
                return False
        else:
            print("❌ Falha na requisição de interfaces")
            return False
        
        # Testa captura de pacotes
        print("🔍 Testando captura de pacotes...")
        payload = {
            "interface": None,  # Auto-detect
            "filter": None,
            "packet_count": 5,
            "timeout": 15
        }
        
        response = requests.post(
            "http://localhost:5000/api/sniffer/start", 
            json=payload, 
            timeout=20
        )
        
        if response.status_code == 200:
            data = response.json()
            if data.get('success'):
                print("✅ Captura iniciada com sucesso")
                
                # Aguarda um pouco para capturar
                time.sleep(5)
                
                # Verifica status
                response = requests.get("http://localhost:5000/api/sniffer/status", timeout=5)
                if response.status_code == 200:
                    status_data = response.json()
                    stats = status_data.get('statistics', {})
                    packet_count = stats.get('total_packets', 0)
                    print(f"✅ Pacotes capturados: {packet_count}")
                    
                    if packet_count > 0:
                        print("🎉 SUCESSO! Backend conseguiu capturar pacotes!")
                        return True
                    else:
                        print("⚠️ Backend funcionou, mas não capturou pacotes")
                        return False
                else:
                    print("❌ Erro ao verificar status")
                    return False
            else:
                print("❌ Erro ao iniciar captura:", data.get('error'))
                return False
        else:
            print("❌ Falha na requisição de captura")
            return False
            
    except Exception as e:
        print(f"❌ Erro durante teste: {e}")
        return False
    finally:
        # Para o backend
        try:
            backend_process.terminate()
            backend_process.wait(timeout=5)
            print("✅ Backend finalizado")
        except:
            backend_process.kill()
            print("⚠️ Backend forçado a parar")

if __name__ == "__main__":
    success = test_backend_sniffer()
    
    print("\n" + "=" * 50)
    if success:
        print("✅ TESTE PASSOU! Backend funciona corretamente")
        print("   Agora você pode usar: python run_all_improved.py")
    else:
        print("❌ TESTE FALHOU! Verifique os problemas acima")
    print("=" * 50)
