# Template Project For Python/Gtk4/Libadwaita.


## Screenshot
![Alt text](https://raw.githubusercontent.com/yucefsourani/gtk4matjar/main/Screenshot1.png "Screenshot")

![Alt text](https://raw.githubusercontent.com/yucefsourani/gtk4matjar/main/Screenshot2.png "Screenshot")



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

* jinja2


# How to use

1. clone or download  repo.


2. Edit project info in create_py_gtk4temp.py

```python
NEW_NAME                = "gtk4matjar"
VERSION                 = "0.1beta"
APP_NAME                = "GTK4 gtk4matjar"
DEV_NAME                = "Yucef Sourani"
DEVELOPERS              = ["Yucef Sourani"]
DEV_EMAIL               = "example@examplee.com"
ID_NAME                 = "com.github.yucefsourani.gtk4matjar"
COMMENT                 = "TEST COMMANT"
COPYRIGHT               = "© 2026 Developer"
HOMEPAGE_WEB            = "https://github.com/yucefsourani/gtk4matjar" 
WEBSITE                 = "https://github.com/yucefsourani/gtk4matjar" # git
ISSUESITE               = "https://github.com/yucefsourani/gtk4matjar"
LICENSE                 = 10
LICENSE_STR             = "GPL-3.0-or-later"
SUMMARY                 = "A cross-platform GTK4/libadwaita application template."
GITMAIN_BRANCH          = "main"
FLATPAK_RUNTIME_VERSION = 49
TRANSLATOR_CREDITS      = 'translator-credits'
```

3.Close all Files and  run create_py_gtk4temp.py to create project template .

```bash
python ./create_py_gtk4temp.py
```

4.read README.md again.
