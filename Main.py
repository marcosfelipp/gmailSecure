# -*- coding:utf-8 -*-
from getpass import getpass
from src.User import User
from src import send_email
import os
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
    os.mkdir(userfolder)
    os.mkdir(userfolder + '/' + 'sent')
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

    print()
    print('1 - Criar E-Mail')
    print('2 - Ler E-Mail')
    opc = raw_input('O que deseja fazer? ')

    if opc == 1:
        send_email.send_menu()






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

