from HuffmanEncoding import *

def xor(text, key):
    if len(text) != (16 * 1024 * 1024): # File size set to 16MB
        print(f"Error: File size is {len(text)}B. File must be {16 * 1024 * 1024}B in size")
        exit()
        
    offset = 1024 # Key size, set to 1KB
    if len(key) != offset:
        print(f"Error: Key size is {len(key)}B. Key must be {offset}B in size.")
        exit()
        
    return bytes(text[i] ^ key[i % offset] for i in range(len(text)))

