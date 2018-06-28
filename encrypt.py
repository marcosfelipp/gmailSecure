'''import hashlib
from Crypto.PublicKey import RSA
from Crypto.Util.randpool import RandomPool
import os, random, struct
from Crypto.Cipher import AES


class EncrryptFile():
	def __init__(self):
		pass

    def encrypt_file(key, in_filename, out_filename=None, chunksize=64 * 1024):
    """ Encrypts a file using AES (CBC mode) with the
        given key.

        key:
            The encryption key - a string that must be
            either 16, 24 or 32 bytes long. Longer keys
            are more secure.

        in_filename:
            Name of the input file

        out_filename:
            If None, '<in_filename>.enc' will be used.

        chunksize:
            Sets the size of the chunk which the function
            uses to read and encrypt the file. Larger chunk
            sizes can be faster for some files and machines.
            chunksize must be divisible by 16.
    """
    if not out_filename:
        out_filename = in_filename + '.enc'

    iv = ''.join(chr(random.randint(0, 0xFF)) for i in range(16))
    encryptor = AES.new(key, AES.MODE_CBC, iv)
    filesize = os.path.getsize(in_filename)

    with open(in_filename, 'rb') as infile:
        with open(out_filename, 'wb') as outfile:
            outfile.write(struct.pack('<Q', filesize))
            outfile.write(iv)

            while True:
                chunk = infile.read(chunksize)
                if len(chunk) == 0:
                    break
                elif len(chunk) % 16 != 0:
                    chunk += ' ' * (16 - len(chunk) % 16)

                outfile.write(encryptor.encrypt(chunk))


class EncryptEmail:
    def __init__(self):
        self.session_key, self.session_public_key = self.generate_key()
        self.server_public_key = None

    def generate_key(self):
        '''
        Generate public and private session_key
        '''
        pool = RandomPool(384)
        pool.stir()
        randfunc = pool.get_bytes
        key_size = 1024
        key = RSA.generate(key_size, randfunc)
        public_key = key.publickey()
        return key, public_key

    def get_public_key(self):
        '''
		Return public session_key
		'''
        return self.session_key.publickey().exportKey(format='PEM', passphrase=None, pkcs=1)

    def set_server_public_key(self, server_public_key):
        '''
        Store public session_key received from server
        :param server_public_key: session_key
        '''
        self.server_public_key = RSA.importKey(server_public_key, passphrase=None)

    def hash_md5(self, message):
        '''
        Apply hash in msg
        :param message: mesage to hash
        '''
        return hashlib.sha256(message.encode('utf-8'))

    def check_msg_received(self, ):
        '''
        Use hash to checking msg received integrity
        :return:
        '''
        pass

    def encrypt_msg(self, message, user_public_key):
        '''
		Encrypt messages using session_key of server
		:param message: Message to cryptography
		:return: Message encrypted
		'''

        # encrypted_msg = self.server_public_key.encrypt(message, '')
        encrypted_msg = self.session_public_key.encrypt(message, '')
        encrypted_session_key = user_public_key.encrypt(encrypted_msg, '')

        return encrypted_msg, encrypted_session_key

    def decrypt_msg(self, message):
        '''
        Encrypt messages using RSA
        :param message: Message to cryptography
        :return: Message encrypted
        '''
        msg_decrypted = self.session_key.decrypt(message)

        return msg_decrypted


# Testes:

if __name__ == '__main__':
    e = EncryptEmail()

    # ----------Client -----------------
    key_pv_client, key_pub_client = e.generate_key()
    client_key = key_pv_client.publickey().exportKey(format='PEM', passphrase=None, pkcs=1)

    # ----------server -----------------
    key_pv_server, key_pub_server = e.generate_key()
    server_key = key_pv_server.publickey().exportKey(format='PEM', passphrase=None, pkcs=1)

    key_rcv_server = RSA.importKey(server_key, passphrase=None)

    key_rcv_client = RSA.importKey(client_key, passphrase=None)

    # server encrypt msg with session_key of client
    msg = key_rcv_client.encrypt("Hello", '')

    # Client decrypt msg with private session_key
    msg = key_pv_client.decrypt(msg)
    print(msg)
'''