from pygame.sprite import Sprite
from pygame import image, transform

from src.configs import CELL_SIZE, PACMAN_SPEED
from src.sprites.sprite_configs import GHOST_PATHS

class Ghost(Sprite):
    def __init__(self,
                 name: str,
                 ghost_pos: dict,
                 start_x: float,
                 start_y: float,
                 matrix,
                 tiny_matrix,
                 coord_matrix,
                 frame_rate=5
                 ):
        ...