# FT_OTP 🚀🔐

FT_OTP is a simple One-Time Password (OTP) generator written in Python that uses a secure hashing algorithm to create time-based OTPs. Great for implementing an additional layer of security in your projects! 😎

## 📂 Files

- `ft_otp.py`: Main script containing the OTP generator and key management functions.
- `keygen.py`: Helper script to generate a random 64-character hex key based on an input text.
- `requirements.txt`: List of required Python packages.

## 📦 Installation

1. Clone the repository:

```bash
git clone https://github.com/username/ft_otp.git
```

2. Install required packages:

```bash
pip install -r requirements.txt
```

## 🎯 Usage

### Generate a hex key

1. Edit the `input_text` variable in the `keygen.py` script with your desired input text.
2. Run the script:

```bash
python keygen.py
```

This will generate a `key.hex` file with the hex key.

### Create a ft_otp key file

Generate a `ft_otp.key` file from the hex key file:

```bash
python ft_otp.py --generate key.hex
```

### Generate an OTP

Generate an OTP using the `ft_otp.key` file:

```bash
python ft_otp.py --key ft_otp.key
```
