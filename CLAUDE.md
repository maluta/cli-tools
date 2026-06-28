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

Every Python tool carries PEP 723 inline metadata (the `# /// script` block) and is run with `uv run`,
which resolves dependencies and the interpreter automatically. `ip_qrcode_generator.py` declares
`qrcode[pil]`; the url-cleaner and open-chat-to-rewrite scripts are stdlib-only (`dependencies = []`).

```
uv run ip-qr-code/ip_qrcode_generator.py --prefix "http://" --suffix ":5000" --output my_ip_qr.png
```

The url-cleaner scripts additionally shell out to external clipboard tools — `xclip` (X11) or
`wl-clipboard` (Wayland) must be installed:

```
uv run url-cleaner/url-cleaner-wayland.py
```

There are no tests, linters, or build steps in this repo.

## Conventions when editing

- The two `url-cleaner` scripts are intentionally identical except for the clipboard backend. Any change to
  the cleaning/validation logic must be applied to **both** files to keep them in sync.
- Each tool is fully self-contained; do not introduce shared modules or a top-level package — keep new tools
  as standalone scripts in their own directory with a short README, and add an entry to the root `README.md`.
- New tools should follow the same pattern: a PEP 723 `# /// script` block (empty `dependencies` if
  stdlib-only) and a `.sh` wrapper that calls `uv run`. Use `uv run` in all docs and examples.
