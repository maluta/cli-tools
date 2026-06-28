# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## What this repo is

A personal collection of small, independent CLI utilities. There is no shared package, build system, or
cross-script dependency — each tool lives in its own directory, is run standalone, and has its own README.
`README.md` at the root acts as the index of tools.

## Tools

- `ip-qr-code/ip_qrcode_generator.py` — gets the local IP (via a UDP socket to `8.8.8.8`, no packets sent),
  encodes it into a QR PNG with optional `--prefix`/`--suffix`/`--output`, annotates the image with the IP
  text, and tries to open it.
- `url-cleaner/` — reads a URL from the clipboard, strips **all** query parameters (everything after `?`,
  keeping path/params/fragment), and writes it back. Two backends:
  - `url-cleaner.py` — X11, uses `xclip`.
  - `url-cleaner-wayland.py` — Wayland, uses `wl-paste`/`wl-copy`.
  - `url-cleaner.sh` — wrapper that activates the `~/senv` venv and runs the Wayland version (intended for
    binding to a keyboard shortcut).
- `open-chat-to-rewrite/` — reads clipboard text (Wayland `wl-paste`, reusing the url-cleaner pattern),
  prepends the fixed instruction `reescreva para deixar mais claro`, URL-encodes it with
  `urllib.parse.urlencode`, and opens `https://chat.com/?q=<encoded>` via stdlib `webbrowser`. Has a
  `.sh` venv launcher for keybinding.

## Running

`ip_qrcode_generator.py` carries PEP 723 inline metadata (the `# /// script` block declaring `qrcode[pil]`).
Run it with uv so dependencies resolve automatically:

```
uv run ip-qr-code/ip_qrcode_generator.py --prefix "http://" --suffix ":5000" --output my_ip_qr.png
```

The url-cleaner scripts use only the Python stdlib but shell out to external clipboard tools — `xclip`
(X11) or `wl-clipboard` (Wayland) must be installed:

```
python url-cleaner/url-cleaner-wayland.py
```

There are no tests, linters, or build steps in this repo.

## Conventions when editing

- The two `url-cleaner` scripts are intentionally identical except for the clipboard backend. Any change to
  the cleaning/validation logic must be applied to **both** files to keep them in sync.
- Each tool is fully self-contained; do not introduce shared modules or a top-level package — keep new tools
  as standalone scripts in their own directory with a short README, and add an entry to the root `README.md`.
- The README's `python ip_qrcode_generator.py` example is stale; prefer `uv run` for that tool.
