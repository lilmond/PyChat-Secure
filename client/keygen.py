from Crypto.PublicKey import RSA
import sys
import os

output_name = input("Filename: ")
private_key_path = f"./files/{output_name}"

if os.path.exists(private_key_path):
    print("error: key file already exists")
    sys.exit()

key = RSA.generate(2048)
private_key = key.export_key().decode()

with open(private_key_path, "w") as file:
    file.write(private_key)
    file.close()

print("key file successfully created")
