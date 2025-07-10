# Sniffer de Pacotes - Documentação

## Visão Geral

O Sniffer de Pacotes é uma ferramenta completa para captura e análise de tráfego de rede em tempo real. Ele utiliza a biblioteca Scapy para capturar pacotes e oferece uma API REST para integração com frontend.

## Funcionalidades

### 🔍 Captura de Pacotes
- Captura em tempo real de pacotes de rede
- Suporte a múltiplas interfaces de rede
- Filtros BPF (Berkeley Packet Filter)
- Limite de pacotes e timeout configuráveis

### 📊 Análise de Protocolos
- Análise de protocolos TCP, UDP, ICMP
- Detecção de tráfego HTTP e DNS
- Extração de informações de IP, portas e flags
- Análise de cabeçalhos Ethernet

### 📈 Estatísticas
- Contagem total de pacotes
- Distribuição por protocolo
- Taxa de pacotes por segundo
- Tempo de captura

### 💾 Exportação
- Exportação em formato JSON
- Exportação em formato CSV
- Arquivo com timestamp automático

## Instalação

### Pré-requisitos

As seguintes bibliotecas são necessárias (já listadas no requirements.txt):

```
scapy
netifaces
psutil
```

### Instalação das Dependências

```bash
pip install -r requirements.txt
```

**Nota para Windows:** O Scapy no Windows requer WinPcap ou Npcap:
- Baixe e instale o Npcap: https://nmap.org/npcap/
- Certifique-se de marcar "Install Npcap in WinPcap API-compatible Mode"

## Uso da API

### 1. Listar Interfaces de Rede

```http
GET /api/sniffer/interfaces
```

**Resposta:**
```json
{
  "success": true,
  "interfaces": [
    {
      "name": "eth0",
      "ip_addresses": [
        {
          "type": "IPv4",
          "address": "192.168.1.100",
          "netmask": "255.255.255.0"
        }
      ]
    }
  ]
}
```

### 2. Iniciar Captura

```http
POST /api/sniffer/start
Content-Type: application/json

{
  "interface": "eth0",
  "filter": "tcp port 80",
  "packet_count": 100,
  "timeout": 30
}
```

**Parâmetros:**
- `interface` (opcional): Interface específica para capturar
- `filter` (opcional): Filtro BPF (ex: "tcp port 80", "udp", "icmp")
- `packet_count` (opcional): Número máximo de pacotes (0 = ilimitado)
- `timeout` (opcional): Timeout em segundos

### 3. Parar Captura

```http
POST /api/sniffer/stop
```

### 4. Obter Status e Estatísticas

```http
GET /api/sniffer/status
```

**Resposta:**
```json
{
  "success": true,
  "statistics": {
    "status": "running",
    "duration": 15.5,
    "total_packets": 142,
    "protocols": {
      "TCP": 98,
      "UDP": 31,
      "ICMP": 13
    },
    "packets_per_second": 9.16
  }
}
```

### 5. Obter Pacotes Capturados

```http
GET /api/sniffer/packets?limit=50
```

**Resposta:**
```json
{
  "success": true,
  "packets": [
    {
      "timestamp": "2025-01-15T10:30:45.123456",
      "protocol": "TCP",
      "src_ip": "192.168.1.100",
      "dst_ip": "93.184.216.34",
      "src_port": 54321,
      "dst_port": 80,
      "size": 1500,
      "info": "Flags: SYN,ACK"
    }
  ],
  "count": 1
}
```

### 6. Exportar Pacotes

```http
POST /api/sniffer/export
Content-Type: application/json

{
  "filename": "minha_captura.json",
  "format": "json"
}
```

### 7. Análises Especializadas

#### Tráfego HTTP
```http
GET /api/sniffer/analyze/http
```

#### Tráfego DNS
```http
GET /api/sniffer/analyze/dns
```

#### Top Talkers (IPs com mais tráfego)
```http
GET /api/sniffer/analyze/top-talkers?limit=10
```

## Uso Programático

### Exemplo Básico

```python
from backend.ferramentas.sniffer.sniffer import PacketSniffer

# Criar sniffer
sniffer = PacketSniffer(interface="eth0", filter_expr="tcp port 80")

# Iniciar captura
result = sniffer.start_capture(packet_count=100)

# Aguardar um pouco
import time
time.sleep(10)

# Parar captura
sniffer.stop_capture()

# Obter resultados
stats = sniffer.get_statistics()
packets = sniffer.get_packets()

print(f"Capturados {stats['total_packets']} pacotes")
```

### Exemplo com Análise

```python
from backend.ferramentas.sniffer.sniffer import (
    PacketSniffer, 
    analyze_http_traffic, 
    get_top_talkers
)

sniffer = PacketSniffer()
sniffer.start_capture(timeout=30)

# Aguardar captura
time.sleep(30)

packets = sniffer.get_packets()

# Analisar tráfego HTTP
http_packets = analyze_http_traffic(packets)
print(f"Pacotes HTTP: {len(http_packets)}")

# Top talkers
top_ips = get_top_talkers(packets, limit=5)
for ip, bytes_count in top_ips:
    print(f"{ip}: {bytes_count} bytes")
```

## Filtros BPF Comuns

### Por Protocolo
- `tcp` - Apenas TCP
- `udp` - Apenas UDP
- `icmp` - Apenas ICMP

### Por Porta
- `port 80` - Porta 80 (HTTP)
- `port 443` - Porta 443 (HTTPS)
- `port 53` - Porta 53 (DNS)

### Por Host
- `host 192.168.1.1` - Tráfego de/para IP específico
- `src host 192.168.1.1` - Apenas origem
- `dst host 192.168.1.1` - Apenas destino

### Combinações
- `tcp and port 80` - TCP na porta 80
- `udp and port 53` - DNS
- `host 192.168.1.1 and port 22` - SSH para IP específico

## Limitações e Considerações

### Privilégios
- **Linux/Mac:** Requer privilégios de root para captura
- **Windows:** Requer execução como administrador

### Performance
- Limite padrão de 1000 pacotes em memória
- Pacotes antigos são removidos automaticamente
- Use filtros para reduzir carga

### Segurança
- Pode capturar dados sensíveis
- Use apenas em redes autorizadas
- Respeite políticas de privacidade

## Teste

Execute o script de teste para verificar a instalação:

```bash
# Teste sem captura real
python test_sniffer.py --no-capture

# Teste completo (requer privilégios administrativos)
python test_sniffer.py
```

## Troubleshooting

### Erro: "Scapy não está disponível"
- Instale: `pip install scapy`
- Windows: Instale Npcap

### Erro: "Permission denied"
- Linux/Mac: Execute com `sudo`
- Windows: Execute como administrador

### Erro: "Interface not found"
- Verifique interfaces disponíveis: `/api/sniffer/interfaces`
- Use interface correta para seu sistema

### Performance baixa
- Use filtros BPF mais específicos
- Reduza limite de pacotes
- Verifique recursos do sistema

## Integração com Frontend

O sniffer pode ser facilmente integrado com aplicações web:

1. **Streamlit**: Use as funções diretamente
2. **React/Vue**: Consume a API REST
3. **Dashboard**: Implemente polling para estatísticas em tempo real

## Exemplos de Interface

```javascript
// Exemplo JavaScript para frontend
async function startCapture() {
    const response = await fetch('/api/sniffer/start', {
        method: 'POST',
        headers: {'Content-Type': 'application/json'},
        body: JSON.stringify({
            interface: 'eth0',
            filter: 'tcp port 80',
            timeout: 60
        })
    });
    const result = await response.json();
    console.log(result);
}

// Polling para estatísticas
setInterval(async () => {
    const response = await fetch('/api/sniffer/status');
    const stats = await response.json();
    updateDashboard(stats);
}, 1000);
```
