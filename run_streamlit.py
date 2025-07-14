#!/usr/bin/env python3
"""
Script para executar apenas o Streamlit integrado
Não precisa mais do backend Flask!
"""

import sys
import os
import subprocess

def check_dependencies():
    """Verifica se todas as dependências estão instaladas"""
    print("📦 Verificando dependências...")
    
    required_packages = [
        'streamlit', 'pyshark', 'pandas'
    ]
    missing_packages = []
    
    for package in required_packages:
        try:
            __import__(package)
            print(f"✅ {package}")
        except ImportError:
            print(f"❌ {package} - não encontrado")
            missing_packages.append(package)
    
    if missing_packages:
        print(f"\n⚠️  Pacotes faltando: {', '.join(missing_packages)}")
        print("📥 Execute: pip install streamlit pyshark pandas")
        return False
    
    print("✅ Todas as dependências estão instaladas!")
    return True

def main():
    print("=" * 65)
    print("🌐 FERRAMENTAS DE REDES - VERSÃO INTEGRADA")
    print("=" * 65)
    print("✨ Nova versão: Tudo integrado no Streamlit!")
    print("🚫 Não precisa mais do backend Flask")
    print("📱 Interface: http://localhost:8501")
    print("=" * 65)
    
    # Verifica se estamos no diretório correto
    if not os.path.exists("frontend/app.py"):
        print("❌ Execute este script a partir do diretório raiz do projeto!")
        print("   Certifique-se de que o arquivo frontend/app.py existe")
        sys.exit(1)
    
    # Verifica dependências
    if not check_dependencies():
        sys.exit(1)
    
    print(f"\n🚀 Iniciando aplicação Streamlit...")
    print(f"🌐 Acesse: http://localhost:8501")
    print(f"📱 App: frontend/app.py")
    print(f"\n💡 Funcionalidades disponíveis:")
    print(f"   - 🔍 Sniffer de Pacotes integrado")
    print(f"   - 📊 Dashboard em tempo real")
    print(f"   - 💾 Exportação de dados")
    print(f"   - 📈 Análise de protocolos")
    print(f"\n⏹️  Pressione Ctrl+C para parar")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "frontend/app.py", 
            "--server.port=8501",
            "--server.headless=false",
            "--browser.gatherUsageStats=false"
        ])
        
    except KeyboardInterrupt:
        print("\n👋 Aplicação finalizada pelo usuário")
    except Exception as e:
        print(f"❌ Erro ao executar aplicação: {e}")
        print("\n🔍 Soluções possíveis:")
        print("1. Verifique se o Streamlit está instalado: pip install streamlit")
        print("2. Verifique se o PyShark está instalado: pip install pyshark")
        print("3. Execute como administrador (para captura de pacotes)")
        sys.exit(1)

if __name__ == "__main__":
    main()
