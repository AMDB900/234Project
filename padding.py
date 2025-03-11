"""
References:
https://www.geeksforgeeks.org/python-strings-encode-method/
https://www.geeksforgeeks.org/hashlib-module-in-python/
"""

import random
import time
import hashlib
import os

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

def load_and_pad_key_from_file(file_path, pi_digits, target_length=1024):
    with open(file_path, 'rb') as f:
        key = f.read()  # Read the key from the file as bytes
    
    return pad_key_with_pi(key, pi_digits, target_length)

def pad_file(input_file_path, seed=12345):
    # Read the content of the input file
    print(f"Loading {input_file_path} ...", end='')
    start = time.perf_counter()
    
    with open(input_file_path, 'rb') as file:
        file_content = file.read()
        
    end = time.perf_counter()
    print(f" {end - start:.4f} seconds")
    
    if len(file_content) > (12 * 1024 * 1024): # 12 MB
        print(f"Error: File size is {len(file_content)}B. File must be less than {12 * 1024 * 1024}B in size.")
        exit()
    
    print(f"Padding {input_file_path} ...", end='')
    start = time.perf_counter()
    
    # Extract the length of the string (4 bytes)
    content_length = len(file_content)
    
    # Get the file suffix (file extension)
    file_suffix = os.path.splitext(input_file_path)[1].encode('utf-8')  # Ensure it's a byte string
    while len(file_suffix) < 5: # Pad the extension to 5 bytes (covers .docx)
        file_suffix = file_suffix + b'0'
        
    # Append the 4-byte length of the content and file suffix
    linear_array = bytearray(content_length.to_bytes(4, byteorder='little') + file_suffix + file_content)
    
    # Calculate how much padding is needed to reach 16MB
    total_size = 16 * 1024 * 1024  # 16 MB
    current_size = len(linear_array)
    
    # If the current size is less than 16MB, we need to pad
    padding_needed = total_size - current_size
    
    linear_array += random.randbytes(padding_needed)
    # Ensure the final array size is exactly 16MB
    assert len(linear_array) == total_size
    
    end = time.perf_counter()
    print(f" {end - start:.4f} seconds")

    return bytes(linear_array)

def return_original_file(content):
    # Extract the length of the string (4 bytes)
    content_length = content[0:4]
    length = int.from_bytes(content_length, byteorder='little')
    
    # Get the file suffix (file extension)
    file_suffix = content[4:9]
    suffix = file_suffix.split(b'0')[0]

    # Gather file data based on length of the string
    data = content[9:9 + length]

    text = "output" + suffix.decode()
    with open(text, "wb") as file:
        file.write(data)
    
    return data

if __name__ == "__main__":
    
    # pad_key_with_pi example usage:
    pi_digits = read_pi_digits('pi_10000_digits.txt')  # Load the pi digits from a file
    key = "my secret key"  # Example key
    padded_key = pad_key_with_pi(key, pi_digits)
    print(padded_key.hex())
    print(len(padded_key))  # This should print 1024 if the padding is correct
    
    # load_and_pad_key_from_file example usage:
    file_key = load_and_pad_key_from_file('Screenshot 2025-02-20 160715.png', pi_digits)
    print(file_key.hex())
    print(len(file_key))  # Should print 1024 if the padding is correct

    # Example usage for 
    input_file_path = 'test_input/1.docx'  # Replace with your file path
    linear_array = pad_file(input_file_path)

    # Output file should be 16MB with the data as described

    print(f"Linear array created with size: {len(linear_array)} bytes")
    print(return_original_file(linear_array))

