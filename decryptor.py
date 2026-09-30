import os
from cryptography.fernet import Fernet

TARGET_DIR = "./test_files"
KEY_FILE = "secret.key"

# Load encryption key
try:
    with open(KEY_FILE, "rb") as key_file:
        key = key_file.read()
except FileNotFoundError:
    print("[!] ERROR: Key file", KEY_FILE, "not found!")
    exit()

cipher = Fernet(key)

# Decrypt files
for root, dirs, files in os.walk(TARGET_DIR):
    for file in files:
        file_path = os.path.join(root, file)
        
        # Skip ransom note
        if file == "RANSOM_NOTE.txt":
            continue
        
        # Read encrypted data
        with open(file_path, "rb") as f:
            encrypted_data = f.read()
        
        # Decrypt and restore
        try:
            decrypted_data = cipher.decrypt(encrypted_data)
            with open(file_path, "wb") as f:
                f.write(decrypted_data)
        except:
            print("[!] Failed to decrypt:", file_path)

# Delete ransom note
ransom_note_path = os.path.join(TARGET_DIR, "RANSOM_NOTE.txt")
if os.path.exists(ransom_note_path):
    os.remove(ransom_note_path)

print("[+] Decryption complete. Ransom note deleted.")
