#!/usr/bin/env python3
"""
Teste rápido do tshark path detection
"""

import subprocess
import os
import platform

def find_tshark():
    """Busca tshark no sistema"""
    system = platform.system()
    
    if system == "Windows":
        possible_paths = [
            "C:\\Program Files\\Wireshark\\tshark.exe",
            "C:\\Program Files (x86)\\Wireshark\\tshark.exe",
            os.path.expanduser("~\\AppData\\Local\\Programs\\Wireshark\\tshark.exe"),
            "tshark.exe",
            "tshark"
        ]
        
        for path in possible_paths:
            print(f"🔍 Testando: {path}")
            
            if path in ["tshark.exe", "tshark"]:
                try:
                    result = subprocess.run([path, '--version'], 
                                          capture_output=True, timeout=3, text=True)
                    if result.returncode == 0:
                        print(f"✅ Encontrado no PATH: {path}")
                        print(f"   Versão: {result.stdout.split()[1]}")
                        return path
                except Exception as e:
                    print(f"❌ Falha no PATH: {e}")
                    continue
            else:
                if os.path.exists(path):
                    try:
                        result = subprocess.run([path, '--version'], 
                                              capture_output=True, timeout=3, text=True)
                        if result.returncode == 0:
                            print(f"✅ Encontrado: {path}")
                            print(f"   Versão: {result.stdout.split()[1]}")
                            return path
                    except Exception as e:
                        print(f"⚠️ Existe mas falhou: {e}")
                else:
                    print(f"❌ Não existe")
    
    print("❌ tshark não encontrado em nenhum local")
    return None

def main():
    print("🔍 TESTE DE DETECÇÃO DO TSHARK")
    print("=" * 50)
    
    tshark_path = find_tshark()
    
    if tshark_path:
        print(f"\n🎉 SUCESSO! tshark encontrado em:")
        print(f"   {tshark_path}")
        
        # Teste básico de captura
        print(f"\n🧪 Testando captura básica...")
        try:
            result = subprocess.run([
                tshark_path, '-c', '1', '-T', 'json'
            ], capture_output=True, timeout=10, text=True)
            
            if result.returncode == 0:
                print("✅ Teste de captura funcionou!")
                if result.stdout.strip():
                    print("✅ Dados JSON retornados")
                else:
                    print("⚠️ Sem dados (pode não haver tráfego)")
            else:
                print(f"❌ Teste de captura falhou: {result.stderr}")
                
        except subprocess.TimeoutExpired:
            print("⏰ Timeout - pode estar aguardando tráfego")
        except Exception as e:
            print(f"❌ Erro no teste: {e}")
    else:
        print("\n❌ FALHA! Instale Wireshark:")
        print("   https://www.wireshark.org/download.html")

if __name__ == "__main__":
    main()
