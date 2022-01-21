import threading
import socket

class config:
    listen_host = "0.0.0.0"
    listen_port = 4444

class clients:
    sockets = []

def client_handle(client):
    clients.sockets.append(client)
    try:
        while True:
            full_data = b""
            while True:
                chunk = client.recv(1024)
                if len(chunk) == 0: return
                full_data += chunk
                if full_data.decode(errors="ignore").endswith("|||||"):
                    break
            broadcast(full_data, client)
    except Exception:
        return
    finally:
        clients.sockets.remove(client)

def broadcast(data, sender):
    current_clients = clients.sockets.copy()
    for client in current_clients:
        try:
            if client == sender: continue
            client.send(data)
        except Exception:
            continue

def main():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        sock.bind((config.listen_host, config.listen_port))
        sock.listen()
        print(f"[SERVER] Listening on {config.listen_host}:{config.listen_port}")

        while True:
            client, address = sock.accept()
            threading.Thread(target=client_handle, args=[client], daemon=True).start()
    except KeyboardInterrupt:
        return

if __name__ == "__main__":
    main()
