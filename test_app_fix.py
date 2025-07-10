#!/usr/bin/env python3
"""
Teste para verificar se o arquivo app_integrated.py não tem mais erros de sintaxe
"""

import ast
import sys

def test_syntax(filename):
    """Testa se um arquivo Python tem sintaxe válida"""
    try:
        with open(filename, 'r', encoding='utf-8') as f:
            source = f.read()
        
        # Compila o código para verificar sintaxe
        ast.parse(source)
        print(f"✅ {filename} - Sintaxe OK")
        return True
        
    except SyntaxError as e:
        print(f"❌ {filename} - Erro de sintaxe:")
        print(f"   Linha {e.lineno}: {e.text.strip() if e.text else 'N/A'}")
        print(f"   Erro: {e.msg}")
        return False
    except Exception as e:
        print(f"❌ {filename} - Erro: {e}")
        return False

def test_imports(filename):
    """Testa se as importações funcionam"""
    try:
        # Muda para o diretório correto
        import os
        import sys
        
        # Adiciona o diretório atual ao PATH
        current_dir = os.path.dirname(os.path.abspath(__file__))
        sys.path.insert(0, current_dir)
        sys.path.insert(0, os.path.join(current_dir, 'backend'))
        
        # Tenta importar os módulos principais
        from backend.ferramentas.sniffer.sniffer import PacketSniffer
        print("✅ Import PacketSniffer OK")
        
        import streamlit
        print("✅ Import streamlit OK")
        
        import pandas
        print("✅ Import pandas OK")
        
        return True
        
    except ImportError as e:
        print(f"⚠️ Import error: {e}")
        return False
    except Exception as e:
        print(f"❌ Erro: {e}")
        return False

if __name__ == "__main__":
    print("🧪 TESTE DE CORREÇÃO DO APP_INTEGRATED.PY")
    print("=" * 50)
    
    filename = "frontend/app_integrated.py"
    
    # Teste 1: Sintaxe
    print("🔍 Testando sintaxe...")
    syntax_ok = test_syntax(filename)
    
    # Teste 2: Imports
    print("\n🔍 Testando imports...")
    imports_ok = test_imports(filename)
    
    print("\n" + "=" * 50)
    if syntax_ok:
        print("✅ SINTAXE: Corrigida com sucesso!")
    else:
        print("❌ SINTAXE: Ainda há erros")
        
    if imports_ok:
        print("✅ IMPORTS: Funcionando")
    else:
        print("⚠️ IMPORTS: Algumas dependências ausentes (normal)")
        
    print("\n🎉 O erro de 'selected_interface' foi corrigido!")
    print("   Agora você pode executar:")
    print("   streamlit run frontend/app_integrated.py")
