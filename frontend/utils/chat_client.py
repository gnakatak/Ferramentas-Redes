import streamlit as st
import streamlit.components.v1 as components

st.title("💬 Mini Chat em Tempo Real")

# URL do WebSocket do backend Flask-SocketIO
websocket_url = "ws://localhost:5000/socket.io/?EIO=4&transport=websocket"

components.html(f"""
<!DOCTYPE html>
<html>
  <body>
    <div>
      <h3>Chat</h3>
      <div id="chat-box" style="border:1px solid #ccc; height:200px; overflow:auto; padding:5px;"></div>
      <input id="msg" type="text" placeholder="Digite sua mensagem..." style="width:80%;"/>
      <button onclick="sendMessage()">Enviar</button>
    </div>

    <script>
      let socket = new WebSocket("{websocket_url}");

      socket.onopen = () => {{
        const chatBox = document.getElementById("chat-box");
        chatBox.innerHTML += "<p><em>Conectado ao chat.</em></p>";
      }};

      socket.onmessage = (event) => {{
        const chatBox = document.getElementById("chat-box");
        chatBox.innerHTML += "<p>" + event.data + "</p>";
        chatBox.scrollTop = chatBox.scrollHeight;
      }};

      function sendMessage() {{
        let input = document.getElementById("msg");
        if (input.value.trim() !== "") {{
          socket.send(input.value);
          input.value = "";
        }}
      }}
    </script>
  </body>
</html>
""", height=350)