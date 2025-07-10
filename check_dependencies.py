"""
Verifica se todas as dependências estão instaladas
"""
import importlib
import subprocess
import sys

def check_python_package(package_name):
    """Verifica se um pacote Python está instalado"""
    try:
        importlib.import_module(package_name)
        print(f"✅ {package_name}: Instalado")
        return True
    except ImportError:
        print(f"❌ {package_name}: NÃO instalado")
        return False

def check_npcap():
    """Verifica se o Npcap está instalado"""
    try:
        result = subprocess.run(['sc', 'query', 'npcap'], 
                              capture_output=True, text=True)
        if result.returncode == 0:
            print("✅ Npcap: Instalado e rodando")
            return True
        else:
            print("❌ Npcap: NÃO instalado")
            return False
    except Exception:
        print("⚠️  Npcap: Não foi possível verificar")
        return False

def main():
    print("🔍 Verificando dependências do Sniffer...\n")
    
    # Verifica pacotes Python
    python_deps = ['streamlit', 'pyshark', 'pandas']
    all_python_ok = True
    
    for dep in python_deps:
        if not check_python_package(dep):
            all_python_ok = False
    
    # Verifica Npcap
    npcap_ok = check_npcap()
    
    print("\n📋 Resumo:")
    if all_python_ok and npcap_ok:
        print("🎉 Todas as dependências estão instaladas!")
        print("✅ Você pode executar o sniffer normalmente")
    else:
        print("⚠️  Algumas dependências estão faltando:")
        if not all_python_ok:
            print("   - Execute: pip install streamlit pyshark pandas")
        if not npcap_ok:
            print("   - Execute: python install_npcap.py")

if __name__ == "__main__":
    main()