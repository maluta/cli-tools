#!/usr/bin/env python3
"""
URL Cleaner Script
Reads URL from clipboard, validates it, removes all query parameters, and saves back to clipboard.
"""

import re
import subprocess
import sys
from urllib.parse import urlparse, parse_qs, urlencode, urlunparse

def get_clipboard_content():
    """Get content from clipboard using xclip"""
    try:
        result = subprocess.run(['xclip', '-selection', 'clipboard', '-o'], 
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("Error: Could not read from clipboard. Make sure xclip is installed.")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: xclip not found. Please install it with: sudo apt-get install xclip")
        sys.exit(1)

def set_clipboard_content(content):
    """Set content to clipboard using xclip"""
    try:
        subprocess.run(['xclip', '-selection', 'clipboard'], 
                      input=content, text=True, check=True)
        print(f"✓ Cleaned URL saved to clipboard: {content}")
    except subprocess.CalledProcessError:
        print("Error: Could not write to clipboard.")
        sys.exit(1)

def is_valid_url(url):
    """Check if the string is a valid URL"""
    try:
        result = urlparse(url)
        return all([result.scheme, result.netloc])
    except Exception:
        return False

def remove_all_parameters(url):
    """Remove all query parameters from URL (everything after ?)"""
    parsed = urlparse(url)
    
    # Reconstruct URL without query parameters
    cleaned_url = urlunparse((
        parsed.scheme,
        parsed.netloc,
        parsed.path,
        parsed.params,
        '',  # Empty query string
        parsed.fragment
    ))
    
    return cleaned_url

def main():
    """Main function"""
    print("URL Cleaner - Removes all query parameters from URLs")
    
    # Get clipboard content
    clipboard_content = get_clipboard_content()
    
    if not clipboard_content:
        print("Error: Clipboard is empty")
        sys.exit(1)
    
    print(f"Original content: {clipboard_content}")
    
    # Check if it's a valid URL
    if not is_valid_url(clipboard_content):
        print("Error: Clipboard content is not a valid URL")
        sys.exit(1)
    
    # Remove all query parameters
    cleaned_url = remove_all_parameters(clipboard_content)
    
    # Check if URL was actually cleaned
    if cleaned_url == clipboard_content:
        print("ℹ No query parameters found - URL unchanged")
    else:
        print(f"✓ Removed all query parameters")
        print(f"Original: {clipboard_content}")
        print(f"Cleaned:  {cleaned_url}")
    
    # Save cleaned URL back to clipboard
    set_clipboard_content(cleaned_url)

if __name__ == "__main__":
    main()
