````markdown
# Estrutura do Projeto: Ferramentas-Redes

Este projeto tem como objetivo criar uma aplicação com diversas ferramentas voltadas para o ensino e demonstração prática de conceitos de redes de computadores. Abaixo, está detalhada toda a estrutura do projeto com explicações para que qualquer pessoa possa entender facilmente onde e como contribuir.

## 🚀 Como Executar a Aplicação

### ⭐ NOVO - Versão Integrada (Recomendado)
```bash
python run_streamlit.py
```
**Nova arquitetura totalmente integrada:**
- ✅ Apenas Streamlit (sem backend Flask)
- ✅ Sniffer integrado diretamente 
- ✅ Mais simples e rápido
- ✅ Menos dependências

### Métodos Antigos (com backend Flask)
```bash
# Método completo com backend + frontend
python run_app.py

# Versão melhorada
python run_all_improved.py
```

### Via VS Code Tasks
- Pressione `Ctrl+Shift+P`
- Digite "Tasks: Run Task"  
- Selecione "Run Main App (app.py)" ou "Run Frontend (Streamlit)"

## 📱 Acessando a Aplicação
- **Nova Versão Integrada**: http://localhost:8501 (apenas Streamlit)
- **Versão Antiga**: http://localhost:8501 + http://localhost:5000 (Flask + Streamlit)

## 🗂  Estrutura Geralrkdown
# Estrutura do Projeto: Ferramentas-Redes

Este projeto tem como objetivo criar uma aplicação com diversas ferramentas voltadas para o ensino e demonstração prática de conceitos de redes de computadores. Abaixo, está detalhada toda a estrutura do projeto com explicações para que qualquer pessoa possa entender facilmente onde e como contribuir.

## 🗂  Estrutura Geral

```bash
Ferramentas-Redes/
├── backend/               # Servidor Flask e lógica das ferramentas
│   ├── ferramentas/       # Ferramentas do sistema divididas por funcionalidade
│   │   ├── firewall/      # Ferramenta de firewall
│   │   │ 
│   │   ├── metrics/       # Ferramentas para métricas de rede
│   │   │ 
│   │   ├── mini_chat/     # Ferramenta de chat
│   │   │ 
│   │   ├── sniffer/       # Ferramenta sniffer de pacotes
│   │   │ 
│   │   ├── routes.py      # Rotas do backend
│   │   ├── server.py      # Onde vai rodar o backend
│   │   └── utils.py       # Utilitários do backend
│
├── frontend/              # Interface do usuário com Streamlit
│   ├── static/            # Arquivos estáticos (imagens, css, js)
│   ├── utils/             # Utilitários do frontend
│   │   ├── app.py
│   │   ├── dashboard.py
│   ├── README.md
│
├── requirements.txt       # Lista de bibliotecas necessárias
├── README.md              # Documentação principal do projeto
├── run_all.py             # Script para iniciar frontend e backend simultaneamente
└── .gitignore             # Arquivos ignorados pelo Git
````

---

## Arquivos e Pastas

### 📅 app.py

* Arquivo principal da aplicação.
* Responsável por iniciar o servidor Flask e integrar o frontend (Streamlit) com o backend.

### 📅 requirements.txt

* Lista todas as dependências do projeto.
* Use `pip install -r requirements.txt` para instalar.

### 📅 README.md

* Contém as instruções gerais do projeto, incluindo estrutura, instalação, execução e explicação de pastas (como este texto).

---

## 📚 frontend/

* Contém os componentes visuais e a interface com o usuário usando Streamlit.


#### static/

* Guarda arquivos estáticos como imagens, CSS customizado ou JavaScript opcional.

#### utils/

* Funções auxiliares para manipulação de dados ou layout.

---

## 📁 backend/

* Lógica de negócio, regras de firewall, captura de pacotes, chat, métricas de rede etc.

#### routes.py

* Define os endpoints (rotas) para comunicação entre frontend e backend (via HTTP ou WebSocket).

#### utils.py

* Funções reutilizáveis para o backend inteiro (ex: logs, manipulação de strings, validações).

---

## 📂 services/

* Cada subpasta representa uma "ferramenta" distinta do sistema.

### 🔐 firewall/

* Implementa um firewall personalizado em Python.

Arquivos:

* `firewall.py`: lógica principal de interceptação e bloqueio de pacotes.
* `rules.json`: armazena as regras configuradas (IPs bloqueados, portas, protocolos).
* `utils.py`: auxiliares como validação de IPs, leitura de regras, etc.

### 📡 sniffer/

* Sniffer de pacotes da rede.

Arquivos:

* `sniffer.py`: captura pacotes e exibe dados como origem, destino, protocolo e payload.

### 💬 mini\_chat/

* Módulo de chat em tempo real usando WebSockets.

Arquivos:

* `chat_server.py`: gerencia conexões, mensagens e canais.

### 📊 metrics/

* Ferramentas para medir desempenho da rede.

Arquivos:

* `ping.py`: envia pings e calcula latência.
* `throughput.py`: simula transferências para medir vazão da rede.

---

## ✨ Boas práticas

* Sempre que for adicionar uma nova funcionalidade:

  * Crie um novo arquivo ou funcão em `services`.
  * Exporte-a via `routes.py` ou chame via `dashboard.py`.
* Evite deixar código duplicado. Utilize `utils.py`.
* Atualize o `README.md` conforme modificações relevantes no projeto.

---

Com esta estrutura clara e modular, você e seus colegas podem colaborar com facilidade, criando novas ferramentas ou expandindo as existentes de forma organizada.

## 📦 Bibliotecas utilizadas no projeto Ferramentas-Redes

As seguintes bibliotecas são utilizadas para construir e executar as funcionalidades do projeto. Todas podem ser instaladas com o comando:

```bash
pip install -r requirements.txt
```

### Lista de dependências:

* `flask` — Servidor backend para integração com o frontend.
* `streamlit` — Criação de interfaces gráficas interativas usando Python.
* `scapy` — Captura, construção e manipulação de pacotes de rede.
* `pydivert` — Interface Python para o WinDivert (firewall no Windows).
* `pyshark` — Sniffer de pacotes baseado em tshark (alternativa ao scapy).
* `dnspython` — Biblioteca para manipulação e consulta de DNS.
* `websockets` — Comunicação em tempo real via WebSocket puro.
* `flask-socketio` — Integração de WebSocket com Flask.
* `eventlet` — Mecanismo assíncrono usado pelo Flask-SocketIO.
* `chart-studio` — Visualização de gráficos interativos (opcional).
* `pandas` — Manipulação e análise de dados estruturados.
* `matplotlib` — Geração de gráficos no backend.
* `psutil` — Monitoramento de recursos do sistema (CPU, memória, rede).
* `netifaces` — Leitura das interfaces de rede do sistema.

---

## 🚀 Executando o Projeto

O projeto Ferramentas-Redes é composto por dois componentes principais:

* 🧠 **Backend**: Servidor Flask responsável pela lógica das ferramentas e pela API.
* 🎨 **Frontend**: Interface de usuário interativa feita com Streamlit.

---

### 📦 Pré-requisitos

Certifique-se de que todas as dependências estejam instaladas com o comando abaixo:

```bash
pip install -r requirements.txt
```

---

### ▶️ Execução Automatizada

Para facilitar o desenvolvimento, você pode iniciar o frontend e backend ao mesmo tempo com um único comando:

```bash
python run_all.py
```

Esse script iniciará o servidor Flask e, em seguida, o Streamlit automaticamente. Pressione Ctrl+C para encerrar ambos.

---

### ▶️ Execução Manual

Abra dois terminais (ou duas abas/painéis no terminal).

#### 1️⃣ Terminal 1: Executar o servidor Flask (Backend)

```bash
python backend/server.py
```

Este comando iniciará o backend na URL:

```
http://localhost:5000
```

#### 2️⃣ Terminal 2: Executar a interface Streamlit (Frontend)

```bash
streamlit run frontend/app.py
```

Este comando abrirá automaticamente o frontend no navegador em:

```
http://localhost:8501
```

---

✅ A interface do usuário se comunica com o backend via HTTP e WebSockets, dependendo da ferramenta em uso.

```
```