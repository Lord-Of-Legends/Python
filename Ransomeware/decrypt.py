import threading
from cryptography.fernet import Fernet
import os

def load_key():
    with open('key.txt', 'rb') as key_file:
        return key_file.read()

def decrypt_file(file_path, key):
    cipher_suite = Fernet(key)
    with open(file_path, 'rb') as encrypted_file:
        decrypted_data = cipher_suite.decrypt(encrypted_file.read())
    with open(file_path[:-4], 'wb') as decrypted_file:
        decrypted_file.write(decrypted_data)
    os.remove(file_path)

def decrypt_directory(directory_path, key):
    for root, dirs, files in os.walk(directory_path):
        for file in files:
            if file.endswith('.enc') and file not in ['encrypt.py', 'decrypt.py', 'key.txt', 'encrypt.exe', 'decrypt.exe']:
                file_path = os.path.join(root, file)
                decrypt_file(file_path, key)

def decrypt_folder(folder_path, key):
    decrypt_directory(folder_path, key)

def main():
    if not os.path.exists('key.txt'):
        print("Error: key.txt file not found. Make sure you have generated a key using the encryption script.")
        return

    key = load_key()

    passphrase = input("Enter the decryption passphrase: ")

    if passphrase == "python":
        folders_to_decrypt = ['Downloads', 'Documents', 'Pictures', 'Videos']

        threads = []

        for folder in folders_to_decrypt:
            folder_path = os.path.expanduser(f'~/{folder}')
            if os.path.exists(folder_path):
                thread = threading.Thread(target=decrypt_folder, args=(folder_path, key))
                threads.append(thread)
                thread.start()

        for thread in threads:
            thread.join()

        print("Files decrypted and deleted.")
    else:
        print("Invalid passphrase. Decryption failed.")

if __name__ == '__main__':
    main()
