# -*- coding:utf-8 -*-
from getpass import getpass
from src.User import User
from src.crypto import Encript
from src import send_email
from Crypto.PublicKey import RSA
import os
import glob
import pickle

def read_register():
    try:
        data_users_file = open('publickey_data_users.pkl', 'rb')
        pl = pickle.load(data_users_file)
        public_users_dict = pl if type(pl) == dict else {}
        data_users_file.close()
    except IOError:
        public_users_dict = {}
    except EOFError:
        public_users_dict = {}

    try:
        data_users_file = open('privatekey_data_users.pkl', 'rb')
        pl = pickle.load(data_users_file)
        private_users_dict = pl if type(pl) == dict else {}
        data_users_file.close()
    except IOError:
        private_users_dict = {}
    except EOFError:
        private_users_dict = {}

    return public_users_dict, private_users_dict

def write_register(user):
    public_users_dict, private_users_dict = read_register()

    public_users_dict[user.username] = user.get_public_key()
    data_users_file = open('publickey_data_users.pkl', 'wb')
    pickle.dump(public_users_dict, data_users_file)
    data_users_file.close()

    private_users_dict[user.username] = user.get_private_key()
    data_users_file = open('privatekey_data_users.pkl', 'wb')
    pickle.dump(private_users_dict, data_users_file)
    data_users_file.close()

def register():
    print('\n-- Cadastrando novo Usuário --')
    user_name = raw_input('Usuário: ')
    passwd = getpass('Senha: ')
    user = User(user_name, passwd)
    write_register(user)

    userfolder = 'users_folders/'+user.username
    if not os.path.isdir(userfolder):
        os.mkdir(userfolder)
    if not os.path.isdir(userfolder + '/' + 'sent'):
        os.mkdir(userfolder + '/' + 'sent')
    if not os.path.isdir(userfolder + '/' + 'received'):
        os.mkdir(userfolder + '/' + 'received')


def menu():
    print('********************')
    print('* 1 - Se Cadastrar *')
    print('* 2 - Fazer Login  *')
    print('* X - Sair         *')
    print('********************')
    opc = raw_input('O que deseja fazer? ')
    return opc.lower() if opc in ('1', '2', 'X', 'x') else menu()

def login():
    while True:
        print('\n-- Login --')
        user_name = raw_input('Usuário: ')
        passwd = getpass('Senha: ')
        user = User(user_name, passwd)
        publics, privates = read_register()
        if publics.get(user.username, "User not registered") == "User not registered":
            print('Senha ou usuário incorretos!!!')
            opc = raw_input('Gostaria de se cadastrar? [S-sim / N-não] ')
            if opc in ('s', 'S', 'Sim', 'SIm', 'SIM'):
                register()
            else:
                return
        else:
            break

    print('\n')
    print('1 - Criar E-Mail')
    print('2 - Ler E-Mail')
    opc = raw_input('O que deseja fazer? ')

    if opc == '1':
        while True:
            dest = raw_input("Destinatário: ")
            if dest not in read_register()[0]:
                print('Destinatário não registrado. Tente novamente...')
            else:
                break

        private_key_arq_send = send_email.send_menu(user, dest)
        with open('users_folders/'+dest+'/received/key.arq', 'w') as f:
            public_key_dest = read_register()[0][dest]
            K = RSA.importKey(public_key_dest)
            enc = K.encrypt(private_key_arq_send, 0)
            f.write(enc[0])

        with open('users_folders/'+dest+'/received/sender.publickey', 'w') as f:
            f.write(user.get_public_key())

    if opc == '2':

        if len(glob.glob('users_folders/'+user.username+'/received/*')) == 0:
            print('Nenhuma mensagem para ler...')
        else:
            with open('users_folders/'+user.username+'/received/sender.publickey') as sp:
                sender_publickkey = sp.read()

            K_sender = RSA.importKey(sender_publickkey)

            with open('users_folders/'+user.username+'/received/hash.arq') as h:
                hash_message = K_sender.decrypt(h.read())

            K_user = RSA.importKey(user.get_private_key())
            with open('users_folders/'+user.username+'/received/key.arq') as k:
                key_message = K_user.decrypt(k.read())

            ENC = Encript()
            message = ENC.decrypt_file(None, key_message, 'users_folders/'+user.username+'/received/msg.arq', 'users_folders/'+user.username+'/received/msg.zip')

            print('Hash da menssagem recebida: %s' % hash_message)
            print('O arquivo com a mensagem foi salvo na SUA pasta received!!!')



controll = {
    'x': exit,
    '1': register,
    '2': login,
}


if __name__=='__main__':
    if not os.path.isdir('users_folders'):
        os.mkdir('users_folders')
    while True:
        opc = menu()
        controll[opc]()

