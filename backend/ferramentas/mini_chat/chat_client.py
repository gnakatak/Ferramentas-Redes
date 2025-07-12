import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="Mini Chat", layout="wide")
st.title("💬 Mini Chat em Tempo Real")

# Usa CDN do Socket.IO client
components.html(f"""
<!DOCTYPE html>
<html>
  <head>
    <script src="https://cdn.socket.io/4.7.5/socket.io.min.js"></script>
  </head>
  <body>
    <div>
      <h3>Chat</h3>
      <div id="chat-box" style="border:1px solid #ccc; height:250px; overflow:auto; padding:5px; background:#f9f9f9;"></div>
      <input id="msg" type="text" placeholder="Digite sua mensagem..." style="width:80%;" onkeydown="if(event.key==='Enter')sendMessage();"/>
      <button onclick="sendMessage()">Enviar</button>
    </div>
    <script>
      var socket = io("ws://localhost:5000", {{
        transports: ["websocket"]
      }});
      socket.on("connect", function() {{
        const chatBox = document.getElementById("chat-box");
        chatBox.innerHTML += "<p><em>Conectado ao chat.</em></p>";
      }});
      socket.on("message", function(msg) {{
        const chatBox = document.getElementById("chat-box");
        chatBox.innerHTML += "<p>" + msg + "</p>";
        chatBox.scrollTop = chatBox.scrollHeight;
      }});
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
