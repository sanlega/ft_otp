import sys
import time
import hashlib
import argparse
import hmac
import base64
import struct
import binascii
import string   

def generate_key(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            key = f.read().strip()
    except FileNotFoundError:
        # print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        # print(f"Error: Could not read file '{input_file}': {str(e)}")
        sys.exit(1)

    if len(key) < 64:
        # print("./ft_otp: error: key must be at least 64 hexadecimal characters.")
        sys.exit(1)

    # Define a message to use in HMAC function
    message = 'your_message'.encode('utf-8')

    # Convert the hex key to bytes
    key_bytes = binascii.unhexlify(key)

    # Create a new hmac object using key_bytes and message
    hmac_object = hmac.new(key_bytes, message, digestmod=hashlib.sha1)

    # Get the hmac digest as a hexadecimal string
    hmac_hexdigest = hmac_object.hexdigest()

    # print(f"HMAC-SHA1 Digest: {hmac_hexdigest}")

    # You may want to write the hmac digest to the output file
    try:
        with open(output_file, 'w') as f:
            f.write(hmac_hexdigest)
    except Exception as e:
        # print(f"Error: Could not write to file '{output_file}': {str(e)}")
        sys.exit(1)

def is_base32(s):
    return all(c in string.ascii_uppercase + '234567' for c in s.upper())

def get_otp(key, time_interval=30):
    current_time = int(time.time() // time_interval)
    # Convert the HMAC-SHA1 key from hexadecimal to bytes
    key_bytes = binascii.unhexlify(key)
    msg = current_time.to_bytes(8, byteorder='big')
    hmac_sha1 = hmac.new(key_bytes, msg, hashlib.sha1)
    hex_value = hmac_sha1.hexdigest()
    six_digit_number = int(hex_value, 16) % 1000000
    return six_digit_number

# def print_colored(text, color):
#     color_codes = {
#         'black': '30',
#         'red': '31',
#         'green': '32', 'yellow': '33',
#         'blue': '34',
#         'magenta': '35',
#         'cyan': '36',
#         'white': '37',
#         'reset': '0'
#     }
#
#     return f"\033[{color_codes[color]}m{text}\033[0m"

def main():
    parser = argparse.ArgumentParser(description="Generate a one-time password.")
    parser.add_argument('-g', '--generate', metavar='INPUT_FILE', type=str, help='Generate a key from a hex file and save it in ft_otp.key.')
    parser.add_argument('-k', '--key', metavar='KEY_FILE', type=str, help='Use a specific key file to generate OTP.')

    args = parser.parse_args()

    if args.generate:
        generate_key(args.generate, 'ft_otp.key')
        sys.exit(0)

    if args.key:
        try:
            with open(args.key, 'r') as f:
                content = f.read().strip()
                key = content
                # key = content[:-32]
                # checksum = content[-32:]
        except FileNotFoundError:
            # print(f"Error: File '{args.key}' not found.")
            sys.exit(1)
        except Exception as e:
            # print(f"Error: Could not read file '{args.key}': {str(e)}")
            sys.exit(1)

        # if not verify_checksum(key, checksum):
        #     print("Error: The key file is corrupted or has been modified.")
        #     sys.exit(1)

        otp = get_otp(key)
        # print(f"{print_colored('Your one time password:', 'red')} {print_colored(otp, 'cyan')}")
        print(otp)
        sys.exit(0)

    parser.print_help()
    sys.exit(1)

if __name__ == "__main__":
    main()
