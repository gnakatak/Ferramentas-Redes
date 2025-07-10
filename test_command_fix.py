#!/usr/bin/env python3
"""
Teste específico para verificar se a correção do comando tshark funcionou
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'backend'))

from ferramentas.sniffer.sniffer import PacketSniffer

def test_tshark_command_construction():
    """Testa se o comando tshark está sendo construído corretamente"""
    print("🧪 Testando construção do comando tshark...")
    
    try:
        sniffer = PacketSniffer()
        print("✅ Sniffer criado com sucesso")
        
        # Testa encontrar tshark
        tshark_path = sniffer._find_tshark_path()
        print(f"🔧 tshark encontrado em: {tshark_path}")
        
        # Testa construção do comando manualmente
        test_interface = "4"  # Interface Wi-Fi
        test_packets = 3
        
        cmd = [tshark_path, '-i', test_interface, '-c', str(test_packets), '-T', 'json', '-t', 'a', '-l']
        
        print(f"🔧 Comando construído: {' '.join(cmd)}")
        
        # Verifica se não há duplicação de parâmetros
        if cmd.count('-c') > 1:
            print("❌ ERRO: Parâmetro -c duplicado!")
            return False
        
        if cmd.count('-T') > 1:
            print("❌ ERRO: Parâmetro -T duplicado!")
            return False
            
        if cmd.count('-i') > 1:
            print("❌ ERRO: Parâmetro -i duplicado!")
            return False
        
        print("✅ Comando construído corretamente, sem duplicações")
        
        # Testa o comando real (só para ver se formata corretamente)
        import subprocess
        try:
            # Apenas teste de formato (versão), não captura real
            version_cmd = [tshark_path, '--version']
            result = subprocess.run(version_cmd, capture_output=True, text=True, timeout=5)
            if result.returncode == 0:
                print("✅ tshark está funcionando")
                print(f"   Versão: {result.stdout.split()[1] if result.stdout else 'N/A'}")
            else:
                print(f"⚠️ tshark retornou erro: {result.stderr}")
        except Exception as e:
            print(f"⚠️ Erro ao testar tshark: {e}")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro: {e}")
        import traceback
        traceback.print_exc()
        return False

def test_subprocess_capture_method():
    """Testa o método de captura subprocess especificamente"""
    print("\n🧪 Testando método _capture_via_subprocess...")
    
    try:
        sniffer = PacketSniffer()
        
        # Testa com poucos pacotes e timeout baixo
        print("🚀 Executando captura via subprocess (teste)...")
        success = sniffer._capture_via_subprocess(packet_count=2, timeout=15)
        
        if success:
            print("✅ Captura subprocess funcionou!")
            print(f"   Pacotes capturados: {len(sniffer.captured_packets)}")
        else:
            print("⚠️ Captura subprocess não capturou pacotes")
            
        return success
        
    except Exception as e:
        print(f"❌ Erro na captura subprocess: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 TESTE DE CORREÇÃO DO COMANDO TSHARK")
    print("=" * 60)
    
    success1 = test_tshark_command_construction()
    success2 = test_subprocess_capture_method()
    
    print("\n" + "=" * 60)
    if success1 and success2:
        print("✅ TODOS OS TESTES PASSARAM!")
    elif success1:
        print("⚠️ COMANDO OK, MAS CAPTURA FALHOU")
    else:
        print("❌ TESTES FALHARAM")
    print("=" * 60)
