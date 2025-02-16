def keyPadding(key: bytes, padding_byte: int = 0x00) -> bytearray:
    """
    Pads the inputted key to a length of 1KB. If the key is
    greater than 1KB, the key will be trimmed to exactly 1KB.
    Current version (1.0) pads the key with just zeros, but 
    later implementation will be done with digits of pi.
    The input should first be converted to a bytestring, not ran
    as a unicode. E.g: x = b"Hello World"
    """
    
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
