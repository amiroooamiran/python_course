from cryptography.fernet import Fernet

def generate_key():
    return Fernet.generate_key()

def encrypt_message(message, key):
    cipher_suite = Fernet(key)
    encrypted_message = cipher_suite.encrypt(message.encode())
    return encrypted_message

def decrypt_message(enctypted_message, key):
    cipher_suite = Fernet(key)
    decrypted_message = cipher_suite.decrypt(enctypted_message).decode()
    return decrypted_message

if __name__ == "__main__":
    key = generate_key()
    print("Generate Key: ", key)

    message = "Hello, amirooo"

    encrypted_message = encrypt_message(message, key)
    print("Encrypted Message: ", encrypted_message)

    decrypted_message = decrypt_message(encrypted_message, key)
    print("Encrypt Message: ", decrypted_message)

