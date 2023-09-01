import zlib
import base64
from Cryptodome.Cipher import AES, PKCS1_OAEP
from Cryptodome.PublicKey import RSA
from Cryptodome.Random import get_random_bytes
from io import BytesIO


def generate_keys():
    key = RSA.generate(2048)
    private_key = key.exportKey()
    public_key = key.public_key().exportKey()

    with open('key.pri', 'wb') as key_file:
        key_file.write(private_key)

    with open('key.pub', 'wb') as key_file:
        key_file.write(public_key)


def get_rsa_cipher(key_type):
    with open(f'key.{key_type}') as key_file:
        key = key_file.read()

    rsa_key = RSA.importKey(key)

    return PKCS1_OAEP.new(rsa_key), rsa_key.size_in_bytes()


def encrypt(plain_text):
    compressed_text = zlib.compress(plain_text)

    session_key = get_random_bytes(16)
    cipher_aes = AES.new(session_key, AES.MODE_EAX)

    cipher_text, tag = cipher_aes.encrypt_and_digest(compressed_text)
    cipher_rsa, _ = get_rsa_cipher('pub')

    encrypted_session_key = cipher_rsa.encrypt(session_key)

    payload = encrypted_session_key + cipher_aes.nonce + tag + cipher_text
    encrypted = base64.encodebytes(payload)

    return encrypted


def decrypt(encrypted):
    encrypted_bytes = BytesIO(base64.decodebytes(encrypted))
    cipher_rsa, keysize_in_bytes = get_rsa_cipher('pri')

    encrypted_session_key = encrypted_bytes.read(keysize_in_bytes)
    nonce = encrypted_bytes.read(16)
    tag = encrypted_bytes.read(16)
    cipher_text = encrypted_bytes.read()

    session_key = cipher_rsa.decrypt(encrypted_session_key)
    cipher_aes = AES.new(session_key, AES.MODE_EAX, nonce)
    decrypted = cipher_aes.decrypt_and_verify(cipher_text, tag)

    plain_text = zlib.decompress(decrypted)

    return plain_text
