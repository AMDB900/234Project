from xor import *
from HuffmanEncoding import *

def get_key():
    # List all files in the current directory
    files = [f for f in os.listdir() if os.path.isfile(f)]
    content = []
    if not files:
        print("No files found in the directory.")
        exit()
    else:
        for i, file in enumerate(files):
            print(f"{i + 1}: {file}")

        while True:
            try:
                choice = int(input("Enter the number of the file: ")) - 1
                if 0 <= choice < len(files):
                    break
                else:
                    print("Invalid choice, please enter a valid number.")
            except ValueError:
                print("Please enter a number.")

        filename = files[choice]

    return filename

if __name__ == "__main__":

    pi_digits = read_pi_digits('pi_10000_digits.txt')
    padded_key = load_and_pad_key_from_file('Screenshot 2025-02-20 160715.png', pi_digits)

    ## XOR with HuffmanEncoding
    print("Select a file to encrypt:")
    data = get_file()
    print("\nSelect a key file:")
    key = load_and_pad_key_from_file(get_key(), pi_digits)

    string_data = data.decode('utf-8', errors='ignore')

    # print("Original:", data)
    print("Original size:", len(data))
    print()

    # XOR the key against the file in 1KB chunks
    print("XOR... ", end="")

    start_time = time.perf_counter()
    encrypted = xor(data, key)
    end_time = time.perf_counter()

    fxor_time = end_time - start_time
    print(f"           finished in {fxor_time:7.4f} seconds")

    # Perform Huffman encoding of resulting array
    print("Huffman encode... ", end="")

    start_time = time.perf_counter()
    encoded_data, tree = huffman_encode(encrypted)
    end_time = time.perf_counter()

    huffman_time = end_time - start_time
    print(f"finished in {huffman_time:7.4f} seconds")
    encryption_time = huffman_time + fxor_time
    print(f"Total encryption time ------- {encryption_time:7.4f} seconds")

    # print("\nEncrypted:", encoded_data)
    print("Encrypted size:", len(encoded_data))

    # with open("text.khn", "w") as file:
    #   file.write(encoded_data)
    # with open("XOR.txt", "w") as file:
    #   file.write(str(encrypted))

    # Perform Huffman decoding
    print("\nHuffman decode... ", end="")

    start_time = time.perf_counter()
    decoded_data = huffman_decode(encoded_data, tree)
    end_time = time.perf_counter()

    decode_time = end_time - start_time
    print(f"finished in {decode_time:7.4f} seconds")

    # XOR the decoded data against the file
    print("Reverse XOR... ", end="")

    start_time = time.perf_counter()
    decrypted = xor(decoded_data, key)
    end_time = time.perf_counter()

    rxor_time = end_time - start_time
    print(f"   finished in {rxor_time:7.4f} seconds")

    decryption_time = rxor_time + decode_time
    print(f"Total decryption time ------- {decryption_time:7.4f} seconds")

    # print("\nDecrypted:", decrypted)
    print("Decrypted size:", len(decrypted))

    if encrypted == decoded_data:
        print("\nSuccess: Decoded  Data = XOR'd Data")
    if decrypted == data:
        print("Success: Original Data = Decrypted Data")

    print("\nExtracting file size and suffix / Removing padding...", end='')

    start_time = time.perf_counter()
    og = return_original_file(decrypted)
    end_time = time.perf_counter()

    extract_time = end_time - start_time
    print(f" {extract_time:.4f} seconds")
    print("Extracted size:", len(og))
