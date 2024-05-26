import base64
import unittest
from encryption import generate_salt, encrypt, decrypt


class TestEncryption(unittest.TestCase):

    def test_generate_salt(self):
        salt = generate_salt()
        self.assertEqual(len(salt), 16)  # Ensure the salt length is 16 bytes

    def test_encrypt_decrypt(self):
        data = "mysecretpassword"
        passcode = "mypassword"
        salt = generate_salt()

        encrypted_data, iv = encrypt(data, passcode, salt)
        decrypted_data = decrypt(encrypted_data, base64.b64encode(salt).decode('utf-8'), iv, passcode)

        self.assertEqual(data, decrypted_data)

    def test_decrypt_with_wrong_passcode(self):
        data = "mysecretpassword"
        passcode = "mypassword"
        wrong_passcode = "wrongpassword"
        salt = generate_salt()

        encrypted_data, iv = encrypt(data, passcode, salt)
        with self.assertRaises(Exception):
            decrypt(encrypted_data, base64.b64encode(salt).decode('utf-8'), iv, wrong_passcode)


if __name__ == '__main__':
    unittest.main()
