"""Main application window."""

import gi

gi.require_version('Gtk', '4.0')
gi.require_version('Adw', '1')

from gi.repository import Gtk, Adw, Gio, GLib,Pango


@Gtk.Template(resource_path='{{ GIORESOURCE_ID }}/ui/window.ui')
class MainWindow(Adw.ApplicationWindow):
    """Main application window."""

    __gtype_name__ = 'MainWindow'

    # Template children
    toast_overlay = Gtk.Template.Child()
    main_content  = Gtk.Template.Child()

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._app  = self.get_application()

        clamp = Adw.Clamp()
        clamp.set_maximum_size(600)
        self.main_content.append(clamp)

        content_box = Gtk.Box(orientation=Gtk.Orientation.VERTICAL, spacing=24)
        content_box.set_valign(Gtk.Align.CENTER)
        content_box.set_vexpand(True)
        clamp.set_child(content_box)

        icon = Gtk.Image.new_from_icon_name("application-x-executable-symbolic")
        icon.set_pixel_size(128)
        icon.add_css_class("dim-label")
        content_box.append(icon)

        title = Gtk.Label.new("Welcome to {{ APP_NAME }}")
        title.set_ellipsize(Pango.EllipsizeMode.END)
        title.add_css_class("title-1")
        content_box.append(title)
        subtitle = Gtk.Label.new("{{ SUMMARY }}")
        subtitle.add_css_class("dim-label")
        subtitle.set_wrap(True)
        subtitle.set_wrap_mode(Pango.WrapMode.WORD)
        content_box.append(subtitle)


        button = Gtk.Button.new_with_label("Show Toast")
        button.add_css_class("pill")
        button.add_css_class("suggested-action")
        button.set_halign(Gtk.Align.CENTER)
        button.connect("clicked", self._on_button_clicked)
        content_box.append(button)



        self.setup_settings()
        
    def setup_settings(self):
        self.app_settings = Gio.Settings.new_with_path("{{ ID_NAME }}" ,"{{ GIORESOURCE_ID }}/")
        self.app_settings.bind("width", self, "default-width",
                           Gio.SettingsBindFlags.DEFAULT)
        self.app_settings.bind("height", self, "default-height",
                           Gio.SettingsBindFlags.DEFAULT)
        self.app_settings.bind("is-maximized", self, "maximized",
                           Gio.SettingsBindFlags.DEFAULT)
        self.app_settings.bind("is-fullscreen", self, "fullscreened",
                           Gio.SettingsBindFlags.DEFAULT)
        self._app.get_style_manager().set_color_scheme(Adw.ColorScheme(self.app_settings.get_int("colorschemeenum")))


    def _on_button_clicked(self, button):
        """Handle button click."""
        toast = Adw.Toast.new("Hello from {{ APP_NAME }}")
        toast.set_timeout(3)
        self.toast_overlay.add_toast(toast)



