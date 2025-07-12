import socket
import threading
import time

BUFFER_SIZE = 1024 * 8  # 8KB por pacote
DURATION = 3  # segundos
PORT = 5002

def servidor_throughput(resultado):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server:
        server.bind(('localhost', PORT))
        server.listen(1)
        conn, addr = server.accept()

        total_received = 0
        start = time.time()

        while True:
            data = conn.recv(BUFFER_SIZE)
            if not data:
                break
            total_received += len(data)

        end = time.time()
        conn.close()

        elapsed = end - start
        throughput_kbps = (total_received / elapsed) / 1024
        resultado['throughput_kbps'] = round(throughput_kbps, 2)
        resultado['tempo_s'] = round(elapsed, 2)
        resultado['bytes_recebidos'] = total_received


def cliente_throughput():
    time.sleep(0.5)  # Garante que o servidor está pronto
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as client:
        client.connect(('localhost', PORT))
        data = b'x' * BUFFER_SIZE
        start = time.time()

        while time.time() - start < DURATION:
            client.sendall(data)

        client.shutdown(socket.SHUT_WR)


def medir_throughput():
    resultado = {}

    servidor_thread = threading.Thread(target=servidor_throughput, args=(resultado,))
    servidor_thread.start()

    try:
        cliente_throughput()
        servidor_thread.join()
        return {
            "success": True,
            "dados_kB": round(resultado['bytes_recebidos'] / 1024, 2),
            "tempo_s": resultado['tempo_s'],
            "throughput_kbps": resultado['throughput_kbps']
        }
    except Exception as e:
        return {"success": False, "error": str(e)}