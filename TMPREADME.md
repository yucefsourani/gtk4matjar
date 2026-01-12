# {{ NEW_NAME }}

{{ SUMMARY }}

## Features

- **Cross-platform**: Works on Linux, Windows, and macOS (macOs Not tested)
- **Modern UI**: Uses libadwaita for GNOME-style design
- **GStreamer support**: Media playback with plugin handling
- **Sqlmodel support**: Pyinstall Hook for sqlmodel pydantic sqlalchemy to  building windows exe
- **PyInstaller ready**: Create portable executables with GStreamer plugins
- **Flatpak ready**: Distribute on Linux with codec extensions
- **Smart path handling**: Automatically detects runtime environment
- **Github Action**: To build Windows exe by pyinstaller and MSYS2 (.github folder).

## Requirements

### Linux
```bash
# Fedora
sudo dnf install gtk4-devel libadwaita-devel python3-gobject # and glib tools(glib-compile-schemas glib-compile-resources ) and gstreamer plugins...

# Ubuntu/Debian
sudo apt install libgtk-4-dev libadwaita-1-dev python3-gi python3-gi-cairo gir1.2-gtk-4.0 gir1.2-adw-1 # and glib tools(glib-compile-schemas glib-compile-resources ) and gstreamer plugins...

# Arch Linux
sudo pacman -S gtk4 libadwaita python-gobject # and glib tools(glib-compile-schemas glib-compile-resources ) and gstreamer plugins...
```

### Windows (MSYS2)
```bash
pacman -S   mingw-w64-x86_64-gtk4 \
            mingw-w64-x86_64-libadwaita \
            mingw-w64-x86_64-python-gobject \
            mingw-w64-x86_64-gtk4 \
            mingw-w64-x86_64-libadwaita \
            mingw-w64-x86_64-python \
            mingw-w64-x86_64-python-pip \
            mingw-w64-x86_64-python-gobject \
            mingw-w64-x86_64-gstreamer \
            mingw-w64-x86_64-gst-plugins-base \
            mingw-w64-x86_64-gst-plugins-good \
            mingw-w64-x86_64-gst-plugins-bad \
            mingw-w64-x86_64-gst-plugins-ugly \
            mingw-w64-x86_64-gst-libav \
            mingw-w64-x86_64-pyinstaller \
            mingw-w64-x86_64-binutils \
            mingw-w64-x86_64-python-sqlmodel \
            mingw-w64-x86_64-gettext \
            mingw-w64-x86_64-glib2 \
            mingw-w64-x86_64-gettext-tools \
            base-devel
```

### macOS (Homebrew)
```bash
brew install gtk4 libadwaita pygobject3 # and glib tools and gstreamer plugins...
```

## Development

### Run from source (Linux)
```bash
# Clone and enter directory
cd {{ NEW_NAME }}

# Compile GResource
cd src/{{ NEW_NAME }}/resources
glib-compile-resources {{ NEW_NAME }}.gresource.xml
cd ../../../

# Install in development mode
pip install -e .

# Compile Gschema
mkdir -p  ~/.local/share/glib-2.0/schemas/
cp data/{{ ID_NAME }}.gschema.xml ~/.local/share/glib-2.0/schemas/
glib-compile-schemas ~/.local/share/glib-2.0/schemas/

# Run the application
python -m {{ NEW_NAME }}
```


## Packaging

### PyInstaller (Portable)

```bash
# Install PyInstaller
pip install pyinstaller

# Compile GResource first
cd src/{{ NEW_NAME }}/resources
glib-compile-resources {{ NEW_NAME }}.gresource.xml
cd ../../../

# Build with spec file
pyinstaller pyinstaller/{{ NEW_NAME }}.spec

# Output in dist/{{ NEW_NAME }}/
```

#### Portable Mode

Create a `portable.txt` file next to the executable to enable portable mode:
```bash
touch dist/{{ NEW_NAME }}/portable.txt
```
The app will store data in `dist/{{ NEW_NAME }}/data/` instead of user directories.


### Flatpak

```bash
# Install Flatpak and flatpak-builder
sudo dnf install flatpak flatpak-builder

# Add Flathub repo
flatpak remote-add --if-not-exists flathub https://flathub.org/repo/flathub.flatpakrepo

# Install SDK
flatpak install flathub org.gnome.Platform//{{ FLATPAK_RUNTIME_VERSION }}  org.gnome.Sdk//{{ FLATPAK_RUNTIME_VERSION }}

# Build
cd flatpak
flatpak-builder --user --install --force-clean build-dir {{ ID_NAME  }}.yml

# Run
flatpak run {{ ID_NAME  }}
```

## Project Structure

```
{{ NEW_NAME }}/
|── bin/                     # executable file (to run Entry point)
├── src/{{ NEW_NAME }}/          # Python package
│   ├── __main__.py          # Entry point
│   ├── application.py       # Adw.Application
│   ├── window.py            # Main window
│   ├── paths.py             # Path utilities
│   └── resources/           # GResource files
├── data/                    # Desktop file and icons and Gschema and metainfo file
├── pyinstaller/             # PyInstaller config
├── flatpak/                 # Flatpak manifest
├── po/                      # Gettext files
├── .github/                 # Github Action file to build windows exe by pyinstaller
├── pyproject.toml           # Python project config
└── meson.build              # Meson build system
└── create_py_gtk4temp.py    # To Create Project Template 
└── LICENSE                   
└── README.md                   
└── MANIFEST.in                  
└── changelog.html                  
```

## Path Detection

The `paths.py` module automatically detects the runtime environment:

| Environment | Data Directory | User Data |
|-------------|----------------|-----------|
| Development | `./src/.../resources` | `~/.local/share/{{ NEW_NAME }}` |
| PyInstaller | `sys._MEIPASS` | `./data` (portable) or user home |
| Flatpak | `/app/share/{{ NEW_NAME }}` | `~/.var/app/{{ ID_NAME  }}` |
| System Install | `/usr/share/{{ NEW_NAME }}` | `~/.local/share/{{ NEW_NAME }}` |

## License

{{ LICENSE_STR }}
