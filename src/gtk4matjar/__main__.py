#!/usr/bin/env python3
"""Entry point for the application."""

import sys
import gi
from gi.repository import Gio
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from {{ NEW_NAME }}.paths import get_resource_dir,ensure_user_dirs

if hasattr(sys, '_MEIPASS'):
    import locale
    import gettext
    from pathlib import Path
    localedir  = str(Path(sys._MEIPASS) / "share" / "locale")
    try:
        sys_lang_code, _ = locale.getdefaultlocale()
        langs = [sys_lang_code] if sys_lang_code else None
        lang = gettext.translation('{{ NEW_NAME }}', localedir, languages=langs, fallback=True)
        lang.install()
    except Exception as e:
        print(f"Warning: Could not load translations: {e}")
        gettext.install('{{ NEW_NAME }}', localedir)

def __load_resources():
    """Load GResource file."""
    ensure_user_dirs()
    resource_dir = get_resource_dir()
    resource_file = resource_dir / "{{ NEW_NAME }}.gresource"

    if resource_file.exists():
        resource = Gio.Resource.load(str(resource_file))
        resource._register()
        print(f"Loaded resources from: {resource_file}")
    else:
        print(f"Warning: Resource file not found: {resource_file}")
        print("Run: glib-compile-resources to compile resources")
__load_resources()

def main():
    """Main entry point."""
    from {{ NEW_NAME }}.application import Application
    app = Application()
    return app.run(sys.argv)


if __name__ == "__main__":
    sys.exit(main())
