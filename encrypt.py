import os
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes

# Function to generate ECC key pair
def generate_ecc_key_pair():
    # Generate an ECC key pair
    private_key = ec.generate_private_key(ec.SECP256R1(), default_backend())
    public_key = private_key.public_key()

    # Serialize and save the public key
    public_key_pem = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )

    with open('public_key.pem', 'wb') as public_key_file:
        public_key_file.write(public_key_pem)

    return private_key

# Function to encrypt data with ECC public key
def encrypt_data(data, public_key):
    # Encrypt the data using ECC public key
    ciphertext = public_key.encrypt(
        data.encode('utf-8'),
        ec.ECIES(hashes.SHA512())
    )

    return ciphertext

# Function to symmetrically encrypt data
def symmetric_encrypt(data, key):
    # Encrypt the data symmetrically using Fernet
    fernet = Fernet(key)
    encrypted_data = fernet.encrypt(data.encode('utf-8'))
    return encrypted_data

def Encryption(message, role):
    # Generate ECC key pair
    private_key_ecc = generate_ecc_key_pair()  # Use a different variable name

    # Encrypt the message symmetrically (Fernet)
    symmetric_key = Fernet.generate_key()
    encrypted_message = symmetric_encrypt(message, symmetric_key)

    # Encrypt the symmetric key asymmetrically (ECC)
    ecc_encrypted_key = encrypt_data(symmetric_key.decode('utf-8'), private_key_ecc)

    # Store 'encrypted_message', 'ecc_encrypted_key', and 'role' as needed
    # You can save these to files or store them in a database, for example.

    if role == "Admin":
        # Get the message and role from the user (or another source)
        with open('EncryptedFileAdmin', 'wb') as encrypted_file:
            encrypted_file.write(encrypted_message)
    elif role == "User":
        with open("EncryptedFileUser", 'wb') as encrypted_file:
            encrypted_file.write(encrypted_message)

message = "hllo"
role = "Admin"
Encryption(message, role)
