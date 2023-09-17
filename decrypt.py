from cryptography.hazmat.primitives.asymmetric import ec
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.fernet import Fernet

def initialize_private_key():
    # Load your private key from 'private_key.pem'
    with open('private_key.pem', 'rb') as private_key_file:
        private_key_pem = private_key_file.read()
        private_key = serialization.load_pem_private_key(
            private_key_pem,
            password=None,  # You may need to provide a password if your key is encrypted
            backend=default_backend()
        )
    return private_key

def decrypt_data(encrypted_key_file, role, private_key):
    # Read the ECC-encrypted key
    encrypted_key = encrypted_key_file.read()

    # Decrypt the ECC-encrypted key using ECC private key
    symmetric_key = private_key.decrypt(
        encrypted_key,
        ec.ECIES()
    )

    # Initialize Fernet cipher with the decrypted symmetric key
    cipher = Fernet(symmetric_key)

    # Read and decrypt the symmetrically encrypted data
    encrypted_data = encrypted_data_file.read()
    decrypted_data = cipher.decrypt(encrypted_data)

    
    if role == 'Admin':
        private_key = initialize_private_key()

        with open('EncriptedKey', 'rb') as encrypted_key_file:
            encrypted_data_file = encrypted_data_file.read()
        decrypted_data = cipher.decrypt(encrypted_data_file)
        data = decrypted_data.decode('utf-8')
        
    elif role=="User":
        with open('EncriptedFile', 'rb') as encrypted_data_file:
                encrypted_data_file = encrypted_data_file.read()
        decrypted_data = cipher.decrypt(encrypted_data_file)
        data = decrypted_data.decode('utf-8')

        decrypted_message = decrypt_data(encrypted_key_file, encrypted_data_file, private_key)

        print(decrypted_message)

    return decrypted_data.decode('utf-8')

    

    