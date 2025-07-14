
# 🌐 Ferramentas de Rede

Este projeto visa consolidar diversas ferramentas úteis para análise e monitoramento de redes em uma única aplicação web interativa, desenvolvida com Streamlit. É uma plataforma ideal para educação, demonstração de conceitos de rede e uso prático no dia a dia.

## 🗂 Estrutura do Projeto

A estrutura do projeto foi simplificada e focada na organização das ferramentas em um único diretório para facilitar a gestão.

```

Ferramentas-Redes/
├── app.py                     \# Arquivo principal da aplicação Streamlit
├── requirements.txt           \# Lista de bibliotecas Python necessárias
├── .devcontainer/             \# Configurações para ambientes de desenvolvimento (ex: VS Code Dev Containers)
│   └── devcontainer.json
├── ferramentas/               \# Módulos de cada ferramenta de rede
│   ├── **init**.py            \# Torna 'ferramentas' um pacote Python
│   ├── chat.py                \# Módulo da ferramenta de Chat em tempo real
│   ├── dashboard.py           \# Módulo do Dashboard com ping e informações gerais
│   ├── port\_scanner.py        \# Módulo do Verificador de Portas
│   ├── postman.py             \# Módulo da ferramenta de Requisições HTTP (Postman-like)
│   ├── speedtest\_module.py    \# Módulo da ferramenta SpeedTest
│   ├── traceroute\_dev.py      \# Módulo da ferramenta Traceroute
│   ├── visualizador\_ip.py     \# Módulo do Visualizador de IP e Localização
│   └── whois\_module.py        \# Módulo da ferramenta WHOIS
├── README.md                  \# Este arquivo de documentação
├── chat.db                    \# Database que armazena mensagens trocas no chat por usuários  
└── .gitignore                 \# Arquivos e pastas ignorados pelo Git

```

## 🚀 Como Executar o Projeto

### Pré-requisitos

Certifique-se de ter o Python 3.x instalado em sua máquina.

1. **Clone o Repositório:**

```

git clone "https://github.com/gnakatak/Ferramentas-Redes/tree/main"
cd Ferramentas-Redes

```

2. **Crie e Ative um Ambiente Virtual (Recomendado):**

```

python -m venv venv

# No Windows:

.\\venv\\Scripts\\activate

# No macOS/Linux:

source venv/bin/activate

```

3. **Instale as Dependências:**

```

pip install -r requirements.txt

```

### Execução da Aplicação

Após instalar as dependências, você pode iniciar a aplicação Streamlit:

```

streamlit run app.py

```

Isso abrirá automaticamente a aplicação em seu navegador padrão, geralmente em `http://localhost:8501`.

## 📦 Dependências do Projeto

As seguintes bibliotecas Python são utilizadas no projeto. Elas estão listadas no arquivo `requirements.txt` e podem ser instaladas com `pip install -r requirements.txt`.

* `streamlit`: Framework para construir aplicações web interativas com Python.

* `pandas`: Biblioteca para manipulação e análise de dados, amplamente utilizada para estruturar os resultados das ferramentas.

* `speedtest-cli`: Ferramenta de linha de comando para testar a velocidade da internet.

* `streamlit-extras`: Coleção de componentes extras para Streamlit.

* `streamlit-autorefresh`: Permite a atualização automática de partes da aplicação Streamlit.

* `python-whois`: Biblioteca para realizar consultas WHOIS em domínios.

* `requests`: Biblioteca HTTP para fazer requisições web (usada em Postman, Visualizador de IP, WHOIS).

* `certifi`: Pacote de certificados SSL para requisições seguras.

* `urllib3`: Biblioteca de pooling de conexão HTTP, usada internamente por `requests`.

* `socket`: Módulo padrão do Python para programação de rede de baixo nível (usado em Port Scanner).

* `sqlite3`: Módulo padrão do Python para interagir com bancos de dados SQLite (usado no Chat).

* `datetime`: Módulo padrão do Python para manipulação de datas e horas.

* `time`: Módulo padrão do Python para funções relacionadas ao tempo.

* `logging`: Módulo padrão do Python para registro de eventos (usado em SpeedTest).

* `platform`: Módulo padrão do Python para acessar dados da plataforma subjacente (usado em Traceroute).

* `subprocess`: Módulo padrão do Python para spawnar novos processos (usado em Traceroute).

* `re`: Módulo padrão do Python para expressões regulares (usado em Traceroute).

* `shutil`: Módulo padrão do Python para operações de alto nível em arquivos e coleções de arquivos (usado em Traceroute).

## 🛠 Ferramentas Incluídas

O projeto oferece as seguintes ferramentas de rede, cada uma com seu próprio módulo Python dentro da pasta `ferramentas/`:

### 🌍 Visualizador de IP e Localização (`visualizador_ip.py`)

* **Descrição:** Exibe o IP público do usuário e as informações de localização (cidade, região, país, ISP) utilizando a API `ipinfo.io`. Também mostra as informações do servidor onde a aplicação Streamlit está hospedada.

* **Como Funciona:**

  * `get_ipinfo_details(ip=None)`: Função que faz uma requisição GET para `https://ipinfo.io/json` (ou `https://ipinfo.io/{ip}/json` se um IP for fornecido) para obter os detalhes geográficos.

  * `ip_viewer()`: Renderiza a interface Streamlit, chamando `get_ipinfo_details` para obter e exibir as informações do IP do servidor e do usuário.

### ⚡ SpeedTest (`speedtest_module.py`)

* **Descrição:** Realiza testes de velocidade de download, upload e ping da sua conexão de internet. Permite monitoramento contínuo em intervalos definidos, exibindo gráficos e métricas médias.

* **Como Funciona:**

  * Utiliza a biblioteca `speedtest` para se conectar aos servidores de teste mais próximos.

  * `testar_velocidade()`: Executa os testes de download, upload e ping. Armazena os resultados em `st.session_state` para persistência e visualização.

  * A interface permite iniciar/parar o monitoramento e exibe os dados em uma tabela e gráficos de linha.

### 🗺️ Traceroute (`traceroute_dev.py`)

* **Descrição:** Rastreia o caminho que os pacotes de dados percorrem até um destino na rede, exibindo cada salto (roteador) com seu IP, hostname e latência.

* **Como Funciona:**

  * `contar_saltos(destino, max_saltos)`: Executa o comando de sistema `traceroute` (Linux/macOS) ou `tracert` (Windows) em um subprocesso.

  * Analisa a saída do comando em tempo real, extraindo informações sobre cada salto e exibindo-as em uma tabela Streamlit.

  * Lida com diferenças de comandos e codificação entre sistemas operacionais.

### 💬 Chat em Tempo Real (`chat.py`)

* **Descrição:** Um mini-chat para comunicação em tempo real, ideal para demonstrações de comunicação via rede.

* **Como Funciona:**

  * Utiliza um banco de dados SQLite (`chat.db`) para armazenar mensagens e usuários.

  * `init_db()`: Inicializa as tabelas `messages` e `users` no banco de dados.

  * `add_message()` / `get_messages()`: Funções para adicionar e recuperar mensagens do banco.

  * `manage_user()` / `get_active_users()`: Funções para rastrear usuários ativos e inativos.

  * A interface usa `st.form` para envio de mensagens e `st.empty()` com `time.sleep()` e `st.rerun()` para simular atualizações de chat em tempo real, embora de forma básica sem WebSockets para o backend Flask.

### 📬 Ferramenta de Requisições HTTP (Postman-like) (`postman.py`)

* **Descrição:** Permite enviar requisições HTTP (GET, POST, PUT, DELETE) para qualquer URL, incluindo cabeçalhos e corpo da requisição (JSON). Exibe o código de status, cabeçalhos de resposta e corpo da resposta.

* **Como Funciona:**

  * Utiliza a biblioteca `requests` para fazer as requisições HTTP.

  * A interface Streamlit permite ao usuário selecionar o método HTTP, inserir a URL, cabeçalhos (em formato JSON) e o corpo da requisição (também em JSON).

  * Faz o parse das strings JSON de entrada e tenta exibir o corpo da resposta como JSON, ou como texto puro se não for JSON válido.

  * Inclui tratamento básico de erros para problemas de conexão e timeout.

### 📑 Consulta WHOIS + Localização (`whois_module.py`)

* **Descrição:** Permite consultar informações WHOIS de um domínio (data de criação, expiração, registrar, DNS, status) e obter a localização geográfica do IP associado.

* **Como Funciona:**

  * Utiliza a biblioteca `python-whois` para obter os dados WHOIS do domínio.

  * Para a localização, primeiro resolve o IP do domínio usando a API DNS do Google (`https://dns.google/resolve`).

  * Em seguida, usa a função `get_ipinfo` (presente neste módulo) para obter os detalhes geográficos do IP via `ipinfo.io`.

  * Inclui formatação de datas e tratamento de erros SSL com um fallback (não recomendado para produção) para o DNS do Google.

### 🛡️ Verificador de Portas (Port Scanner) (`port_scanner.py`)

* **Descrição:** Escaneia um alvo (IP ou domínio) para verificar quais portas TCP estão abertas em um intervalo especificado.

* **Como Funciona:**

  * `scan_port(target_host, port, timeout)`: Tenta estabelecer uma conexão TCP com a porta do alvo usando o módulo `socket` do Python. Um `timeout` é usado para evitar travamentos.

  * `get_common_service(port)`: Retorna o nome de um serviço comum associado à porta, se conhecido.

  * A interface permite ao usuário inserir o alvo e um intervalo de portas. Exibe uma barra de progresso e lista as portas abertas.

  * Lida com a resolução de hostname para IP e erros de conexão.

## ✨ Boas Práticas e Colaboração

* **Modularização:** Cada ferramenta reside em seu próprio arquivo na pasta `ferramentas/` para manter o código organizado.

* **Reuso:** Utilize funções auxiliares e componentes do Streamlit para evitar duplicação de código.

* **Documentação:** Mantenha este `README.md` atualizado com as modificações relevantes no projeto e as explicações das novas ferramentas.

* **Estado da Sessão:** A função `reset_speedtest_state()` é crucial para limpar os dados de sessão do SpeedTest ao navegar entre as páginas, garantindo que o estado não seja persistente indevidamente.

Com esta estrutura clara e modular, você e seus colaboradores podem expandir e manter o projeto de forma organizada e eficiente
