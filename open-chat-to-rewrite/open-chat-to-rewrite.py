# /// script
# requires-python = ">=3.9"
# dependencies = []
# ///
"""
Open Chat to Rewrite - Wayland Version
Reads text from the clipboard, prepends a fixed rewrite instruction, and opens
chat.com in the browser with the prompt passed as the ?q= query parameter.
Uses wl-clipboard (wl-paste) for Wayland compatibility.

Usage:
    uv run open-chat-to-rewrite.py

This script uses only the Python standard library, but the PEP 723 metadata
block above lets `uv run` manage the interpreter and execution environment.
"""
import subprocess
import sys
import webbrowser
from urllib.parse import urlencode

PROMPT_PREFIX = "reescreva para deixar mais claro"
CHAT_BASE_URL = "https://chat.com/"

def get_clipboard_content():
    """Get content from clipboard using wl-paste"""
    try:
        result = subprocess.run(['wl-paste'],
                              capture_output=True, text=True, check=True)
        return result.stdout.strip()
    except subprocess.CalledProcessError:
        print("Error: Could not read from clipboard. Make sure wl-clipboard is installed.")
        sys.exit(1)
    except FileNotFoundError:
        print("Error: wl-paste not found. Please install it with: sudo apt-get install wl-clipboard")
        sys.exit(1)

def build_query(content):
    """Build the prompt: the rewrite instruction, a blank line, then the content"""
    return f"{PROMPT_PREFIX}\n\n{content}"

def build_url(query):
    """Build the chat.com URL with the prompt as the ?q= query parameter"""
    return f"{CHAT_BASE_URL}?" + urlencode({"q": query})

def main():
    """Main function"""
    print("Open Chat to Rewrite - Opens chat.com with the clipboard text to rewrite (Wayland)")

    # Get clipboard content
    clipboard_content = get_clipboard_content()

    if not clipboard_content:
        print("Error: Clipboard is empty")
        sys.exit(1)

    print(f"Original content: {clipboard_content}")

    # Build the prompt and target URL
    query = build_query(clipboard_content)
    url = build_url(query)
    print(f"Opening: {url}")

    # Open the URL in the default browser
    if not webbrowser.open(url):
        print("Unable to open the browser automatically.")
        print(f"Please open this URL manually: {url}")

if __name__ == "__main__":
    main()
