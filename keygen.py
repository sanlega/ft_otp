import secrets
import binascii

def generate_hex_key(text, file_name):
    key = binascii.hexlify(text.encode('utf-8')).decode('utf-8')
    while len(key) < 64:
        key += secrets.token_hex(32)
    key = key[:64]

    with open(file_name, 'w') as f:
        f.write(key)

    print(f"Key saved to {file_name}")

input_text = "Your input text here"
generate_hex_key(input_text, 'key.hex')
