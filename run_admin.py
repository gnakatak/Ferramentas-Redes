#!/usr/bin/env python3
"""
Script que força execução como administrador
Automaticamente solicita privilégios de admin e executa o sniffer
"""
import ctypes
import sys
import os
import subprocess

def is_admin():
    """Verifica se já está executando como admin"""
    try:
        return ctypes.windll.shell32.IsUserAnAdmin()
    except:
        return False

def run_as_admin():
    """Re-executa o script como administrador"""
    if is_admin():
        # Já é admin, execute o sniffer
        print("✅ Executando como Administrador")
        print("🚀 Iniciando Sniffer de Pacotes...")
        
        try:
            # Executa o sniffer integrado
            subprocess.run([sys.executable, "run_integrated.py"], check=True)
        except subprocess.CalledProcessError as e:
            print(f"❌ Erro ao executar sniffer: {e}")
            input("Pressione Enter para fechar...")
        except KeyboardInterrupt:
            print("\n👋 Sniffer finalizado pelo usuário")
            
    else:
        # Não é admin, re-execute como admin
        print("🔄 Solicitando privilégios de administrador...")
        print("💡 Aceite a solicitação do UAC para continuar")
        
        try:
            # Re-executa este script como admin
            ctypes.windll.shell32.ShellExecuteW(
                None, 
                "runas", 
                sys.executable, 
                f'"{__file__}"',
                os.getcwd(),
                1
            )
        except Exception as e:
            print(f"❌ Erro ao solicitar privilégios: {e}")
            input("Pressione Enter para fechar...")

if __name__ == "__main__":
    print("🌐 Sniffer de Pacotes - Modo Administrador")
    print("=" * 50)
    
    # Verifica se estamos no diretório correto
    if not os.path.exists("run_integrated.py"):
        print("❌ Erro: run_integrated.py não encontrado")
        print("Execute este script a partir do diretório raiz do projeto")
        input("Pressione Enter para fechar...")
        sys.exit(1)
    
    run_as_admin()
