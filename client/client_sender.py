from denc import Denc
import socket
import json

class config:
    server_host = "127.0.0.1"
    server_port = 4444

    privkey = "./files/privkey"
    username = "anonymous"

def main():
    denc = Denc(config.privkey)
    denc.load_key()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((config.server_host, config.server_port))
    except Exception:
        print("error: server is offline")
        return

    try:
        while True:
            message = input(">")
            data = {"username": config.username, "message": message}
            data = json.dumps(data)
            data = denc.encrypt(data)
            data += b"|||||"
            sock.send(data)
    except KeyboardInterrupt:
        return
    except ConnectionResetError:
        print("error: connection has been closed")
        return
    except Exception as e:
        print(f"error: {e}")
        return

if __name__ == "__main__":
    main()
