"""
Script para auxiliar na instalação do Npcap
"""
import webbrowser
import subprocess
import sys
import os

def open_npcap_download():
    """Abre a página de download do Npcap"""
    print("🌐 Abrindo página de download do Npcap...")
    webbrowser.open("https://nmap.org/npcap/")
    print("📥 Baixe a versão mais recente do Npcap")
    print("⚠️  IMPORTANTE: Marque a opção 'Install Npcap in WinPcap API-compatible mode'")

def check_npcap_installed():
    """Verifica se o Npcap está instalado"""
    try:
        # Verifica se o serviço do Npcap está rodando
        result = subprocess.run(['sc', 'query', 'npcap'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Npcap está instalado e rodando")
            return True
        else:
            print("❌ Npcap não está instalado")
            return False
    except Exception as e:
        print(f"⚠️  Erro ao verificar Npcap: {e}")
        return False

def main():
    print("🔍 Verificando instalação do Npcap...")
    
    if check_npcap_installed():
        print("🎉 Npcap já está instalado! Você pode usar o sniffer.")
        return
    
    print("\n📋 Passos para instalação do Npcap:")
    print("1. Baixar o Npcap")
    print("2. Executar como Administrador")
    print("3. Marcar 'Install Npcap in WinPcap API-compatible mode'")
    print("4. Reiniciar o computador (se necessário)")
    
    response = input("\n🌐 Abrir página de download? (s/n): ")
    if response.lower() in ['s', 'sim', 'y', 'yes']:
        open_npcap_download()
        print("\n⏳ Após instalar o Npcap, execute novamente o sniffer.")

if __name__ == "__main__":
    main()