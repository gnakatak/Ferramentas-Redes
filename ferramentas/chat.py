import streamlit as st
import sqlite3
import time
from datetime import datetime, timedelta

# Emoji mapping
EMOJI_MAP = {
    ":smile:": "😄", ":sad:": "😢", ":heart:": "❤️", ":thumbsup:": "👍",
    ":fire:": "🔥", ":clap:": "👏", ":laugh:": "😂", ":wink:": "😉",
    ":ok:": "👌", ":star:": "⭐"
}

def emojify(text):
    """Converte códigos de emoji em emojis Unicode."""
    for k, v in EMOJI_MAP.items():
        text = text.replace(k, v)
    return text

# Initialize SQLite database
def init_db():
    """Inicializa e conecta ao banco de dados SQLite."""
    # check_same_thread=False é crucial para SQLite em ambientes multi-thread como o Streamlit
    conn = sqlite3.connect("chat.db", check_same_thread=False)
    c = conn.cursor()
    # Tabela para armazenar as mensagens do chat
    c.execute("""
        CREATE TABLE IF NOT EXISTS messages (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user TEXT,
            message TEXT,
            timestamp TEXT,
            is_system BOOLEAN
        )
    """)
    # Tabela para rastrear usuários ativos
    c.execute("""
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            last_active TIMESTAMP
        )
    """)
    conn.commit()
    return conn

# Add or remove user, update last_active
def manage_user(username, action="add"):
    """Adiciona, remove ou atualiza o timestamp de atividade de um usuário."""
    conn = st.session_state.db
    c = conn.cursor()
    if action == "add":
        # INSERT OR IGNORE para evitar duplicatas se o usuário já existir
        c.execute("INSERT OR IGNORE INTO users (username, last_active) VALUES (?, ?)",
                  (username, datetime.now()))
    elif action == "remove":
        c.execute("DELETE FROM users WHERE username = ?", (username,))
    elif action == "update":
        c.execute("UPDATE users SET last_active = ? WHERE username = ?", (datetime.now(), username))
    conn.commit()

# Add a message to the database
def add_message(user, message, is_system=False):
    """Adiciona uma nova mensagem ao banco de dados."""
    conn = st.session_state.db
    c = conn.cursor()
    timestamp = datetime.now().strftime("%H:%M") # Formato de hora:minuto
    c.execute("INSERT INTO messages (user, message, timestamp, is_system) VALUES (?, ?, ?, ?)",
              (user, message, timestamp, is_system))
    conn.commit()

# Get all messages
def get_messages():
    """Recupera todas as mensagens do chat, ordenadas por ID."""
    conn = st.session_state.db
    c = conn.cursor()
    c.execute("SELECT user, message, timestamp, is_system FROM messages ORDER BY id")
    return c.fetchall()

# Get active users (active in last 5 minutes)
def get_users():
    """Recupera a lista de usuários ativos (últimos 5 minutos)."""
    conn = st.session_state.db
    c = conn.cursor()
    five_minutes_ago = datetime.now() - timedelta(minutes=5)
    c.execute("SELECT username FROM users WHERE last_active >= ?", (five_minutes_ago,))
    return [row[0] for row in c.fetchall()]

# Clean up inactive users
def cleanup_users():
    """Remove usuários inativos do banco de dados e registra a saída."""
    conn = st.session_state.db
    c = conn.cursor()
    five_minutes_ago = datetime.now() - timedelta(minutes=5)
    c.execute("SELECT username FROM users WHERE last_active < ?", (five_minutes_ago,))
    inactive_users = [row[0] for row in c.fetchall()]
    for user in inactive_users:
        c.execute("DELETE FROM users WHERE username = ?", (user,))
        add_message("Sistema", f"{user} saiu do chat.", is_system=True) # Registra a saída
    conn.commit()

# A função principal da página do chat
def chat_dev():
    """Renderiza a interface do chat em tempo real."""
    st.title("💬 Chat em Tempo Real")
    st.write("Converse com outros usuários em tempo real (suporta :smile: :heart: ...).")

    # Inicializa o banco de dados na sessão, se ainda não estiver inicializado
    if "db" not in st.session_state:
        st.session_state.db = init_db()

    # Inicializa variáveis de estado da sessão para o chat
    if "username" not in st.session_state:
        st.session_state.username = ""
    if "last_message_count" not in st.session_state:
        st.session_state.last_message_count = 0
    if "chat_active" not in st.session_state:
        st.session_state.chat_active = False

    # Entrada do nome de usuário
    if not st.session_state.username:
        username = st.text_input("Digite seu nome:", key="username_input")
        if st.button("Entrar", key="enter_chat_button"):
            if username.strip():
                st.session_state.username = username.strip()
                manage_user(st.session_state.username, "add")
                add_message("Sistema", f"{st.session_state.username} entrou no chat.", is_system=True)
                st.session_state.chat_active = True
                st.rerun() # Reinicia para mostrar a interface do chat
            else:
                st.warning("Por favor, digite um nome de usuário válido.")
    else:
        # Atualiza o timestamp de atividade do usuário
        manage_user(st.session_state.username, "update")

        # Limpa usuários inativos
        cleanup_users()

        # Exibe usuários online
        users = get_users()
        st.markdown(f"**Online:** {', '.join(u if u != st.session_state.username else f'**{u}**' for u in users)}")

        # Contêiner para as mensagens do chat
        chat_placeholder = st.empty() # Usar st.empty() para atualizar o conteúdo
        
        # Exibe as mensagens
        messages = get_messages()
        with chat_placeholder.container():
            for user, msg, timestamp, is_system in messages:
                # Estilos CSS para mensagens de sistema, do próprio usuário e de outros usuários
                if is_system:
                    st.markdown(f"<div style='font-style: italic; color: #888; text-align: center; margin: 8px 0;'>{msg}</div>", unsafe_allow_html=True)
                elif user == st.session_state.username:
                    st.markdown(f"<div style='display: flex; justify-content: flex-end; margin-bottom: 5px;'><div style='max-width: 70%; background: #e3f0fb; color: #1976d2; border-radius: 15px 15px 0 15px; padding: 10px 15px; box-shadow: 1px 1px 3px rgba(0,0,0,0.1);'><small style='font-weight: bold;'>Você</small><br>{emojify(msg)} <span style='font-size:0.75em;color:#888; display: block; text-align: right;'>{timestamp}</span></div></div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div style='display: flex; justify-content: flex-start; margin-bottom: 5px;'><div style='max-width: 70%; background: #f1f1f1; color: #333; border-radius: 15px 15px 15px 0; padding: 10px 15px; box-shadow: 1px 1px 3px rgba(0,0,0,0.1);'><small style='font-weight: bold;'>{user}</small><br>{emojify(msg)} <span style='font-size:0.75em;color:#888; display: block; text-align: right;'>{timestamp}</span></div></div>", unsafe_allow_html=True)

        # Usando st.form para o input da mensagem para lidar com a limpeza de forma mais limpa
        with st.form(key='chat_form', clear_on_submit=True):
            message_input = st.text_input("Digite sua mensagem:", key="chat_message_input") # Nova chave para o input dentro do form
            submit_button = st.form_submit_button("Enviar")

            if submit_button:
                if message_input.strip():
                    add_message(st.session_state.username, message_input.strip())
                    manage_user(st.session_state.username, "update")
                    # O clear_on_submit=True no st.form cuidará da limpeza do input
                    st.rerun() # Força o rerun para atualizar o chat
                else:
                    st.warning("A mensagem não pode estar vazia.")

        # Auto-refresh para simular atualizações em tempo real
        # Este loop fará o Streamlit recarregar a cada 2 segundos
        if st.session_state.chat_active:
            current_message_count = len(get_messages()) # Pega a contagem atual de mensagens
            if current_message_count > st.session_state.last_message_count:
                st.session_state.last_message_count = current_message_count
                st.rerun() # Força o rerun se houver novas mensagens
            else:
                time.sleep(2)  # Poll a cada 2 segundos
                st.rerun() # Força o rerun para verificar novas mensagens

