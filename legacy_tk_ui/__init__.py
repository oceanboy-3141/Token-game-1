"""Legacy Tkinter UI package

This sub-package contains all historical Tk-based desktop interface code.
It is retained for posterity and research purposes only; the supported
front-end today is the Flask web app in `web_app.py`.
"""

# Re-export the primary GUI class so external code can simply do
# `from legacy_tk_ui import TokenGameGUI`
from .gui_interface import TokenGameGUI  # noqa: F401

# Optional helpers for old scripts
from .startup_dialog import show_startup_dialog  # noqa: F401 