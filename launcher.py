#!/usr/bin/env python3
"""
Desktop launcher for the packaged Resolva build.

Starts the same Flask app on a local port and opens it in the default
browser, so a non-technical user just double-clicks the .exe. Used only by
the PyInstaller build (resolva.spec); for local dev you can run `python app.py`
directly instead.

Port note: 5000 is preferred, but on macOS the AirPlay Receiver squats on
port 5000 by default, and any other local app may hold it too. If 5000 is
busy we fall back to the first free port the OS hands us, and open the
browser at whatever port was actually bound.
"""

import socket
import threading
import webbrowser

from app import app, store

PREFERRED_PORT = 5000


def pick_port() -> int:
    """Use 5000 if free; otherwise let the OS assign a free port."""
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        try:
            s.bind(("127.0.0.1", PREFERRED_PORT))
            return PREFERRED_PORT
        except OSError:
            pass
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind(("127.0.0.1", 0))
        return s.getsockname()[1]


if __name__ == "__main__":
    store.init_db()
    port = pick_port()
    threading.Timer(1.2, lambda: webbrowser.open(f"http://127.0.0.1:{port}")).start()
    # use_reloader=False is essential in a frozen build.
    app.run(host="127.0.0.1", port=port, debug=False, use_reloader=False)
