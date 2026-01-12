"""Main application class."""

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib, Gdk
from {{ NEW_NAME }}.window import MainWindow

from {{ NEW_NAME }}.paths import (
    APP_ID,
    get_resource_dir,
    get_runtime_info
)



class Application(Adw.Application):
    """Main application class."""

    def __init__(self):
        super().__init__(
            application_id=APP_ID,
            flags=Gio.ApplicationFlags.DEFAULT_FLAGS,
            resource_base_path='{{ GIORESOURCE_ID }}'
        )

        # Set up actions
        self.create_action('quit', self.on_quit_action, ['<primary>q'])
        self.create_action('about', self.on_about_action)
        self.create_action('preferences', self.on_preferences_action)
        self.create_action('shortcuts', self.on_show_shortcuts_dialog)

    def do_startup(self):
        """Called when the application starts."""
        Adw.Application.do_startup(self)


        # Load CSS
        self._load_css()

        # Print runtime info for debugging
        print("Runtime Info:")
        for key, value in get_runtime_info().items():
            print(f"  {key}: {value}")


    def _load_css(self):
        """Load application CSS."""
        css_provider = Gtk.CssProvider()

        # Try to load from GResource first
        try:
            css_provider.load_from_resource("{{ GIORESOURCE_ID }}/css/style.css")
        except GLib.Error:
            # Fallback to file
            resource_dir = get_resource_dir()
            css_file = resource_dir / "css" / "style.css"
            if css_file.exists():
                css_provider.load_from_path(str(css_file))
                print(f"Loaded CSS from: {css_file}")
            else:
                print("Warning: CSS file not found")
                return

        Gtk.StyleContext.add_provider_for_display(
            Gdk.Display.get_default(),
            css_provider,
            Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION,
        )

    def do_activate(self):
        """Called when the application is activated."""
        # Get the current window or create a new one
        win = self.props.active_window
        if not win:
            win = MainWindow(application=self)
        win.present()

    def create_action(self, name, callback, shortcuts=None):
        """Create a simple action."""
        action = Gio.SimpleAction.new(name, None)
        action.connect("activate", callback)
        self.add_action(action)
        if shortcuts:
            self.set_accels_for_action(f"app.{name}", shortcuts)

    def on_quit_action(self, action, param):
        """Handle quit action."""
        self.quit()

    def on_about_action(self, action, param):
        """Handle about action."""
        about = Adw.AboutDialog(
            application_name="{{ APP_NAME }}",
            application_icon=APP_ID,
            developer_name="{{ DEV_NAME }}",
            version="{{ VERSION }}",
            developers={{ DEVELOPERS }},
            copyright="{{ COPYRIGHT }}",
            license_type=Gtk.License(int({{ LICENSE }})),
            website="{{ HOMEPAGE_WEB }}",
            issue_url="{{ ISSUESITE }}",
        )
        about.set_translator_credits("{{ TRANSLATOR_CREDITS }}")
        about.present(self.props.active_window)

    def on_preferences_action(self, widget, _):
        """Callback for the app.preferences action."""
        print('app.preferences action activated')

    def on_show_shortcuts_dialog(self, action, param):
        builder = Gtk.Builder.new_from_resource("{{ GIORESOURCE_ID }}/ui/shortcuts-dialog.ui")
        window = builder.get_object("shortcuts_dialog")
        window.present(self.props.active_window)
