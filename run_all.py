import subprocess
import time

# Inicia o backend Flask
backend_process = subprocess.Popen(["python", "backend/server.py"])

# Aguarda alguns segundos para garantir que o backend subiu
time.sleep(3)

# Inicia o frontend Streamlit
frontend_process = subprocess.Popen(["streamlit", "run", "frontend/app.py"])

try:
    frontend_process.wait()
except KeyboardInterrupt:
    print("Finalizando ambos os processos...")

backend_process.terminate()
frontend_process.terminate()
