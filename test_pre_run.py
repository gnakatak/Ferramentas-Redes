#!/usr/bin/env python3
"""
Teste simples para verificar se o app integrado inicia sem erros de sintaxe
"""

import sys
import os

def test_app_syntax():
    """Testa se o app_integrated.py não tem erros de sintaxe"""
    print("🧪 Testando sintaxe do app_integrated.py...")
    
    try:
        # Compila o arquivo para verificar sintaxe
        with open('frontend/app_integrated.py', 'r', encoding='utf-8') as f:
            code = f.read()
        
        compile(code, 'frontend/app_integrated.py', 'exec')
        print("✅ Sintaxe do arquivo está correta!")
        return True
        
    except SyntaxError as e:
        print(f"❌ Erro de sintaxe: {e}")
        print(f"   Linha {e.lineno}: {e.text}")
        return False
    except Exception as e:
        print(f"❌ Erro ao ler arquivo: {e}")
        return False

def test_imports():
    """Testa se os imports funcionam"""
    print("\n🧪 Testando imports do sniffer...")
    
    try:
        # Adiciona backend ao path
        backend_dir = os.path.join(os.getcwd(), 'backend')
        sys.path.insert(0, backend_dir)
        
        from ferramentas.sniffer.sniffer import PacketSniffer, get_network_interfaces
        print("✅ Imports do sniffer funcionaram!")
        
        # Teste básico
        interfaces = get_network_interfaces()
        print(f"✅ get_network_interfaces retornou {len(interfaces)} interfaces")
        
        return True
        
    except Exception as e:
        print(f"❌ Erro nos imports: {e}")
        return False

if __name__ == "__main__":
    print("🔧 TESTE PRÉ-EXECUÇÃO DO APP INTEGRADO")
    print("=" * 50)
    
    # Verifica se estamos no diretório correto
    if not os.path.exists("frontend/app_integrated.py"):
        print("❌ Erro: Execute este script a partir do diretório raiz do projeto")
        sys.exit(1)
    
    # Testa sintaxe
    syntax_ok = test_app_syntax()
    
    # Testa imports
    imports_ok = test_imports()
    
    print("\n" + "=" * 50)
    print("📊 RESULTADOS")
    print("=" * 50)
    print(f"Sintaxe do app: {'✅ OK' if syntax_ok else '❌ ERRO'}")
    print(f"Imports: {'✅ OK' if imports_ok else '❌ ERRO'}")
    
    if syntax_ok and imports_ok:
        print("\n🎉 TUDO OK! O app deve executar sem erros.")
        print("✅ Agora você pode executar:")
        print("   python run_integrated.py")
    else:
        print("\n⚠️ Há problemas que precisam ser corrigidos.")
    
    input("\nPressione Enter para sair...")
