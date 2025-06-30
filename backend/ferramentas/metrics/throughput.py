import socket
import threading
import time

BUFFER_SIZE = 1024 * 8  # 8KB por pacote
DURATION = 5  # segundos

def start_server(host='0.0.0.0', port=5002):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind((host, port))
        server.listen(1)
        print(f"[Servidor] Aguardando conexão em {host}:{port}")
        conn, addr = server.accept()
        print(f"[Servidor] Conectado por {addr}")

        total_received = 0
        start = time.time()

        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            total_received += len(data)

        end = time.time()
        elapsed = end - start
        throughput = total_received / elapsed / 1024  # KB/s

        print(f"[Servidor] Vazão: {throughput:.2f} KB/s")

def start_client(server_ip='127.0.0.1', port=5002):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect((server_ip, port))
        print(f"[Cliente] Conectado a {server_ip}:{port}")

        data = b'a' * BUFFER_SIZE
        start = time.time()

        while time.time() - start < DURATION:
            client.sendall(data)

        print(f"[Cliente] Envio concluído")

if __name__ == '__main__':
    choice = input("Digite 's' para servidor ou 'c' para cliente: ").lower()
    if choice == 's':
        start_server()
    else:
        start_client()
