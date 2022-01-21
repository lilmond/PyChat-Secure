from Crypto.Cipher import PKCS1_OAEP
from Crypto.PublicKey import RSA
import os

class Denc(object):
    def __init__(self, privkey_path):
        self.privkey_path = privkey_path
        self.privkey2 = None

    def load_key(self):
        if not os.path.exists(self.privkey_path):
            raise Exception(f"error: file {self.privkey_path} does not exist")

        with open(self.privkey_path) as file:
            privkey_string = file.read()
            file.close()

        privkey = RSA.import_key(privkey_string)
        privkey2 = PKCS1_OAEP.new(privkey)

        self.privkey2 = privkey2

    def encrypt(self, data):
        if not self.privkey2:
            raise Exception("error: key has not been loaded")

        return self.privkey2.encrypt(data.encode())

    def decrypt(self, data):
        if not self.privkey2:
            raise Exception("error: key has not been loaded")

        try:
            return self.privkey2.decrypt(data)
        except Exception:
            return
