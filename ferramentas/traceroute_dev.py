import streamlit as st
import platform
import subprocess
import re
import pandas as pd
import time
import shutil

def traceroute_dev():
    def contar_saltos(destino, max_saltos=30):
        sistema = platform.system().lower()
        
        # Localizar o comando traceroute ou tracert
        if sistema == "windows":
            cmd_name = "tracert"
        else:
            cmd_name = "traceroute"
        
        comando = shutil.which(cmd_name)
        if not comando:
            return None, f"Erro: Comando '{cmd_name}' não encontrado no sistema. Certifique-se de que está instalado."
        
        if sistema == "windows":
            comando = [comando, "-h", str(max_saltos), destino]
            encoding = "cp850"
        else:
            comando = [comando, "-m", str(max_saltos), destino]
            encoding = "utf-8"

        try:
            processo = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding=encoding)
            
            placeholder = st.empty()
            hops = []
            
            while True:
                linha = processo.stdout.readline()
                if not linha and processo.poll() is not None:
                    break
                
                if re.match(r"^\s*\d+", linha):
                    hop_num = re.match(r"^\s*(\d+)", linha).group(1)
                    
                    if sistema == "windows":
                        match = re.search(r"((\d+\s+ms|\<\d+\s+ms|\*)\s+(\d+\s+ms|\<\d+\s+ms|\*)\s+(\d+\s+ms|\<\d+\s+ms|\*))\s+(.+?)(?:\s+\[(\d+\.\d+\.\d+\.\d+)\]|$)", linha)
                        if match:
                            latency_str, latency1, _, _, tail, ip = match.groups()
                            latency = latency1 if latency1 != "*" else "Timeout"
                            hostname = tail.strip() if tail else "N/A"
                            ip = ip if ip else (hostname if re.match(r"\d+\.\d+\.\d+\.\d+", hostname) else "N/A")
                            if ip == "N/A" and hostname == "N/A":
                                continue
                            hops.append({"Hop": hop_num, "Hostname": hostname, "IP": ip, "Latency": latency})
                        else:
                            hops.append({"Hop": hop_num, "Hostname": "N/A", "IP": "N/A", "Latency": "Timeout"})
                    else:
                        match = re.search(r"(\S+)\s+\((\d+\.\d+\.\d+\.\d+)\)\s+(\d+\.\d+\s+ms|\*)", linha)
                        if match:
                            hostname, ip, latency = match.groups()
                            latency = latency if latency != "*" else "Timeout"
                            hops.append({"Hop": hop_num, "Hostname": hostname, "IP": ip, "Latency": latency})
                        else:
                            hops.append({"Hop": hop_num, "Hostname": "N/A", "IP": "N/A", "Latency": "Timeout"})
                    
                    if hops:
                        df = pd.DataFrame(hops)
                        placeholder.table(df)
                        time.sleep(0.1)

            if processo.returncode != 0:
                erro = processo.stderr.read()
                return hops, f"Erro ao executar o comando:\n{erro}"
            
            return hops, None
        except Exception as e:
            return None, f"Erro: {str(e)}"

    st.title("Traceroute em Tempo Real com Streamlit")
    st.write("Digite o destino para rastrear o caminho da rede (exemplo: google.com).")

    destino = st.text_input("Destino:", value="google.com")
    max_saltos = st.number_input("Máximo de saltos:", min_value=1, max_value=255, value=30)

    if st.button("Executar Traceroute"):
        with st.spinner("Executando traceroute em tempo real..."):
            hops, erro = contar_saltos(destino, max_saltos)
            
            if erro:
                st.error(erro)
            elif hops:
                st.success(f"Traceroute concluído! Número de saltos até {destino}: {len(hops)}")
            else:
                st.warning("Nenhum salto detectado. Verifique o destino ou sua conexão.")