import os
import platform
import subprocess
import re

def ping(host='8.8.8.8', count=4):
    system = platform.system().lower()
    if system == "windows":
        cmd = ['ping', host, '-n', str(count)]
        encoding = 'cp850'  # encoding para console Windows
    else:
        cmd = ['ping', '-c', str(count), host]
        encoding = 'utf-8'

    try:
        output = subprocess.check_output(cmd, encoding=encoding)

        # Melhor formatação
        output = re.sub(r'([=\d]+)ms', r'\1 ms', output)
        output = output.replace(',', '   ')

        # Inicializa variáveis
        min_latency = max_latency = avg_latency = None

        if system == "windows":
            # Regex para extrair todas as métricas com acentos
            match = re.search(
                r'Mínimo\s*=\s*(\d+)\s*ms\s+Máximo\s*=\s*(\d+)\s*ms\s+Média\s*=\s*(\d+)', 
                output
            )
            if match:
                min_latency = int(match.group(1))
                max_latency = int(match.group(2))
                avg_latency = int(match.group(3))
        else:
            # Unix-like
            match = re.search(r'=\s*([\d.]+)/([\d.]+)/([\d.]+)/', output)
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
        return {
            "success": False,
            "host": host,
            "count": count,
            "error": str(e),
        }
