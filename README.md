# cli-tools

1. `/ip-to-qrcode`

This script retrieves the local machine’s IP address and generates a QR code image encoding that address,
optionally wrapped with a user-defined prefix and/or suffix.

Example usage:
`python ip_qrcode_generator.py --prefix "http://" --suffix ":5000" --output my_ip_qr.png`


2. `/url-cleaner`

This script reads URL from clipboard, validates it, removes all query parameters, and saves back to clipboard.

Example usage:
`python url-cleaner.py`


