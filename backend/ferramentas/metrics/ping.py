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

        output = re.sub(r'([=\d]+)ms', r'\1 ms', output)
        output = output.replace(',', '   ')

        # Extração da latência média
        if system == "windows":
            match = re.search(r'M[ée]dia = (\d+)', output)
        else:
            match = re.search(r'=\s[\d\.]+/([\d\.]+)/', output)

        if match:
            avg_latency = float(match.group(1))
        else:
            avg_latency = None

        return {
            "success": True,
            "host": host,
            "count": count,
            "output": output,
            "avg_latency_ms": avg_latency
        }

    except subprocess.CalledProcessError as e:
        return {
            "success": False,
            "host": host,
            "count": count,
            "error": str(e),
        }
