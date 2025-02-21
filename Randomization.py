import random
import string
import json

# ---------------- STEP 1: Generate a 1KB Random Key ----------------

def generate_random_key():
    """Generates a secure 1KB encryption key."""
    encryption_key = ''.join(random.choices(string.ascii_letters + string.digits + "!@#$%^&*", k=1024))
    return encryption_key

# ---------------- STEP 2: Randomization Functions ----------------

def generate_random_pattern(length):
    """Generates a random pattern for shuffling."""
    pattern = list(range(length))
    random.shuffle(pattern)
    return pattern

def apply_randomization(text, pattern):
    """Applies the given pattern to shuffle the text."""
    return ''.join(text[i] for i in pattern)

def undo_randomization(shuffled_text, pattern):
    """Reverses the randomization using the pattern."""
    original_text = [''] * len(shuffled_text)
    for i, char in enumerate(shuffled_text):
        original_text[pattern[i]] = char
    return ''.join(original_text)

# ---------------- STEP 3: Generate and Randomize Huffman Data ----------------

def generate_huffman_encoded_data(length=100):
    """Generates a random Huffman-encoded binary string (0s and 1s)."""
    return ''.join(random.choices("01", k=length))

# ---------------- TESTING THE IMPLEMENTATION ----------------

# Generate and print the 1KB random key
random_key = generate_random_key()
print(f"🔑 Generated 1KB Random Key:\n{random_key[:100]}... (truncated)\n")

# Generate random Huffman-encoded binary data
huffman_data = generate_huffman_encoded_data(50)  # 50-bit random Huffman data
print(f"📄 Original Huffman-encoded Data:\n{huffman_data}\n")

# Generate a randomization pattern
pattern = generate_random_pattern(len(huffman_data))

# Apply randomization
randomized_data = apply_randomization(huffman_data, pattern)
print(f"🔀 Randomized Huffman Data:\n{randomized_data}\n")

# Undo randomization
recovered_data = undo_randomization(randomized_data, pattern)
print(f"♻️ Recovered Huffman Data (Should Match Original):\n{recovered_data}\n")

# Verification
if huffman_data == recovered_data:
    print("✅ Randomization and Undo Process Worked Correctly!")
else:
    print("❌ Something Went Wrong!")
