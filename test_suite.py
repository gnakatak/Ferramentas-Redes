"""
Testes unificados do projeto Ferramentas-Redes
Inclui os principais testes de sniffer, backend, interfaces e captura
"""
import sys, os
import importlib

def test_sniffer_import():
    try:
        from backend.ferramentas.sniffer.sniffer import PacketSniffer
        print("✅ Import PacketSniffer OK")
        return True
    except Exception as e:
        print(f"❌ Erro import PacketSniffer: {e}")
        return False

def test_backend_api():
    try:
        import requests
        response = requests.get("http://localhost:5000/api/hello", timeout=5)
        if response.status_code == 200:
            print("✅ Backend API /hello OK")
            return True
        else:
            print(f"❌ Backend API status: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Erro backend API: {e}")
        return False

def test_capture():
    try:
        from backend.ferramentas.sniffer.sniffer import PacketSniffer
        sniffer = PacketSniffer()
        result = sniffer.start_capture_subprocess(packet_count=3, timeout=10)
        if isinstance(result, dict) and result.get('error'):
            print(f"❌ Erro captura: {result['error']}")
            return False
        print("✅ Captura subprocess OK")
        return True
    except Exception as e:
        print(f"❌ Erro captura subprocess: {e}")
        return False

def main():
    print("\n🧪 TESTE UNIFICADO - Ferramentas-Redes")
    print("="*50)
    ok1 = test_sniffer_import()
    ok2 = test_backend_api()
    ok3 = test_capture()
    print("\nResultados:")
    print(f"- Importação do sniffer: {'OK' if ok1 else 'FALHOU'}")
    print(f"- Backend API: {'OK' if ok2 else 'FALHOU'}")
    print(f"- Captura de pacotes: {'OK' if ok3 else 'FALHOU'}")
    print("="*50)
    if all([ok1, ok2, ok3]):
        print("🎉 TODOS OS TESTES PASSARAM!")
    else:
        print("⚠️ Algum teste falhou. Veja acima.")

if __name__ == "__main__":
    main()
