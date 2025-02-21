
# https://docs.python.org/3/library/heapq.html
import heapq
# https://docs.python.org/3/library/collections.html
import collections
# Ref: https://www.geeksforgeeks.org/huffman-coding-in-python/
class HuffmanNode:
    def __init__(self, byte, freq):
        self.byte = byte
        self.freq = freq
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

def build_huffman_tree(byte_frequencies):
    heap = [HuffmanNode(byte, freq) for byte, freq in byte_frequencies.items()]
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
    byte_frequencies = collections.Counter(data)
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

# Example Usage
with open("text.txt", "rb") as file:
    data = file.read()  # Read the file only once
encoded_data, tree = huffman_encode(data)
decoded_data = huffman_decode(encoded_data, tree)
print("Original:", data)
print("Encoded:", encoded_data)
print("Decoded:", decoded_data)
