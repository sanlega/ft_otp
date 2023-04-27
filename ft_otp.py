# **************************************************************************** #
#                                                                              #
#                                                         :::      ::::::::    #
#    ft_otp.py                                          :+:      :+:    :+:    #
#                                                     +:+ +:+         +:+      #
#    By: slegaris <slegaris@student.42madrid.com>   +#+  +:+       +#+         #
#                                                 +#+#+#+#+#+   +#+            #
#    Created: 2023/04/26 01:11:18 by slegaris          #+#    #+#              #
#    Updated: 2023/04/26 16:04:32 by slegaris         ###   ########.fr        #
#                                                                              #
# **************************************************************************** #

import sys
import time
import hashlib
import argparse

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
    # print(f"Key: {encrypted_key}")
    checksum = hashlib.md5(encrypted_key.encode('utf-8')).hexdigest()
    # print(f"checksum: {checksum}")

    try:
        with open(output_file, 'w') as f:
            f.write(encrypted_key + checksum)
        print(f"Key was successfully saved in {output_file}.")
    except Exception as e:
        print(f"Error: Could not write to file '{output_file}': {str(e)}")
        sys.exit(1)

def verify_checksum(key, checksum):
    calculated_checksum = hashlib.md5(key.encode('utf-8')).hexdigest()
    # print(f"calculated_checksum: {calculated_checksum}")
    return calculated_checksum == checksum

def get_otp(key, time_interval=30):
    current_time = int(time.time() // time_interval)
    # print(f"Time: {current_time}")
    hasher = hashlib.sha256()
    # print(f"hasher: {hasher}")
    hasher.update(str(current_time).encode('utf-8'))
    hex_value = hasher.hexdigest()[:6]
    # print(f"hashed output: {hex_value}")
    six_digit_number = int(hex_value, 16) % 1000000
    return six_digit_number

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
                key = content[:-32]
                checksum = content[-32:]
        except FileNotFoundError:
            print(f"Error: File '{args.key}' not found.")
            sys.exit(1)
        except Exception as e:
            print(f"Error: Could not read file '{args.key}': {str(e)}")
            sys.exit(1)

        if not verify_checksum(key, checksum):
            print("Error: The key file is corrupted or has been modified.")
            sys.exit(1)

        otp = get_otp(key)
        print(f"{print_colored('Your one time password:', 'red')} {print_colored(otp, 'cyan')}")
        sys.exit(0)

    parser.print_help()
    sys.exit(1)

if __name__ == "__main__":
    main()
