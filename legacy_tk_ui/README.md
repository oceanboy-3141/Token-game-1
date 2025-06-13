# Legacy Tkinter UI

This folder contains the original desktop interface built with Tkinter.

It's no longer the actively supported front-end (the Flask web
application in `web_app.py` is the primary interface now), but the code
is kept here for historical reference and for users who still prefer a
native desktop experience.

**Important notes**

1. The modules have been namespaced (e.g., `legacy_tk_ui.gui_interface`)
   so they don't clutter the top-level package.
2. External code can still use `from legacy_tk_ui import TokenGameGUI`.
3. No new features are planned for this UI; only critical fixes will be
   accepted. 