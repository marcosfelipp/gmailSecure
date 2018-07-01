#! -*- coding:utf-8 -*-
from src.crypto import Encript
import zipfile
import os
from hashlib import md5
import glob
from Crypto.PublicKey import RSA

def send_menu(user, dest):
    print("Digite a mensagem que deseja enviar")
    msg = raw_input()

    print("Coloque os anexos na pasta 'anexos', digite 1 para continuar:")
    raw_input()
    with zipfile.ZipFile('./msg.arq.zip', 'w') as jungle_zip:
        jungle_zip.writestr('message.txt', bytes(msg), compress_type=zipfile.ZIP_DEFLATED)


        caminhos = glob.glob('./anexos/*')
        anexos = [arq for arq in caminhos if os.path.isfile(arq)]

        for file in anexos:
            jungle_zip.write(file, compress_type=zipfile.ZIP_DEFLATED)

    ## essa parte deve ir para outro arquivo
    with open('./msg.arq.zip', 'r') as f:
        hashfile = md5(f.read()).hexdigest()

    with open('users_folders/'+dest+'/received'+'/hash.arq', 'w') as f:
        # salvando o hash criptografado com a chave privada do usuário corrent
        K = RSA.importKey(user.get_private_key())
        hashcript = K.encrypt(hashfile, 0)
        f.write(hashfile)


    enc = Encript()
    key = enc.encrypt_file(in_filename='./msg.arq.zip', out_filename='users_folders/'+dest+'/received'+'/msg.arq')
    return key


if __name__ == "__main__":
    send_menu()