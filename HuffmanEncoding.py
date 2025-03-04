
# https://docs.python.org/3/library/os.html
import os
# https://docs.python.org/3/library/heapq.html
import heapq
# https://docs.python.org/3/library/collections.html
from collections import Counter
# Ref: https://www.geeksforgeeks.org/huffman-coding-in-python/

class HuffmanNode:
    # A node in the Huffman tree
    def __init__(self, byte, freq):
        self.byte = byte
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def byte_frequency_analysis(data):
    """
    Analyzes the frequency of each byte in the input data and returns an array
    with the most frequent byte as the first element.

    Args:
        data: Bytes or bytearray object.

    Returns:
        A list of byte patterns, sorted by frequency (descending) and byte value (ascending) during tie-breakers.
    """
    if not isinstance(data, (bytes, bytearray)):
        raise TypeError("Input data must be a bytes object")

    byte_counts = Counter(data)
    sorted_bytes = sorted(byte_counts.items(), key=lambda item: (-item[1], item[0]))
    return sorted_bytes

def build_huffman_tree(byte_frequencies):
    # Build the Huffman tree using a priority queue (min-heap)
    # Initialize the heap with leaf nodes for each byte
    heap = [HuffmanNode(byte, freq) for byte, freq in byte_frequencies]
    heapq.heapify(heap)
    
    while len(heap) > 1:
        left = heapq.heappop(heap)
        right = heapq.heappop(heap)
        merged = HuffmanNode(None, left.freq + right.freq)
        merged.left, merged.right = left, right
        heapq.heappush(heap, merged)
    
    return heap[0]


def generate_huffman_codes(node, prefix="", huffman_codes={}):
    if node is None:
        return
    if node.byte is not None:
        huffman_codes[node.byte] = prefix
    generate_huffman_codes(node.left, prefix + "0", huffman_codes)
    generate_huffman_codes(node.right, prefix + "1", huffman_codes)
    return huffman_codes

def huffman_encode(data):
    byte_frequencies = byte_frequency_analysis(data)
    root = build_huffman_tree(byte_frequencies)
    huffman_codes = generate_huffman_codes(root)
    missing_bytes = [byte for byte in data if byte not in huffman_codes]
    if missing_bytes:
        print("Error: missing bytes:", set(missing_bytes))
        exit()
    encoded_data = "".join(huffman_codes[byte] for byte in data)
    for char, code in huffman_codes.items():
        print(f"Character: {char}, Code: {code}")

    return encoded_data, root  # Return encoded data and tree for decoding


def huffman_decode(data, tree):
    decoded_data = bytearray()
    node = tree
    for bit in data:
        if bit == '0':
            node = node.left
        else:
            node = node.right
        if node.byte is not None:
            decoded_data.append(node.byte)
            node = tree  # Reset to the root of the tree
    return decoded_data

# Function to get the file name from the user
# Ref: https://www.geeksforgeeks.org/python-list-files-in-a-directory/
def get_file():
    # List all files in the current directory
    files = [f for f in os.listdir() if os.path.isfile(f)]
    content = []
    if not files:
        print("No files found in the directory.")
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

        # Read and print file content
        with open(filename, 'rb') as f:
            content = f.read()
            print(f"Loading: {filename} ...\n")
    
    return content

# Helper function to convert string to binary representation for comparison
def string_to_binary(s):
    return ' '.join(format(ord(char), '08b') for char in s)

def xor_byte_encrpyt(text, key):
    """
    Performs XOR operation on input string and a key.

    Args:
        text: input file, string or bytes/bytearray.
        key: 1KB string or bytes/bytearray.

    Returns:
        result: String or bytearray containing the XOR result of corresponding bytes.
                     Returns None if arrays are not of the same length.
    """
    if len(text) != len(key):
        return None
    
    result = ''
    for i in range(len(text)):
        result += chr(ord(text[i]) ^ key[i % len(key)])
    return result

if __name__ == "__main__":
    print("Select a file to encrypt:")
    data = get_file()

    print("Select a key file:")
    key = get_file()

    string_data = data.decode('utf-8', errors='ignore')

    # Example usage
    encoded_data, tree = huffman_encode(data)

    decoded_data = huffman_decode(encoded_data, tree)

    with open("text.khn", "w") as file:
        file.write(encoded_data)

    print("Original:", data)
    print("Original length:", len(string_to_binary(string_data)))
    print("Encoded length:", len(encoded_data))
    print("Encoded:", encoded_data)
    print("Decoded:", decoded_data)

