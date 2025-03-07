import time
from padding import *
from byte_frequency_analysis import *
from HuffmanEncoding import *

def xor(text, key):
    # if text != 16MB: error
    offset = 1024 # Key size, set to 1KB
    if len(key) != offset:
        print(f"Error: Key size is {len(key)}B. Key must be {offset}B in size.")
        exit()
    return bytes(text[i] ^ key[i % offset] for i in range(len(text)))

if __name__ == "__main__":

    pi_digits = read_pi_digits('pi_10000_digits.txt')
    padded_key = load_and_pad_key_from_file('Screenshot 2025-02-20 160715.png', pi_digits)
    
    ## Integration with HuffmanEncoding
    print("Select a file to encrypt:")
    data = get_file()
    key = padded_key # Using a padded key

    string_data = data.decode('utf-8', errors='ignore')

    print("Original:", data)
    print("Original size:", len(data))
    print()

    # XOR the key against the file in 1KB chunks
    print("XOR... ", end="")
    
    start_time = time.perf_counter()
    encrypted = xor(data, key)
    end_time = time.perf_counter()
    
    fxor_time = end_time - start_time
    print(f"           finished in {fxor_time:.4f} seconds")
    
    # Perform Huffman encoding of resulting array
    print("Huffman encode... ", end="")
    
    start_time = time.perf_counter()
    encoded_data, tree = huffman_encode(encrypted)
    end_time = time.perf_counter()
    
    huffman_time = end_time - start_time
    print(f"finished in {huffman_time:.4f} seconds")
    encryption_time = huffman_time + fxor_time
    print(f"Total encryption time ------- {encryption_time:.4f} seconds")
    
    print("\nEncrypted:", encoded_data)
    print("Encrypted size:", len(encoded_data))
    
    #with open("text.khn", "w") as file:
     #   file.write(encoded_data)
    #with open("XOR.txt", "w") as file:
     #   file.write(str(encrypted))

    # Perform Huffman decoding
    print("\nHuffman decode... ", end="")
    
    start_time = time.perf_counter()
    decoded_data = huffman_decode(encoded_data, tree)
    end_time = time.perf_counter()
    
    decode_time = end_time - start_time
    print(f"finished in {decode_time:.4f} seconds")
    
    
    # XOR the decoded data against the file
    print("Reverse XOR... ", end="")
    
    start_time = time.perf_counter()
    decrypted = xor(decoded_data, key)
    end_time = time.perf_counter()
    
    rxor_time = end_time - start_time
    print(f"   finished in {rxor_time:.4f} seconds")
    
    decryption_time = rxor_time + decode_time
    print(f"Total decryption time ------- {decryption_time:.4f} seconds")
    
    print("\nDecrypted:", decrypted)
    print("Decrypted size:", len(decrypted))
    
    if encrypted == decoded_data:
        print("\nSuccess: Decoded Data = XOR'd Data")
    if decrypted == data:
        print("Success: Original Data = Decrypted Data")