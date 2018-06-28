from crypto import Encript
import zipfile
import os

def menu():
    print("Digite a mensagem que deseja enviar")
    msg = raw_input()
    file = open('./texto.txt', 'w')
    file.write(msg)
    file.close()

    print("Coloque os anexos na pasta 'anexos', digite 1 para continuar:")
    raw_input()
    jungle_zip = zipfile.ZipFile('./msg.zip', 'w')
    jungle_zip.write('./texto.txt', compress_type=zipfile.ZIP_DEFLATED)

    caminhos = [os.path.join('./anexos', nome) for nome in os.listdir('./anexos')]
    arquivos = [arq for arq in caminhos if os.path.isfile(arq)]
    anexos = [arq for arq in arquivos if arq.lower()]

    for file in anexos:
        jungle_zip.write(file, compress_type=zipfile.ZIP_DEFLATED)

    jungle_zip.close()
    enc = Encript()
    key = enc.encrypt_file('./msg.zip')


if __name__ == "__main__":
    menu()