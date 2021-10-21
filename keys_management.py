from os import write
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_keys(private_key_fn = "private_key.pem"):
    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=1024,
        backend=default_backend()
    )
    write_key(private_key, private_key_fn)

def write_key(key, filename, private = True):
    if private:
        pem = key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
    else:
        pem = key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )

    with open(filename, 'wb') as f:
        f.write(pem)

def read_key(file, private = True):
    if private:
        with open(file, "rb") as key_file:
            key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
    else:
        with open(file, "rb") as key_file:
            key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
    return key
