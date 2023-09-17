from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.fernet import Fernet

def KeyGeneration():
    # Create Symmetric key
    key = Fernet.generate_key()

    # Write the symmetric key
    with open('message.key', 'wb') as k:
        k.write(key)

    # Generate an ECC key pair
    private_key = ec.generate_private_key(ec.SECP256R1())  # You can choose other curves as well

    # Serialize and write the public key
    public_key = private_key.public_key()
    public_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open('public_key.key', 'wb') as public_key_file:
        public_key_file.write(public_pem)

    # Serialize and write the private key
    private_pem = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )

    with open('private_key.key', 'wb') as private_key_file:
        private_key_file.write(private_pem)

KeyGeneration()
