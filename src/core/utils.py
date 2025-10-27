# src/core/utils.py
import os

def text_to_bits(text: str) -> str:
    """Convert string to binary representation."""
    return ''.join(format(ord(c), '08b') for c in text)

def bits_to_text(bits: str) -> str:
    """Convert binary string back to text."""
    chars = [bits[i:i+8] for i in range(0, len(bits), 8)]
    return ''.join(chr(int(b, 2)) for b in chars)

def validate_image(path: str) -> bool:
    """Check if the file exists and is an image."""
    valid_ext = ('.png', '.bmp')
    return os.path.isfile(path) and path.lower().endswith(valid_ext)

def chunk_data(data: str, size: int):
    """Split binary data into chunks."""
    for i in range(0, len(data), size):
        yield data[i:i+size]
