from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
import os
import base64

def generate_salt():
    return os.urandom(16)


def encrypt(data, passcode, salt):

    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2 ** 14,
        r=8,
        p=1,
        backend=default_backend()
    )
    key = kdf.derive(passcode.encode())


    iv = os.urandom(16)


    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    encryptor = cipher.encryptor()
    encrypted_data = encryptor.update(data.encode()) + encryptor.finalize()

    return base64.b64encode(encrypted_data).decode('utf-8'), base64.b64encode(iv).decode('utf-8')


def decrypt(encrypted_data, salt, iv, passcode):
    encrypted_data = base64.b64decode(encrypted_data)
    salt = base64.b64decode(salt)
    iv = base64.b64decode(iv)


    kdf = Scrypt(
        salt=salt,
        length=32,
        n=2**14,
        r=8,
        p=1,
        backend=default_backend()
    )
    key = kdf.derive(passcode.encode())


    cipher = Cipher(algorithms.AES(key), modes.CFB(iv), backend=default_backend())
    decryptor = cipher.decryptor()
    decrypted_data = decryptor.update(encrypted_data) + decryptor.finalize()

    return decrypted_data.decode('utf-8')
