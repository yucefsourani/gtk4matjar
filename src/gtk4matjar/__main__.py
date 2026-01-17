#!/usr/bin/env python3
"""Entry point for the application."""

import sys
if hasattr(sys, '_MEIPASS'):
    import locale
    import gettext
    from pathlib import Path
    import ctypes
    import os
    import gi
    gi.require_version('PangoCairo', '1.0')
    from gi.repository import PangoCairo
    
    
    os.environ['GST_PLUGIN_SYSTEM_PATH'] = os.path.join(sys._MEIPASS, 'gst_plugins')
    os.environ['GST_PLUGIN_PATH'] = os.path.join(sys._MEIPASS, 'gst_plugins')
    os.environ['GST_PLUGIN_SCANNER'] = os.path.join(sys._MEIPASS,'gst-plugin-scanner.exe')
    os.environ['GST_REGISTRY_FORK'] = 'yes'

    def load_custom_fonts():
        base_path = sys._MEIPASS
        fonts_dir = os.path.join(base_path, "share", "fonts")
        if os.path.isdir(fonts_dir):
            font_map = PangoCairo.FontMap.get_default()
            fonts = [font for font in os.listdir(fonts_dir) ]
            for font in fonts:
                font_path = os.path.join(fonts_dir, font)
                try:
                    font_map.add_font_file(font_path)
                    print(f"Loaded: {font}")
                except Exception as e:
                    print(f"Error loading {font}: {e}")
    
    load_custom_fonts()

    localedir  = str(Path(sys._MEIPASS) / "share" / "locale")
    def get_windows_language():
        try:
            lang_code = None
            lang_code = os.environ.get('LANG') or os.environ.get('LC_ALL') or os.environ.get('LANGUAGE')
            if not lang_code:
                windll = ctypes.windll.kernel32
                lang_id = windll.GetUserDefaultUILanguage()
                lang_code = locale.windows_locale.get(lang_id)
            if lang_code:
                lang_code = lang_code.split('.')[0]
                langs = []
                for l in [lang_code ,lang_code.split('_')[0]]:
                    mo_l = os.path.join(localedir , l , "LC_MESSAGES" , "{{ NEW_NAME }}.mo")
                    if os.path.isfile(mo_l):
                        os.environ['LANG'] = l 
                        langs.insert(0,l)
                    else:
                        langs.append(l)
                return langs 
        except Exception as e:
            print(e)
        os.environ['LANG'] = "en"
        return ['en','en_US']
    
    try:
        sys_lang_code = get_windows_language()
        lang = gettext.translation('{{ NEW_NAME }}', localedir, languages=sys_lang_code, fallback=True)
        lang.install()
    except Exception as e:
        print(f"Warning: Could not load translations: {e}")
        gettext.install('{{ NEW_NAME }}', localedir)
        
import gi
from gi.repository import Gio
gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from {{ NEW_NAME }}.paths import get_resource_dir,ensure_user_dirs





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
