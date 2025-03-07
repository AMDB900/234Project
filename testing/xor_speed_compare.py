import os
import sys
import inspect
import time

sys.path.insert(1, os.path.join(sys.path[0], '..'))

from padding import *

def xor_old(text, key):
    offset = 1024
    if len(key) != offset:
        print(f"Error: Key size is {len(key)}B. Key must be {offset}B in size.")
        exit()
    i = 0
    result = b''
    while i < len(text):
        result += bytes(a ^ b for a, b in zip(text[i:i + offset], key))
        i += offset
    return result

def xor_new(text, key):
    # if text != 16MB: error
    offset = 1024 # Key size, set to 1KB
    if len(key) != offset:
        print(f"Error: Key size is {len(key)}B. Key must be {offset}B in size.")
        exit()
    return bytes(text[i] ^ key[i % offset] for i in range(len(text)))


if __name__ == "__main__":
    pi_digits = read_pi_digits('../pi_10000_digits.txt')
    padded_key = load_and_pad_key_from_file('../Screenshot 2025-02-20 160715.png', pi_digits)
    
    ## Real Test Input (2 = 2MB random numbers)
    f = open("../test_input/3", "rb")
    file = f.read()
    print(f"File: {len(file)}B: {file}\n")
    
    print("Old XOR")
    print("-------")
    
    start_time = time.perf_counter()
    encrypted_text = xor_old(file, padded_key)  # Using a padded key from padding.py, we assume it will work for a loaded one too
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    print(f"Encrypted in {execution_time:.4f} seconds: {encrypted_text}")
    
    start_time = time.perf_counter()
    decrypted_text = xor_old(encrypted_text, padded_key)
    end_time = time.perf_counter()
    execution_time = end_time - start_time
    
    print(f"Decrypted in {execution_time:.4f} seconds: {decrypted_text}\n")
    
    
    print("New XOR")
    print("-------")
    
    start_time = time.perf_counter()
    encrypted_text2 = xor_new(file, padded_key)  # Using a padded key from padding.py, we assume it will work for a loaded one too
    end_time = time.perf_counter()    
    execution_time = end_time - start_time

    print(f"Encrypted in {execution_time:.4f} seconds: {encrypted_text2}")
    
    start_time = time.perf_counter()
    decrypted_text2 = xor_new(encrypted_text, padded_key)
    end_time = time.perf_counter()    
    execution_time = end_time - start_time
    
    print(f"Decrypted in {execution_time:.4f} seconds: {decrypted_text2}")
    
    if encrypted_text == encrypted_text2:
        print("\nxor_old = xor_new\n")