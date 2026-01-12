"""GStreamer utilities for the application."""

import os
import sys

import gi

gi.require_version('Gst', '1.0')
from gi.repository import Gst, GLib

from {{ NEW_NAME }}.paths import is_frozen, get_base_dir


def init_gstreamer():
    """
    Initialize GStreamer with proper plugin paths.
    Call this before using any GStreamer functionality.
    """
    # Set plugin path for PyInstaller builds
    if is_frozen():
        base_dir = get_base_dir()
        plugin_path = base_dir / 'lib' / 'gstreamer-1.0'
        
        if plugin_path.exists():
            os.environ['GST_PLUGIN_PATH'] = str(plugin_path)
            os.environ['GST_PLUGIN_SYSTEM_PATH'] = str(plugin_path)
            
            # Disable plugin scanner for frozen apps (already scanned)
            os.environ['GST_PLUGIN_SCANNER'] = ''
            
            # Set registry path to writable location
            if sys.platform == 'win32':
                registry_dir = base_dir / 'cache'
            else:
                registry_dir = base_dir / '.cache'
            
            registry_dir.mkdir(exist_ok=True)
            os.environ['GST_REGISTRY'] = str(registry_dir / 'gstreamer-registry.bin')
            os.environ['GST_REGISTRY_UPDATE'] = 'no'
    
    # Initialize GStreamer
    Gst.init(None)


def get_gst_version():
    """Get GStreamer version string."""
    return '.'.join(map(str, Gst.version()))


def create_playbin(uri=None):
    """
    Create a playbin element for media playback.
    
    Args:
        uri: Optional URI to play
        
    Returns:
        Gst.Element: A playbin element
    """
    playbin = Gst.ElementFactory.make('playbin', 'playbin')
    if uri:
        playbin.set_property('uri', uri)
    return playbin


def create_pipeline_from_string(pipeline_string):
    """
    Create a GStreamer pipeline from a string description.
    
    Args:
        pipeline_string: Pipeline description (e.g., "videotestsrc ! autovideosink")
        
    Returns:
        Gst.Pipeline: A pipeline element
    """
    return Gst.parse_launch(pipeline_string)


def get_available_plugins():
    """
    Get list of available GStreamer plugins.
    
    Returns:
        list: Plugin names
    """
    registry = Gst.Registry.get()
    plugins = registry.get_plugin_list()
    return [plugin.get_name() for plugin in plugins]


def check_element_available(element_name):
    """
    Check if a GStreamer element is available.
    
    Args:
        element_name: Name of the element (e.g., 'playbin', 'x264enc')
        
    Returns:
        bool: True if element is available
    """
    factory = Gst.ElementFactory.find(element_name)
    return factory is not None


def get_supported_formats():
    """
    Get information about supported media formats.
    
    Returns:
        dict: Supported formats by category
    """
    formats = {
        'audio_decoders': [],
        'video_decoders': [],
        'audio_encoders': [],
        'video_encoders': [],
        'demuxers': [],
        'muxers': [],
    }
    
    registry = Gst.Registry.get()
    
    # Get all features
    features = registry.get_feature_list(Gst.ElementFactory)
    
    for feature in features:
        klass = feature.get_metadata('klass')
        if not klass:
            continue
            
        name = feature.get_name()
        
        if 'Decoder/Audio' in klass:
            formats['audio_decoders'].append(name)
        elif 'Decoder/Video' in klass:
            formats['video_decoders'].append(name)
        elif 'Encoder/Audio' in klass:
            formats['audio_encoders'].append(name)
        elif 'Encoder/Video' in klass:
            formats['video_encoders'].append(name)
        elif 'Demuxer' in klass:
            formats['demuxers'].append(name)
        elif 'Muxer' in klass:
            formats['muxers'].append(name)
    
    return formats


class SimplePlayer:
    """
    A simple media player using GStreamer.
    
    Example:
        player = SimplePlayer()
        player.play('/path/to/video.mp4')
        # ... when done
        player.stop()
    """
    
    def __init__(self):
        self._playbin = Gst.ElementFactory.make('playbin', 'player')
        self._bus = self._playbin.get_bus()
        self._bus.add_signal_watch()
        
        # Connect signals
        self._bus.connect('message::error', self._on_error)
        self._bus.connect('message::eos', self._on_eos)
        self._bus.connect('message::state-changed', self._on_state_changed)
        
        # Callbacks
        self.on_error = None
        self.on_eos = None
        self.on_state_changed = None
    
    def play(self, uri):
        """Play media from URI."""
        if not uri.startswith(('file://', 'http://', 'https://', 'rtsp://')):
            # Convert file path to URI
            uri = GLib.filename_to_uri(uri, None)
        
        self._playbin.set_property('uri', uri)
        self._playbin.set_state(Gst.State.PLAYING)
    
    def pause(self):
        """Pause playback."""
        self._playbin.set_state(Gst.State.PAUSED)
    
    def resume(self):
        """Resume playback."""
        self._playbin.set_state(Gst.State.PLAYING)
    
    def stop(self):
        """Stop playback."""
        self._playbin.set_state(Gst.State.NULL)
    
    def seek(self, position_seconds):
        """Seek to position in seconds."""
        self._playbin.seek_simple(
            Gst.Format.TIME,
            Gst.SeekFlags.FLUSH | Gst.SeekFlags.KEY_UNIT,
            position_seconds * Gst.SECOND
        )
    
    def get_position(self):
        """Get current position in seconds."""
        success, position = self._playbin.query_position(Gst.Format.TIME)
        if success:
            return position / Gst.SECOND
        return 0
    
    def get_duration(self):
        """Get media duration in seconds."""
        success, duration = self._playbin.query_duration(Gst.Format.TIME)
        if success:
            return duration / Gst.SECOND
        return 0
    
    def set_volume(self, volume):
        """Set volume (0.0 to 1.0)."""
        self._playbin.set_property('volume', max(0.0, min(1.0, volume)))
    
    def get_volume(self):
        """Get current volume."""
        return self._playbin.get_property('volume')
    
    def set_video_sink(self, sink):
        """Set custom video sink element."""
        self._playbin.set_property('video-sink', sink)
    
    def _on_error(self, bus, message):
        error, debug = message.parse_error()
        if self.on_error:
            self.on_error(error.message, debug)
    
    def _on_eos(self, bus, message):
        self.stop()
        if self.on_eos:
            self.on_eos()
    
    def _on_state_changed(self, bus, message):
        if message.src == self._playbin:
            old, new, pending = message.parse_state_changed()
            if self.on_state_changed:
                self.on_state_changed(old.value_nick, new.value_nick)
