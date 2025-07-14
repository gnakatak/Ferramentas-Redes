# 🌐 Ferramentas de Rede

Este projeto visa consolidar diversas ferramentas úteis para **análise e monitoramento de redes** em uma única **aplicação web interativa**, desenvolvida com **Streamlit**. É uma plataforma ideal para **educação**, **demonstração de conceitos de rede** e **uso prático no dia a dia**.

---

## 🗂 Estrutura do Projeto

A estrutura do projeto foi simplificada e focada na organização das ferramentas em um único diretório:

Ferramentas-Redes/
├── app.py # Arquivo principal da aplicação Streamlit
├── requirements.txt # Lista de bibliotecas Python necessárias
├── .devcontainer/ # Configurações para ambientes de desenvolvimento (VS Code)
│ └── devcontainer.json
├── ferramentas/ # Módulos de cada ferramenta de rede
│ ├── init.py
│ ├── chat.py
│ ├── dashboard.py
│ ├── port_scanner.py
│ ├── postman.py
│ ├── speedtest_module.py
│ ├── traceroute_dev.py
│ ├── visualizador_ip.py
│ └── whois_module.py
├── README.md # Este arquivo de documentação
├── chat.db # Banco de dados SQLite do chat
└── .gitignore # Arquivos e pastas ignorados pelo Git

yaml
Copiar
Editar

---

## 🚀 Como Executar o Projeto

### ✅ Pré-requisitos

- Python 3.x instalado na máquina

### 📥 Clone o Repositório

```bash
git clone "https://github.com/gnakatak/Ferramentas-Redes/tree/main"
cd Ferramentas-Redes
🧪 Crie e Ative um Ambiente Virtual (Recomendado)
bash
Copiar
Editar
python -m venv venv

# No Windows:
.\venv\Scripts\activate

# No macOS/Linux:
source venv/bin/activate
📦 Instale as Dependências
bash
Copiar
Editar
pip install -r requirements.txt
▶️ Execute a Aplicação
bash
Copiar
Editar
streamlit run app.py
A aplicação será aberta automaticamente no navegador em: http://localhost:8501

📦 Dependências do Projeto
O projeto depende das seguintes bibliotecas:

streamlit – Aplicações web interativas

pandas – Manipulação e análise de dados

speedtest-cli – Testes de velocidade de internet

streamlit-extras, streamlit-autorefresh – Componentes extras e atualização automática

python-whois – Consulta WHOIS de domínios

requests – Requisições HTTP

certifi, urllib3 – Requisições HTTPS seguras

Módulos padrão do Python:

socket, sqlite3, datetime, time, logging, platform, subprocess, re, shutil

🛠 Ferramentas Incluídas
🌍 Visualizador de IP e Localização (visualizador_ip.py)
Exibe o IP público do usuário e informações de geolocalização via ipinfo.io.

get_ipinfo_details(ip=None) – Faz requisição à API para obter os dados.

ip_viewer() – Renderiza os dados no Streamlit.

⚡ SpeedTest (speedtest_module.py)
Testa velocidade de download, upload e ping. Permite monitoramento contínuo com gráficos.

testar_velocidade() – Executa os testes e salva no st.session_state.

🗺️ Traceroute (traceroute_dev.py)
Rastreia o caminho dos pacotes até um destino, exibindo IPs, nomes e latência de cada salto.

contar_saltos(destino, max_saltos) – Usa traceroute ou tracert via subprocesso.

💬 Chat em Tempo Real (chat.py)
Mini-chat com persistência em banco de dados SQLite.

init_db() – Inicializa as tabelas

add_message() / get_messages() – Insere e recupera mensagens

manage_user() / get_active_users() – Gerencia usuários conectados

📬 Requisições HTTP (Postman-like) (postman.py)
Permite requisições HTTP GET, POST, PUT e DELETE com customização de headers e body.

Interface com campos para URL, headers, body (em JSON)

Mostra resposta formatada (ou texto puro)

📑 Consulta WHOIS + Localização (whois_module.py)
Consulta dados WHOIS de domínios e localização geográfica do IP resolvido.

Usa python-whois e ipinfo.io

Resolve IP via API DNS do Google (https://dns.google/resolve)

🛡️ Verificador de Portas (port_scanner.py)
Escaneia portas TCP abertas em um host/domínio.

scan_port(host, port, timeout) – Tenta conectar via socket

get_common_service(port) – Retorna o nome do serviço padrão da porta

✨ Boas Práticas e Colaboração
Modularização: Cada ferramenta em seu módulo próprio na pasta ferramentas/.

Reuso: Use funções auxiliares e componentes compartilháveis para evitar repetição.

Documentação: Mantenha este README.md atualizado.

Sessão Limpa: A função reset_speedtest_state() limpa estados persistentes no SpeedTest.

🤝 Contribuições
Pull requests são bem-vindos! Para grandes mudanças, abra uma issue antes para discutir o que você gostaria de alterar.