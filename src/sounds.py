import pygame


class SoundManager:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(SoundManager, cls).__new__(cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, "_initialized"):
            self._initialized = True
            self._sounds = {}
            self._background_music = None
            pygame.mixer.init()
    
    def load_sound(self, name, filepath):
        """Loads a sound effect and assigns it a name."""
        self._sounds[name] = pygame.mixer.Sound(filepath)

    def play_sound(self, name):
        """Plays a specific sound effect."""
        if name in self._sounds:
            self._sounds[name].play()
        else:
            print(f"Sound '{name}' not found!")

    def set_background_music(self, filepath):
        """Loads and sets the background music."""
        self._background_music = filepath
        pygame.mixer.music.load(filepath)
        pygame.mixer.music.set_volume(0.5)  # Adjust the volume

    def play_background_music(self, loops=-1, start=0.0, fade_ms=0):
        """Starts playing the background music."""
        if self._background_music:
            pygame.mixer.music.play(loops=loops, start=start, fade_ms=fade_ms)
        else:
            print("Background music not set!")

    def stop_background_music(self):
        """Stops the background music."""
        pygame.mixer.music.stop()

    def stop_all_sounds(self):
        """Stops all currently playing sounds."""
        pygame.mixer.stop()
