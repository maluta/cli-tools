"""
ip_qrcode_generator.py

This script retrieves the local machine’s IP address and generates a QR code image encoding that address,
optionally wrapped with a user-defined prefix and/or suffix (for example, “http://” before or “:8080” after).
It saves the resulting QR code as a PNG file (default “ip_qrcode.png”) and attempts to display it.

Usage:
    python ip_qrcode_generator.py [--prefix PREFIX] [--suffix SUFFIX] [--output OUTPUT_FILENAME]

Options:
    --prefix    Text to prepend to the IP address in the QR code (e.g., "http://")
    --suffix    Text to append to the IP address in the QR code (e.g., ":8000")
    --output    Filename for the generated PNG image (default: ip_qrcode.png)

Functions:
    get_ip_address()      Determine the local IP address by opening a UDP socket.
    generate_qr_code()    Create a QR code image with optional text annotations and save/display it.
    main()                Parse arguments, fetch IP, and invoke the QR code generation.

Example:
    $ python ip_qrcode_generator.py --prefix "http://" --suffix ":5000" --output my_ip_qr.png
"""

import socket
import qrcode
from PIL import Image, ImageDraw, ImageFont
import os
import argparse

def get_ip_address():
    """Get the local IP address of the machine"""
    try:
        # Create a socket connection to determine the IP address
        s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        # Doesn't need to be reachable
        s.connect(('8.8.8.8', 80))
        ip_address = s.getsockname()[0]
        s.close()
        return ip_address
    except Exception as e:
        print(f"Error getting IP address: {e}")
        # Fallback method
        hostname = socket.gethostname()
        return socket.gethostbyname(hostname)

def generate_qr_code(data, prefix="", suffix="", output_path="ip_qrcode.png"):
    """Generate a QR code image with the given data and optional prefix/suffix"""
    # Create the full string with prefix and suffix
    full_data = f"{prefix}{data}{suffix}"
    
    # Create QR code instance
    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    
    # Add data to the QR code
    qr.add_data(full_data)
    qr.make(fit=True)
    
    # Create an image from the QR code
    qr_img = qr.make_image(fill_color="black", back_color="white")
    
    # Create a larger image with space for text
    width, height = qr_img.size
    img = Image.new('RGB', (width, height + 60), color='white')
    
    # Paste the QR code onto the new image
    img.paste(qr_img, (0, 0))
    
    # Add text below the QR code
    draw = ImageDraw.Draw(img)
    try:
        # Try to use a TrueType font if available
        font = ImageFont.truetype("arial.ttf", 16)
    except IOError:
        # Fallback to default font
        font = ImageFont.load_default()
    
    # Draw the IP address
    draw.text((10, height+10), f"IP: {data}", fill="black", font=font)
    
    # Draw the full string with prefix and suffix
    draw.text((10, height+30), f"{full_data}", fill="black", font=font)
    
    # Save the image
    img.save(output_path)
    print(f"QR code generated and saved as {output_path}")
    
    # Display the image
    try:
        img.show()
    except Exception as e:
        print(f"Unable to display image automatically: {e}")
        print(f"Please open the saved image at: {os.path.abspath(output_path)}")

def main():
    # Set up command line argument parsing
    parser = argparse.ArgumentParser(description='Generate QR code for IP address with optional prefix and suffix')
    parser.add_argument('--prefix', default="", help='Prefix to add before the IP address (e.g., "http://")')
    parser.add_argument('--suffix', default="", help='Suffix to add after the IP address (e.g., ":8080")')
    parser.add_argument('--output', default="ip_qrcode.png", help='Output filename')
    
    args = parser.parse_args()
    
    ip_address = get_ip_address()
    print(f"Your IP address is: {ip_address}")
    print(f"Creating QR code for: {args.prefix}{ip_address}{args.suffix}")
    
    generate_qr_code(ip_address, args.prefix, args.suffix, args.output)

if __name__ == "__main__":
    main()
