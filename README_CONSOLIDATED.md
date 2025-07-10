# 🌐 Ferramentas de Redes - Sniffer de Pacotes

## 📋 Visão Geral

Este projeto implementa um **sniffer de pacotes** completo em Python com interface web, capaz de capturar e analisar tráfego de rede em tempo real. O projeto foi **depurado e consolidado** para máxima estabilidade e facilidade de uso.

## ✨ Características

### 🎯 **Versão Integrada (Recomendada)**
- **Interface única:** Streamlit + PyShark integrados
- **Dependências mínimas:** Apenas 3 pacotes essenciais
- **Mais estável:** Sem comunicação HTTP, menos pontos de falha
- **Mais rápido:** Execução direta, sem overhead de servidor

### 🔧 **Funcionalidades Principais**
- 📡 **Captura em tempo real** de pacotes de rede
- 🔍 **Filtros personalizados** (BPF - Berkeley Packet Filter)
- 📊 **Análise de protocolos** (TCP, UDP, HTTP, DNS, ICMP)
- 📈 **Estatísticas em tempo real** (pacotes/segundo, top talkers)
- 💾 **Exportação de dados** (JSON, CSV)
- 🔄 **Fallback robusto** (PyShark → subprocess/tshark)
- 🛡️ **Detecção automática** de privilégios administrativos

## 🚀 Instalação e Uso

### 1️⃣ **Instalação das Dependências**
```bash
# Dependências mínimas (versão integrada)
pip install -r requirements_integrated.txt

# OU dependências completas (arquitetura backend/frontend)
pip install -r requirements.txt
```

### 2️⃣ **Pré-requisitos de Sistema**

#### Windows:
- **Npcap:** Baixe e instale do [site oficial](https://nmap.org/npcap/)
  - ✅ Marque "Install Npcap in WinPcap API-compatible Mode"
- **Privilégios:** Execute como Administrador

#### Linux/Mac:
- **Privilégios:** Execute com `sudo`
- **Dependências:** `sudo apt install tshark` (opcional, para fallback)

### 3️⃣ **Execução**

#### 🎯 **Método Simples (Recomendado):**
```bash
# Teste opcional (verificação pré-execução)
python test_pre_run.py

# Execução principal
python run_integrated.py

# OU versão melhorada com diagnósticos
python run_integrated_improved.py
```

#### 🔒 **Windows (solicita admin automaticamente):**
```bash
python run_admin.py
```

#### 🏗️ **Arquitetura Completa (backend + frontend):**
```bash
python run_all_improved.py
```

### 4️⃣ **Acesso**
- **Interface Web:** http://localhost:8501
- **API REST:** http://localhost:5000 (apenas na arquitetura completa)

## 📂 Estrutura do Projeto

```
📁 backend/
  📁 ferramentas/
    📁 sniffer/
      📄 sniffer.py          # 🎯 Módulo principal do sniffer
      📄 __init__.py
    📁 firewall/             # Módulos auxiliares
    📁 metrics/
    📁 mini_chat/
  📄 server.py              # Servidor Flask (arquitetura completa)
  📄 routes.py              # Rotas da API

📁 frontend/
  📄 app_integrated.py      # 🎯 Interface Streamlit integrada
  📄 app.py                # Interface cliente (arquitetura completa)

📄 run_integrated.py       # 🎯 Script principal (recomendado)
📄 run_admin.py           # Script com privilégios admin
📄 run_all_improved.py    # Arquitetura completa melhorada
📄 test_comprehensive.py  # 🎯 Teste abrangente principal

📄 requirements_integrated.txt  # Dependências mínimas
📄 requirements.txt            # Dependências completas
```

## 🧪 Testes

### Scripts de Teste Principais:
- **`test_comprehensive.py`** - Teste abrangente de todo o projeto
- **`test_pre_run.py`** - Validação rápida pré-execução
- **`test_sniffer.py`** - Demonstração da API do sniffer

```bash
# Teste completo
python test_comprehensive.py --export

# Validação rápida
python test_pre_run.py
```

## 🔧 Configuração e Personalização

### Filtros de Captura (BPF):
```python
# Exemplos de filtros
"tcp port 80"           # Tráfego HTTP
"udp port 53"           # Tráfego DNS
"icmp"                  # Pings
"host 192.168.1.1"      # Tráfego de/para IP específico
"port 22 or port 80"    # SSH ou HTTP
```

### Interfaces Disponíveis:
- **`any`** - Todas as interfaces (padrão)
- **`eth0`** - Interface Ethernet específica
- **`wlan0`** - Interface Wi-Fi específica
- **Auto-detecção** - O sistema detecta automaticamente

## 📊 Funcionalidades da Interface

### 🔍 **Captura de Pacotes:**
- Seleção de interface de rede
- Filtros BPF personalizados
- Controle de quantidade e tempo limite
- Monitoramento em tempo real

### 📈 **Análise e Estatísticas:**
- Protocolos mais usados
- Top talkers (IPs com mais tráfego)
- Análise específica de HTTP/DNS
- Taxa de pacotes por segundo

### 💾 **Exportação:**
- Formato JSON (completo)
- Formato CSV (compatibilidade)
- Download direto pela interface

## 🛠️ Solução de Problemas

### ❌ **"PyShark falha silenciosamente"**
- **Solução:** Use `run_integrated_improved.py` para diagnóstico completo
- **Verificação:** Execute `python test_comprehensive.py`
- **Fallback:** O sistema tenta tshark automaticamente

### ❌ **"PyShark não funciona"**
- **Windows:** Instale Npcap com modo WinPcap
- **Linux:** `sudo apt install wireshark-common`
- **Fallback:** O sistema tenta usar tshark automaticamente

### ❌ **"Privilégios insuficientes"**
- **Windows:** Execute `run_admin.py` ou como Administrador
- **Linux/Mac:** Use `sudo python run_integrated.py`

### ❌ **"Nenhuma interface encontrada"**
- Verifique privilégios administrativos
- Tente usar interface `any` (padrão)
- Reinstale Npcap (Windows) ou permissions (Linux)

### ❌ **"ImportError"**
- Verifique instalação: `pip install -r requirements_integrated.txt`
- Use ambiente virtual Python

### ❌ **"Captura retorna 0 pacotes"**
- Verifique se há tráfego de rede ativo
- Tente remover filtros BPF
- Use `run_integrated_improved.py` para diagnóstico
- Verifique configurações de firewall local

## 🔍 Falsos Positivos de Lint

Os seguintes avisos do linter são **NORMAIS** e podem ser ignorados:
- `Import "ferramentas.sniffer.sniffer" could not be resolved` - Path dinâmico
- `Import "netifaces" could not be resolved` - Dependência opcional
- `os.geteuid() only available on Unix` - Código tem verificação de plataforma

## 📝 API de Programação

### Uso Básico:
```python
from backend.ferramentas.sniffer.sniffer import PacketSniffer

# Criar sniffer
sniffer = PacketSniffer(interface='any', filter_expr='tcp port 80')

# Iniciar captura
result = sniffer.start_capture(packet_count=100, timeout=30)

# Obter estatísticas
stats = sniffer.get_statistics()

# Obter pacotes
packets = sniffer.get_packets(limit=50)

# Parar captura
sniffer.stop_capture()

# Exportar dados
sniffer.export_packets(format='json', filename='capture.json')
```

## 🎯 Recomendações

### ✅ **Para a maioria dos usuários:**
- Use `run_integrated.py` - mais simples e estável
- Execute como administrador
- Use filtros BPF para focar no tráfego relevante

### ✅ **Para desenvolvimento:**
- Use `run_all_improved.py` para arquitetura completa
- Execute `test_comprehensive.py` após mudanças
- Consulte os guias `TESTING_GUIDE.md` e `EXECUTION_GUIDE.md`

## 📞 Suporte

Para problemas ou dúvidas:
1. Execute `python test_comprehensive.py` para diagnóstico
2. Consulte os logs de erro na interface
3. Verifique os guias de solução de problemas acima

---

**🎉 Projeto consolidado, testado e pronto para uso!**
