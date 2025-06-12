"""Convenience launcher so users can just `python run_web.py` to start the web server."""

from web_app import app

if __name__ == "__main__":
    # Listen on all interfaces so LAN devices can connect during testing
    app.run(host="0.0.0.0", port=5000, debug=True) 