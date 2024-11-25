from pygame.sprite import Sprite
from pygame import image, transform

from src.sprites.sprite_configs import *

class Pacman(Sprite):
    def __init__(self, x, y, 
                 width, height,
                 frame_rate=5):
        super().__init__()
        self.frames = [
            transform.scale(
                image.load(path).convert_alpha(), 
                (width, height)
            ) 
            for path in PACMAN_PATHS['right']
        ]
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame_rate = frame_rate
        self.counter = 0

    def frame_update(self):
        self.counter += 1
        if self.counter >= self.frame_rate:
            self.counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def update(self):
        self.frame_update()

