def keyPadding(key: bytes, padding_byte: int = 0x00) -> bytearray:   # Padding will be 0s
    # Create a bytearray from the provided key
    byte_array = bytearray(key)
    
    # Check if the length of the key is already 1KB (1024 bytes)
    if len(byte_array) >= 1024:
        return byte_array[:1024]  # Trim it to 1KB if it's longer than 1KB
    
    # Pad the bytearray with the specified padding byte until it's 1KB long
    byte_array.extend([padding_byte] * (1024 - len(byte_array)))
    
    return byte_array

# Example usage
key = b"my_short_key"  # Some example key that's less than 1KB
padded_key = keyPadding(key)

#print(padded_key.hex()) # Prints the hexadecimal of the padded key
print(len(padded_key))  # Should print 1024