import subprocess
import time
import os
import signal
import sys

# Caminhos relativos dos scripts

BACKEND_PATH = os.path.join("backend", "ferramentas", "mini_chat", "chat_server.py")
FRONTEND_PATH = os.path.join("backend", "ferramentas", "mini_chat", "chat_client.py")

# Verifica se os arquivos existem
if not os.path.exists(BACKEND_PATH):
    print(f"Erro: {BACKEND_PATH} não encontrado.")
    sys.exit(1)

if not os.path.exists(FRONTEND_PATH):
    print(f"Erro: {FRONTEND_PATH} não encontrado.")
    sys.exit(1)

# Inicia o backend Flask + SocketIO
print("Iniciando o backend Flask (SocketIO)...")
backend_process = subprocess.Popen(
    ["python", BACKEND_PATH],
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
)

# Aguarda o backend subir
time.sleep(3)

# Inicia o frontend Streamlit
print("Iniciando o frontend Streamlit...")
frontend_process = subprocess.Popen(
    ["streamlit", "run", FRONTEND_PATH],
    creationflags=subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
)

try:
    frontend_process.wait()
except KeyboardInterrupt:
    print("\nInterrompido. Finalizando ambos os processos...")
    backend_process.send_signal(signal.CTRL_BREAK_EVENT)  # Para Windows
    frontend_process.send_signal(signal.CTRL_BREAK_EVENT)
    time.sleep(1)
    backend_process.terminate()
    frontend_process.terminate()

# Encerra os dois processos
backend_process.terminate()
frontend_process.terminate()

# Aguarda a finalização
backend_process.wait()
frontend_process.wait()

print("Todos os processos foram encerrados.")
