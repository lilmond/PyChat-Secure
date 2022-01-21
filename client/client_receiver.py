from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
from denc import Denc
import socket
import json

class config:
    server_host = "127.0.0.1"
    server_port = 4444

    privkey_path = "./files/privkey"

def main():
    denc = Denc(config.privkey_path)
    denc.load_key()

    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.connect((config.server_host, config.server_port))
    except Exception:
        print("error: server is offline")
        return

    try:
        while True:
            full_data = b""
            while True:
                chunk = sock.recv(1024)
                if len(chunk) == 0:
                    print("error: connection has disconnected")
                    return
                full_data += chunk
                if full_data.decode(errors="ignore").endswith("|||||"):
                    break

            data = full_data[:len(full_data)-5]
            data_decrypt = denc.decrypt(data)

            if data_decrypt == None:
                print("<distorted>")
                continue

            data_json = json.loads(data_decrypt)

            username = data_json["username"]
            message = data_json["message"]

            print(f"{username}> {message}")
    except ConnectionResetError:
        print("error: connection has been closed")
        return
    except Exception as e:
        print(f"error: {e}")
        return

if __name__ == "__main__":
    main()
