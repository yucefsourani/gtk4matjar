#!/usr/bin/env python3
import os
from jinja2 import Environment, FileSystemLoader
import datetime
from pathlib import Path

NEW_NAME                = "gtk4matjar"
VERSION                 = "0.1beta"
APP_NAME                = "GTK4 gtk4matjar"
DEV_NAME                = "Yucef Sourani"
DEVELOPERS              = ["Yucef Sourani"]
DEV_EMAIL               = "example@exampleee.com"
ID_NAME                 = "com.github.yucefsourani.gtk4matjar"
COMMENT                 = "TEST COMMENT"
COPYRIGHT               = "© 2026 Developer"
HOMEPAGE_WEB            = "https://github.com/yucefsourani/gtk4matjar" 
WEBSITE                 = "https://github.com/yucefsourani/gtk4matjar" # git repository link
ISSUESITE               = "https://github.com/yucefsourani/gtk4matjar"
LICENSE                 = 10 #https://lazka.github.io/pgi-docs/#Gtk-4.0/enums.html#Gtk.License
LICENSE_STR             = "GPL-3.0-or-later"
GIORESOURCE_ID          = "/" + "/".join(ID_NAME.split("."))
SUMMARY                 = "A cross-platform GTK4/libadwaita application template."
DATE_NOW                = str(datetime.date.today())
GITMAIN_BRANCH          = "main"
FLATPAK_RUNTIME_VERSION = 49
TRANSLATOR_CREDITS      = 'translator-credits'


data = {"NEW_NAME"                : NEW_NAME ,
        "ID_NAME"                 : ID_NAME,
        "COMMENT"                 : COMMENT,
        "WEBSITE"                 : WEBSITE,
        "ISSUESITE"               : ISSUESITE,
        "APP_NAME"                : APP_NAME,
        "DEV_NAME"                : DEV_NAME,
        "VERSION"                 : VERSION,
        "DEVELOPERS"              : DEVELOPERS,
        "COPYRIGHT"               : COPYRIGHT,
        "LICENSE"                 : LICENSE,
        "GIORESOURCE_ID"          : GIORESOURCE_ID,
        "SUMMARY"                 : SUMMARY,
        "HOMEPAGE_WEB"            : HOMEPAGE_WEB,
        "DEV_EMAIL"               : DEV_EMAIL,
        "LICENSE_STR"             : LICENSE_STR,
        "DATE_NOW"                : DATE_NOW,
        "GITMAIN_BRANCH"          : GITMAIN_BRANCH,
        "FLATPAK_RUNTIME_VERSION" : FLATPAK_RUNTIME_VERSION,
        "TRANSLATOR_CREDITS"      : TRANSLATOR_CREDITS
        }

env = Environment(loader=FileSystemLoader('.'))

files = ["src/gtk4matjar/paths.py",
         "src/gtk4matjar/__main__.py",
         "src/gtk4matjar/application.py",
         "src/gtk4matjar/window.py",
         "src/gtk4matjar/gstreamer.py",
         "src/gtk4matjar.egg-info/entry_points.txt",
         "src/gtk4matjar.egg-info/top_level.txt",
         "src/gtk4matjar.egg-info/SOURCES.txt",
         "src/gtk4matjar.egg-info/PKG-INFO",
         "pyproject.toml",
         "pyinstaller/gtk4matjar.spec",
         "flatpak/com.example.gtk4matjar.yml",
         "meson.build",
         "bin/gtk4matjar.in",
         "data/com.example.gtk4matjar.desktop.in",
         "data/com.example.gtk4matjar.metainfo.xml.in",
         "data/com.example.gtk4matjar.gschema.xml",
         "TMPREADME.md",
         "MANIFEST.in",
         ".github/workflows/build-windows.yml",
         "src/gtk4matjar/resources/gtk4matjar.gresource.xml",
         "src/gtk4matjar/resources/ui/window.ui",
         "po/POTFILES.in",
         "po/meson.build"
        ]
for f in files:
    template = env.get_template(f)
    output = template.render(data)
    with open(f, 'w') as nf:
        nf.write(output)



def remove_file(file_location):
    if os.path.isfile(file_location):
        return os.remove(file_location)




folders = [("src/gtk4matjar/resources/gtk4matjar.gresource.xml",f"src/gtk4matjar/resources/{NEW_NAME}.gresource.xml"),
          ("src/gtk4matjar",f"src/{NEW_NAME}"),
          ("src/gtk4matjar.egg-info",f"src/{NEW_NAME}.egg-info"),
          ("pyinstaller/gtk4matjar.spec",f"pyinstaller/{NEW_NAME}.spec"),
          ("flatpak/com.example.gtk4matjar.yml",f"flatpak/{ID_NAME}.yml"),
          ("bin/gtk4matjar.in",f"bin/{NEW_NAME}.in"),
          ("data/com.example.gtk4matjar.desktop.in",f"data/{ID_NAME}.desktop.in"),
          ("data/icons/hicolor/scalable/apps/com.example.gtk4matjar.svg",f"data/icons/hicolor/scalable/apps/{ID_NAME}.svg"),
          ("data/icons/Adwaita/scalable/apps/com.example.gtk4matjar.svg",f"data/icons/Adwaita/scalable/apps/{ID_NAME}.svg"),
          ("data/icons/hicolor/symbolic/apps/com.example.gtk4matjar-symbolic.svg",f"data/icons/hicolor/symbolic/apps/{ID_NAME}-symbolic.svg"),
          ("data/icons/Adwaita/symbolic/apps/com.example.gtk4matjar-symbolic.svg",f"data/icons/Adwaita/symbolic/apps/{ID_NAME}-symbolic.svg"),
          ("data/icons/com.example.gtk4matjar.ico",f"data/icons/{ID_NAME}.ico"),
          ("data/icons/com.example.gtk4matjar.icns",f"data/icons/{ID_NAME}.icns"),
          ("data/com.example.gtk4matjar.metainfo.xml.in",f"data/{ID_NAME}.metainfo.xml.in"),
          ("data/com.example.gtk4matjar.gschema.xml",f"data/{ID_NAME}.gschema.xml"),
          ("TMPREADME.md","README.md"),
         ]
         
for i in folders : 
    f,nf = i
    f  = Path(i[0])
    nf = Path(i[1])
    if f.exists():
        f.rename(nf)
        print(f"Rename {f}-->{nf}")


remove_file("Screenshot1.png")
remove_file("Screenshot2.png")
print("\nDone.")
    
        



        


