import os
import platform
import subprocess
import re
import shutil # Importe shutil

def ping(host='8.8.8.8', count=4):
    system = platform.system().lower()
    
    # Localizar o comando ping
    ping_cmd = shutil.which("ping")
    if not ping_cmd:
        return {
            "success": False,
            "host": host,
            "count": count,
            "error": "Comando 'ping' não encontrado no sistema. Certifique-se de que o comando está instalado."
        }

    if system == "windows":
        cmd = [ping_cmd, host, '-n', str(count)]
        encoding = 'cp850'
    else:
        cmd = [ping_cmd, '-c', str(count), host]
        encoding = 'utf-8'

    try:
        output = subprocess.check_output(cmd, encoding=encoding)

        # Normaliza o espaçamento e substitui vírgulas para facilitar o regex
        output = re.sub(r'([=\d]+)ms', r'\1 ms', output)
        output = output.replace(',', '   ') # Ajusta para o regex subsequente

        min_latency = max_latency = avg_latency = None

        if system == "windows":
            match = re.search(
                r'Mínimo\s*=\s*(\d+)\s*ms\s+Máximo\s*=\s*(\d+)\s*ms\s+Média\s*=\s*(\d+)', 
                output
            )
            if match:
                min_latency = int(match.group(1))
                max_latency = int(match.group(2))
                avg_latency = int(match.group(3))
        else: # Linux/macOS
            match = re.search(r'=\s*([\d.]+)/([\d.]+)/([\d.]+)/', output) # min/avg/max
            if match:
                min_latency = float(match.group(1))
                avg_latency = float(match.group(2))
                max_latency = float(match.group(3))

        return {
            "success": True,
            "host": host,
            "count": count,
            "output": output,
            "min_latency_ms": min_latency,
            "max_latency_ms": max_latency,
            "avg_latency_ms": avg_latency
        }

    except subprocess.CalledProcessError as e:
        # Se o ping falhar (ex: host inacessível)
        return {
            "success": False,
            "host": host,
            "count": count,
            "error": f"Erro ao executar o ping: {e.stderr if e.stderr else e.output}"
        }
    except FileNotFoundError:
        # Este erro seria pego pelo shutil.which(), mas é bom ter uma redundância
        return {
            "success": False,
            "host": host,
            "count": count,
            "error": "Comando 'ping' não encontrado. Certifique-se de que está instalado e no PATH."
        }
    except Exception as e:
        # Captura outros erros inesperados
        return {
            "success": False,
            "host": host,
            "count": count,
            "error": f"Erro inesperado: {str(e)}"
        }