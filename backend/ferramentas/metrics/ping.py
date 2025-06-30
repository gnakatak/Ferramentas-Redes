import os
import platform
import subprocess
import re

def ping(host='8.8.8.8', count=4):
    system = platform.system().lower()
    if system == "windows":
        cmd = ['ping', host, '-n', str(count)]
    else:
        cmd = ['ping', '-c', str(count), host]

    try:
        output = subprocess.check_output(cmd, universal_newlines=True)
        print(output)

        # Extração simples da latência média (pode ser ajustada conforme o SO)
        if "avg" in output:
            match = re.search(r'avg\/([\d\.]+)', output)
        else:
            match = re.search(r'=\s.*\/([\d\.]+)\/', output)
        
        if match:
            avg_latency = float(match.group(1))
            print(f"Latência média: {avg_latency} ms")
            return avg_latency
    except subprocess.CalledProcessError as e:
        print(f"Erro ao executar o ping: {e}")
        return None

if __name__ == '__main__':
    ping()
