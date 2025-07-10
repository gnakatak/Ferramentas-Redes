#!/usr/bin/env python3
"""
Script simples para testar apenas a detecção do tshark
"""

import subprocess
import os
import platform

def find_tshark_simple():
    """Encontra o tshark usando busca simples"""
    system = platform.system()
    
    print(f"🔍 Sistema detectado: {system}")
    
    if system == "Windows":
        paths_to_test = [
            "C:\\Program Files\\Wireshark\\tshark.exe",
            "C:\\Program Files (x86)\\Wireshark\\tshark.exe"
        ]
        
        for path in paths_to_test:
            print(f"🔍 Testando: {path}")
            if os.path.exists(path):
                print(f"✅ Arquivo existe: {path}")
                try:
                    result = subprocess.run([path, '--version'], 
                                          capture_output=True, timeout=5)
                    if result.returncode == 0:
                        print(f"✅ tshark funcional: {path}")
                        return True, path
                    else:
                        print(f"❌ Erro de execução: código {result.returncode}")
                except Exception as e:
                    print(f"❌ Erro ao executar: {e}")
            else:
                print(f"❌ Arquivo não existe: {path}")
    
    # Testa no PATH
    print("\n🔍 Testando no PATH...")
    try:
        result = subprocess.run(['tshark', '--version'], 
                              capture_output=True, timeout=5)
        if result.returncode == 0:
            print("✅ tshark disponível no PATH")
            return True, 'tshark'
        else:
            print(f"❌ Erro no PATH: código {result.returncode}")
    except Exception as e:
        print(f"❌ Erro no PATH: {e}")
    
    return False, None

if __name__ == "__main__":
    print("🔧 Teste Simples de Detecção do tshark")
    print("=" * 40)
    
    found, path = find_tshark_simple()
    
    print("\n" + "=" * 40)
    if found:
        print(f"🎉 SUCESSO: tshark encontrado em {path}")
    else:
        print("❌ FALHA: tshark não encontrado")
