from src.crypto import Encript
import zipfile
import os
from hashlib import md5
import glob

def send_menu():
    print("Digite a mensagem que deseja enviar")
    msg = raw_input()

    print("Coloque os anexos na pasta 'anexos', digite 1 para continuar:")
    raw_input()
    with zipfile.ZipFile('./msg.zip', 'w') as jungle_zip:
        jungle_zip.writestr('message.txt', bytes(msg), compress_type=zipfile.ZIP_DEFLATED)


        caminhos = glob.glob('./anexos/*')
        anexos = [arq for arq in caminhos if os.path.isfile(arq)]

        for file in anexos:
            jungle_zip.write(file, compress_type=zipfile.ZIP_DEFLATED)

    enc = Encript()
    key = enc.encrypt_file('./msg.zip')


if __name__ == "__main__":
    send_menu()