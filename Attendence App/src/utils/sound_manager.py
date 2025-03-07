"""
Sound management utility for the Time Tracker application.
Handles sound effects and muting functionality.
"""

# Try to import winsound, but don't fail if it's not available
try:
    import winsound
    SOUND_AVAILABLE = True
    # Define sound constants only if winsound is available
    SOUND_OK = 0x00000000
    SOUND_EXCLAMATION = 0x00000030
    SOUND_WARNING = 0x00000030
    SOUND_INFORMATION = 0x00000040
except ImportError:
    SOUND_AVAILABLE = False
    # Define dummy sound constants
    SOUND_OK = 0
    SOUND_EXCLAMATION = 0
    SOUND_WARNING = 0
    SOUND_INFORMATION = 0

class SoundManager:
    def __init__(self):
        """Initialize the sound manager with default settings."""
        self.is_muted = not SOUND_AVAILABLE
        self.sound_effects = {
            'in': SOUND_OK,
            'out': SOUND_EXCLAMATION,
            'pause': SOUND_WARNING,
            'resume': SOUND_INFORMATION
        }

    def play_sound(self, sound_type):
        """
        Play a sound effect if not muted and sound is available.
        
        Args:
            sound_type (str): Type of sound to play ('in', 'out', 'pause', 'resume')
        """
        if SOUND_AVAILABLE and not self.is_muted:
            try:
                if sound_type in self.sound_effects:
                    winsound.MessageBeep(self.sound_effects[sound_type])
            except:
                pass  # Silently continue if sound fails

    def toggle_mute(self):
        """Toggle the mute state."""
        if SOUND_AVAILABLE:
            self.is_muted = not self.is_muted
            return self.is_muted

    @property
    def is_sound_available(self):
        """Check if sound system is available."""
        return SOUND_AVAILABLE 