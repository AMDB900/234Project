"""
References:
https://www.geeksforgeeks.org/python-strings-encode-method/
https://www.geeksforgeeks.org/hashlib-module-in-python/
"""

import hashlib

def read_pi_digits(file_path):
    with open(file_path, 'r') as f:
        pi_digits = f.read()  # Read all digits as a string
    return pi_digits.replace(".", "").strip()  # Remove the decimal point and any whitespace

def hash_key(key):
    # Use SHA-256 hash function to generate a digest of the key
    key_bytes = key.encode('utf-8') if isinstance(key, str) else key
    hash_digest = hashlib.sha256(key_bytes).hexdigest()  # Get the hex digest
    return int(hash_digest, 16)  # Convert hex digest to an integer

def pad_key_with_pi(key, pi_digits, target_length=1024):
    # Ensure the key is in bytes
    if isinstance(key, str):
        key = key.encode('utf-8')

    # Calculate the starting index from the hash of the key
    start_index = hash_key(key) % len(pi_digits)

    # Pad the key with digits from pi, wrapping around if necessary
    padding_needed = target_length - len(key)
    if padding_needed > 0:
        # Get the relevant digits of pi for padding
        padding_string = (pi_digits * ((padding_needed // len(pi_digits)) + 1))[start_index:start_index + padding_needed]
        padding_bytes = padding_string.encode('utf-8')  # Convert padding to bytes
        key += padding_bytes  # Append padding to the key

    elif padding_needed < 0:
        key = key[:target_length]  # Truncate the key if it's too long

    return key

# Example usage:
pi_digits = read_pi_digits('pi_10000_digits.txt')  # Load the pi digits from a file
key = "my secret key"  # Example key
padded_key = pad_key_with_pi(key, pi_digits)
print(padded_key.hex())
print(len(padded_key))  # This should print 1024 if the padding is correct

def load_and_pad_key_from_file(file_path, pi_digits, target_length=1024):
    with open(file_path, 'rb') as f:
        key = f.read()  # Read the key from the file as bytes
    
    return pad_key_with_pi(key, pi_digits, target_length)

# Example usage:
file_key = load_and_pad_key_from_file('Screenshot 2025-02-20 160715.png', pi_digits)
print(file_key.hex())
print(len(file_key))  # Should print 1024 if the padding is correct
