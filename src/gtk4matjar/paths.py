# Path utilities for cross-platform support
# Handles different runtime environments:
# - Development (running from source)
# - PyInstaller (frozen executable)
# - Flatpak (sandboxed)
# - System install (package manager)

import sys
import os
from pathlib import Path
from typing import Optional

APP_ID = "{{ ID_NAME  }}"
APP_NAME = "{{ NEW_NAME }}"


def is_frozen() -> bool:
    """Check if running from PyInstaller bundle."""
    return getattr(sys, 'frozen', False) and hasattr(sys, '_MEIPASS')


def is_flatpak() -> bool:
    """Check if running inside Flatpak sandbox."""
    return os.path.exists("/.flatpak-info")


def is_development() -> bool:
    """Check if running in development mode (from source)."""
    # Check if we're running from a source directory
    src_dir = Path(__file__).parent
    return (src_dir / "resources").exists() and not is_frozen()


def get_base_dir() -> Path:
    """Get the base directory of the application."""
    if is_frozen():
        # PyInstaller bundle
        return Path(sys._MEIPASS)
    elif is_flatpak():
        # Flatpak installation
        return Path(f"/app/share/{APP_NAME}")
    else:
        # Development or system install
        return Path(__file__).parent


def get_data_dir() -> Path:
    """Get the data directory (read-only resources)."""
    if is_frozen():
        return Path(sys._MEIPASS) / "data"
    elif is_flatpak():
        return Path(f"/app/share/{APP_NAME}")
    elif is_development():
        return Path(__file__).parent / "resources"
    else:
        # System install - check common locations
        candidates = [
            Path(f"/usr/share/{APP_NAME}"),
            Path(f"/usr/local/share/{APP_NAME}"),
            Path.home() / f".local/share/{APP_NAME}",
        ]
        for path in candidates:
            if path.exists():
                return path
        # Fallback to development path
        return Path(__file__).parent / "resources"


def get_resource_dir() -> Path:
    """Get the directory containing GResource files."""
    if is_frozen():
        return Path(sys._MEIPASS) / "resources"
    elif is_flatpak():
        return Path(f"/app/share/{APP_NAME}")
    else:
        return Path(__file__).parent / "resources"


def get_user_data_dir() -> Path:
    """Get the user data directory (writable)."""
    if is_flatpak():
        # Flatpak has its own data directory
        data_home = os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")
        return Path(data_home) / APP_NAME
    elif sys.platform == "win32":
        # Windows: use APPDATA
        appdata = os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")
        return Path(appdata) / APP_NAME
    elif sys.platform == "darwin":
        # macOS: use Application Support
        return Path.home() / "Library" / "Application Support" / APP_NAME
    else:
        # Linux/Unix: use XDG_DATA_HOME
        data_home = os.environ.get("XDG_DATA_HOME", Path.home() / ".local/share")
        return Path(data_home) / APP_NAME


def get_user_config_dir() -> Path:
    """Get the user config directory (writable)."""
    if is_flatpak():
        config_home = os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
        return Path(config_home)
    elif sys.platform == "win32":
        appdata = os.environ.get("APPDATA", Path.home() / "AppData" / "Roaming")
        return Path(appdata) / APP_NAME
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Preferences" / APP_NAME
    else:
        config_home = os.environ.get("XDG_CONFIG_HOME", Path.home() / ".config")
        return Path(config_home) / APP_NAME


def get_user_cache_dir() -> Path:
    """Get the user cache directory (writable)."""
    if is_flatpak():
        cache_home = os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")
        return Path(cache_home)
    elif sys.platform == "win32":
        localappdata = os.environ.get("LOCALAPPDATA", Path.home() / "AppData" / "Local")
        return Path(localappdata) / APP_NAME / "Cache"
    elif sys.platform == "darwin":
        return Path.home() / "Library" / "Caches" / APP_NAME
    else:
        cache_home = os.environ.get("XDG_CACHE_HOME", Path.home() / ".cache")
        return Path(cache_home) / APP_NAME


def get_portable_data_dir() -> Optional[Path]:
    """
    Get portable data directory (next to executable).
    Returns None if not running in portable mode.
    """
    if is_frozen():
        # Check for portable marker file next to executable
        exe_dir = Path(sys.executable).parent
        portable_marker = exe_dir / "portable.txt"
        if portable_marker.exists():
            return exe_dir / "data"
    return None


def ensure_user_dirs() -> None:
    """Create user directories if they don't exist."""
    # Use portable dir if available
    portable_dir = get_portable_data_dir()
    if portable_dir:
        portable_dir.mkdir(parents=True, exist_ok=True)
        return

    get_user_data_dir().mkdir(parents=True, exist_ok=True)
    get_user_config_dir().mkdir(parents=True, exist_ok=True)
    get_user_cache_dir().mkdir(parents=True, exist_ok=True)


def get_runtime_info() -> dict:
    """Get information about the current runtime environment."""
    return {
        "frozen": is_frozen(),
        "flatpak": is_flatpak(),
        "development": is_development(),
        "platform": sys.platform,
        "base_dir": str(get_base_dir()),
        "data_dir": str(get_data_dir()),
        "resource_dir": str(get_resource_dir()),
        "user_data_dir": str(get_user_data_dir()),
        "user_config_dir": str(get_user_config_dir()),
        "user_cache_dir": str(get_user_cache_dir()),
        "portable_data_dir": str(get_portable_data_dir()) if get_portable_data_dir() else None,
    }
