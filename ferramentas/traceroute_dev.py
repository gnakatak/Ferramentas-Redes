import streamlit as st
import platform
import subprocess
import re
import pandas as pd
import time

def traceroute_dev():
    def contar_saltos(destino, max_saltos=30):
        sistema = platform.system().lower()
        
        if sistema == "windows":
            comando = ["tracert", "-h", str(max_saltos), destino]
            encoding = "cp850"
        else:
            comando = ["traceroute", "-m", str(max_saltos), destino]
            encoding = "utf-8"

        try:
            # Iniciar o processo com saída em streaming
            processo = subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding=encoding)
            
            # Placeholder para exibir os resultados em tempo real
            placeholder = st.empty()
            hops = []
            
            # Processar a saída linha por linha
            while True:
                linha = processo.stdout.readline()
                if not linha and processo.poll() is not None:
                    break  # Sai do loop quando o processo termina
                
                # Ignorar linhas vazias ou cabeçalhos
                if re.match(r"^\s*\d+", linha):
                    # Extrair número do salto
                    hop_num = re.match(r"^\s*(\d+)", linha).group(1)
                    
                    # Extrair hostname, IP e latência
                    if sistema == "windows":
                        # Exemplo: "  1    <1 ms    <1 ms    <1 ms  router.local [192.168.1.1]"
                        # ou "  1     *        *        *     Request timed out."
                        # ou "  1    <1 ms    <1 ms    <1 ms  192.168.1.1"
                        match = re.search(r"((\d+\s+ms|\<\d+\s+ms|\*)\s+(\d+\s+ms|\<\d+\s+ms|\*)\s+(\d+\s+ms|\<\d+\s+ms|\*))\s+(.+?)(?:\s+\[(\d+\.\d+\.\d+\.\d+)\]|$)", linha)
                        if match:
                            latency_str, latency1, _, _, tail, ip = match.groups()
                            latency = latency1 if latency1 != "*" else "Timeout"
                            # Extrair hostname e IP (se disponível)
                            hostname = tail.strip() if tail else "N/A"
                            ip = ip if ip else (hostname if re.match(r"\d+\.\d+\.\d+\.\d+", hostname) else "N/A")
                            if ip == "N/A" and hostname == "N/A":
                                continue  # Pular linhas sem informações úteis
                            hops.append({"Hop": hop_num, "Hostname": hostname, "IP": ip, "Latency": latency})
                        else:
                            # Linha malformada, pular com informações mínimas
                            hops.append({"Hop": hop_num, "Hostname": "N/A", "IP": "N/A", "Latency": "Timeout"})
                    else:
                        # Exemplo: " 1  192.168.1.1 (192.168.1.1)  0.123 ms"
                        match = re.search(r"(\S+)\s+\((\d+\.\d+\.\d+\.\d+)\)\s+(\d+\.\d+\s+ms|\*)", linha)
                        if match:
                            hostname, ip, latency = match.groups()
                            latency = latency if latency != "*" else "Timeout"
                            hops.append({"Hop": hop_num, "Hostname": hostname, "IP": ip, "Latency": latency})
                        else:
                            hops.append({"Hop": hop_num, "Hostname": "N/A", "IP": "N/A", "Latency": "Timeout"})
                    
                    # Atualizar a interface com a tabela mais recente
                    if hops:
                        df = pd.DataFrame(hops)
                        placeholder.table(df)
                        time.sleep(0.1)  # Pequena pausa para suavizar a atualização da UI

            # Verificar se houve erro
            if processo.returncode != 0:
                erro = processo.stderr.read()
                return hops, f"Erro ao executar o comando:\n{erro}"
            
            return hops, None
        except Exception as e:
            return None, f"Erro: {str(e)}"

    # Interface do Streamlit
    st.title("Traceroute em Tempo Real com Streamlit")
    st.write("Digite o destino para rastrear o caminho da rede (exemplo: google.com).")

    # Campo de entrada para o destino
    destino = st.text_input("Destino:", value="google.com")
    max_saltos = st.number_input("Máximo de saltos:", min_value=1, max_value=255, value=30)

    # Botão para executar o traceroute
    if st.button("Executar Traceroute"):
        with st.spinner("Executando traceroute em tempo real..."):
            hops, erro = contar_saltos(destino, max_saltos)
            
            if erro:
                st.error(erro)
            elif hops:
                st.success(f"Traceroute concluído! Número de saltos até {destino}: {len(hops)}")
            else:
                st.warning("Nenhum salto detectado. Verifique o destino ou sua conexão.")