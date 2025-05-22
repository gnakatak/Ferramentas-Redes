# server.py
from flask import Flask
from backend.routes import api_routes  # Certifique-se de que o nome do pacote e pasta está correto

app = Flask(__name__)
app.register_blueprint(api_routes)

if __name__ == '__main__':
    app.run(port=5000)
