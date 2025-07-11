import streamlit as st
import websocket
print("websocket importado de:", websocket.__file__)
import threading
import time

st.set_page_config(page_title="Mini Chat", layout="wide")
st.title("💬 Mini Chat com WebSocket")

# Variável para armazenar mensagens
if "messages" not in st.session_state:
    st.session_state.messages = []

# Função para ouvir mensagens do servidor
def listen():
    def on_message(ws, message):
        st.session_state.messages.append(message)
        st.experimental_rerun()

    def on_error(ws, error):
        print("Erro:", error)

    def on_close(ws, close_status_code, close_msg):
        print("Conexão encerrada")

    ws = websocket.WebSocketApp(
        "ws://localhost:5000/socket.io/?EIO=4&transport=websocket",
        on_message=on_message,
        on_error=on_error,
        on_close=on_close
    )
    ws.run_forever()

# Inicia a thread de escuta só uma vez
if "listener_started" not in st.session_state:
    threading.Thread(target=listen, daemon=True).start()
    st.session_state.listener_started = True

# Campo para digitar mensagem
with st.form(key="chat_form"):
    user_msg = st.text_input("Digite sua mensagem:")
    submitted = st.form_submit_button("Enviar")
    if submitted and user_msg.strip():
        try:
            ws = websocket.create_connection("ws://localhost:5000/socket.io/?EIO=4&transport=websocket")
            ws.send(user_msg)
            ws.close()
        except Exception as e:
            st.error(f"Erro ao enviar mensagem: {e}")
        st.session_state.messages.append(f"Você: {user_msg}")

# Exibir mensagens
st.subheader("Mensagens:")
for msg in st.session_state.messages:
    st.markdown(f"- {msg}")
