import sys
import time
import hashlib
import argparse
import hmac
import math
import base64
import struct
import binascii

def generate_key(input_file, output_file):
    try:
        with open(input_file, 'r') as f:
            key = f.read().strip()
    except FileNotFoundError:
        print(f"Error: File '{input_file}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error: Could not read file '{input_file}': {str(e)}")
        sys.exit(1)

    if len(key) < 64:
        print("./ft_otp: error: key must be at least 64 hexadecimal characters.")
        sys.exit(1)

    encrypted_key = hashlib.sha256(key.encode('utf-8')).hexdigest()
    print(f"Key: {encrypted_key}")
    # checksum = hashlib.md5(encrypted_key.encode('utf-8')).hexdigest()
    # print(f"checksum: {checksum}")

    try:
        with open(output_file, 'w') as f:
            # f.write(encrypted_key + checksum)
            f.write(encrypted_key)
        print(f"Key was successfully saved in {output_file}.")
    except Exception as e:
        print(f"Error: Could not write to file '{output_file}': {str(e)}")
        sys.exit(1)


def get_otp(key):
    current_time = time.time()
    time_step = 30
    time_factor = math.floor(current_time / time_step)

    key_bytes = binascii.unhexlify(key)  # Use unhexlify to decode the key
    time_bytes = struct.pack(">Q", time_factor)
    sig = hmac.new(key_bytes, time_bytes, hashlib.sha1).digest()

    offset = sig[19] & 0xf
    extracted_bytes = sig[offset:offset+4]

    int_digits = struct.unpack(">I", extracted_bytes)
    int_code = int_digits[0] & 0x7fffffff

    modded_code = int_code % 1000000

    return "%06d" % modded_code

def print_colored(text, color):
    color_codes = {
        'black': '30',
        'red': '31',
        'green': '32',
        'yellow': '33',
        'blue': '34',
        'magenta': '35',
        'cyan': '36',
        'white': '37',
        'reset': '0'
    }

    return f"\033[{color_codes[color]}m{text}\033[0m"

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
            print(f"Error: File '{args.key}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: Could not read file '{args.key}': {str(e)}")
            sys.exit(1)

        # if not verify_checksum(key, checksum):
        #     print("Error: The key file is corrupted or has been modified.")
        #     sys.exit(1)

        otp = get_otp(key)
        print(f"{print_colored('Your one time password:', 'red')} {print_colored(otp, 'cyan')}")
        sys.exit(0)

    parser.print_help()
    sys.exit(1)

if __name__ == "__main__":
    main()
