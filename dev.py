#!/usr/bin/env python3
"""
Local development server for the portfolio site.

Watches data/, templates/, and assets/ for changes, rebuilds
automatically, and serves the site locally — so you can preview
edits without pushing to GitHub.

Usage:
    python dev.py [port]

Then open http://localhost:8000 (or whatever port you passed) and
just refresh the page after saving a change; the rebuild happens
automatically in the background.
"""
import os
import sys
import time
import threading
import http.server
import socketserver
from pathlib import Path

import build

ROOT = Path(__file__).parent
WATCH_DIRS = [ROOT / "data", ROOT / "templates", ROOT / "assets"]
PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 8000


def snapshot():
    """Return {path: mtime} for every file under the watched directories."""
    files = {}
    for d in WATCH_DIRS:
        if not d.exists():
            continue
        for p in d.rglob("*"):
            if p.is_file():
                files[p] = p.stat().st_mtime
    return files


def watch_loop():
    last = snapshot()
    print("Watching data/, templates/, assets/ for changes... (Ctrl+C to stop)")
    while True:
        time.sleep(1)
        current = snapshot()
        if current != last:
            print("Change detected, rebuilding...")
            try:
                build.build()
                print("Rebuilt. Refresh your browser to see it.")
            except Exception as e:
                print(f"Build error: {e}")
            last = current


def serve():
    os.chdir(ROOT / "output")
    handler = http.server.SimpleHTTPRequestHandler
    with socketserver.TCPServer(("", PORT), handler) as httpd:
        print(f"Serving at http://localhost:{PORT}")
        httpd.serve_forever()


if __name__ == "__main__":
    build.build()
    watcher = threading.Thread(target=watch_loop, daemon=True)
    watcher.start()
    try:
        serve()
    except KeyboardInterrupt:
        print("\nStopped.")
