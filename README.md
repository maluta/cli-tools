# cli-tools

1. `/ip-to-qrcode`

This script retrieves the local machine’s IP address and generates a QR code image encoding that address,
optionally wrapped with a user-defined prefix and/or suffix.

Example
$ python ip_qrcode_generator.py --prefix "http://" --suffix ":5000" --output my_ip_qr.png
