from flask import jsonify, request
import datetime
import socket

def hello():
    agora = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    client_ip = request.remote_addr
    user_agent = request.headers.get('User-Agent')
    hostname = socket.gethostname()
    
    return jsonify({
        "client_ip": client_ip,
        "user_agent": user_agent,
        "server_hostname": hostname,
        "data": agora,
        "message": "Olá do backend Flask!"
    })
