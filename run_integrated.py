#!/usr/bin/env python3
"""
Script para executar a versão integrada do Sniffer
Apenas uma dependência externa: streamlit + pyshark
"""

import subprocess
import sys
import os

def main():
    print("🌐 Iniciando Sniffer de Pacotes - Versão Integrada")
    print("=" * 50)
    
    # Verifica se estamos no diretório correto
    if not os.path.exists("frontend/app_integrated.py"):
        print("❌ Erro: Execute este script a partir do diretório raiz do projeto")
        sys.exit(1)
    
    # Verifica se as dependências estão instaladas
    try:
        import streamlit
        import pyshark
        import pandas
        print("✅ Dependências verificadas")
    except ImportError as e:
        print(f"❌ Dependência não encontrada: {e}")
        print("📦 Instale as dependências com:")
        print("   pip install -r requirements_integrated.txt")
        sys.exit(1)
    
    # Inicia o Streamlit
    print("🚀 Iniciando aplicação Streamlit...")
    print("🌐 Acesse: http://localhost:8501")
    print("⚠️  Certifique-se de executar como Administrador (Windows) ou com sudo (Linux/Mac)")
    print("\nPressione Ctrl+C para parar")
    
    try:
        subprocess.run([
            sys.executable, "-m", "streamlit", "run", 
            "frontend/app_integrated.py",
            "--server.port=8501",
            "--server.headless=false"
        ])
    except KeyboardInterrupt:
        print("\n👋 Aplicação finalizada")

if __name__ == "__main__":
    main()
