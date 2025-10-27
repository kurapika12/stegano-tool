# src/core/steganography.py
from PIL import Image
from .utils import text_to_bits, bits_to_text

def encode_message(image_path: str, output_path: str, message: str):
    """Embed a binary message into an image using LSB steganography."""
    img = Image.open(image_path)
    if img.mode != 'RGB':
        img = img.convert('RGB')

    binary_msg = text_to_bits(message) + '1111111111111110'  # end delimiter
    data_index = 0
    pixels = list(img.getdata())

    new_pixels = []
    for pixel in pixels:
        if data_index < len(binary_msg):
            r, g, b = pixel
            r = (r & ~1) | int(binary_msg[data_index]) if data_index < len(binary_msg) else r
            data_index += 1
            g = (g & ~1) | int(binary_msg[data_index]) if data_index < len(binary_msg) else g
            data_index += 1
            b = (b & ~1) | int(binary_msg[data_index]) if data_index < len(binary_msg) else b
            data_index += 1
            new_pixels.append((r, g, b))
        else:
            new_pixels.append(pixel)

    img.putdata(new_pixels)
    img.save(output_path)
    print(f"[+] Message hidden successfully in {output_path}")

def decode_message(image_path: str) -> str:
    """Extract hidden message from an image."""
    img = Image.open(image_path)
    binary_data = ''
    for pixel in img.getdata():
        for color in pixel[:3]:
            binary_data += str(color & 1)
    end_marker = '1111111111111110'
    message_bits = binary_data.split(end_marker)[0]
    return bits_to_text(message_bits)
