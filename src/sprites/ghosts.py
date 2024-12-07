from pygame.sprite import Sprite
from pygame import image, transform, draw

from src.configs import *
from src.utils.coord_utils import get_coords_from_idx, get_tiny_matrix
from src.sprites.sprite_configs import GHOST_PATHS

class Ghost(Sprite):
    def __init__(self,
                 name: str,
                 ghost_pos: dict,
                 start_x: float,
                 start_y: float,
                 tiny_matrix_fast: list[list],
                 tiny_matrix_slow: list[list],
                 screen,
                 frame_rate: int=5
                 ):
        super().__init__()
        self.name = name
        self.ghost_pos = ghost_pos
        self.start_x = start_x
        self.start_y = start_y
        self.tiny_matrix_fast = tiny_matrix_fast
        self.tiny_matrix_slow = tiny_matrix_slow
        self.frame_rate = frame_rate
        self.speed = GHOST_SPEED_FAST
        self.ghost_x, self.ghost_y = get_coords_from_idx(ghost_pos,
                                                         start_x,
                                                         start_y,
                                                         self.speed,
                                                         self.speed,
                                                         len(tiny_matrix_fast),
                                                         len(tiny_matrix_fast[0])
                                                         )
        self.screen = screen
        self.image = image.load(GHOST_PATHS[self.name][0])
        self.image = transform.scale(self.image, PACMAN)
        self.rect = self.image.get_rect(topleft=(self.ghost_x,
                                                 self.ghost_y))
        self.released = False
        self.mode = 'chase'
        self.released = False

    def panic_mode(self):
        self.speed = GHOST_SPEED_SLOW
        self.speed = GHOST_SPEED_SLOW
        self.mode = 'panic'
    
    def normal_mode(self):
        self.speed = GHOST_SPEED_FAST
        self.speed = GHOST_SPEED_FAST
        self.mode = 'chase'

    def _draw_bounding_box(self):
        draw.rect(self.screen, Colors.RED, (self.ghost_x,
                                            self.ghost_y,
                                            CELL_SIZE[0] * 2,
                                            CELL_SIZE[0] * 2), 1)

    def draw_ghost(self):
        self.rect.x = self.ghost_x + (CELL_SIZE[0] * 2 - self.rect.width) // 2
        self.rect.y = self.ghost_y + (CELL_SIZE[0] * 2 - self.rect.height) // 2
    
    def update(self):
        self.draw_ghost()

class Blinky(Ghost):
    def __init__(self, ghost_pos: dict, start_x: float, 
                 start_y: float, tiny_matrix_fast, tiny_matrix_slow,
                 screen, frame_rate: int = 5):
        super().__init__("blinky", ghost_pos, start_x, start_y, 
                         tiny_matrix_fast, tiny_matrix_slow, screen, frame_rate)
        ...

    def path_finding(self):
        ...

class Inky(Ghost):
    def __init__(self, ghost_pos: dict, start_x: float, 
                 start_y: float, tiny_matrix_fast, tiny_matrix_slow,
                 screen, frame_rate: int = 3):
        super().__init__("inky", ghost_pos, start_x, start_y, 
                         tiny_matrix_fast, tiny_matrix_slow, screen, frame_rate)
        ...

    def path_finding(self):
        ...

class Pinky(Ghost):
    def __init__(self, ghost_pos: dict, start_x: float, 
                 start_y: float, tiny_matrix_fast, tiny_matrix_slow,
                 screen, frame_rate: int = 1):
        super().__init__("pinky", ghost_pos, start_x, start_y, 
                         tiny_matrix_fast, tiny_matrix_slow, screen, frame_rate)
        ...

    def path_finding(self):
        ...

class Clyde(Ghost):
    def __init__(self, ghost_pos: dict, start_x: float, 
                 start_y: float, tiny_matrix_fast, tiny_matrix_slow,
                 screen, frame_rate: int = 0):
        super().__init__("clyde", ghost_pos, start_x, start_y, 
                         tiny_matrix_fast, tiny_matrix_slow, screen, frame_rate)
        ...

    def path_finding(self):
        ...

class GhostManager:
    def __init__(self,
                 ghost_pos: dict,
                 start_x: float,
                 start_y: float,
                 matrix: list[list],
                 screen):
        self.matrix = matrix
        self.start_x = start_x
        self.start_y = start_y
        self.screen = screen
        self.orig_ghost_pos = ghost_pos
        self.tiny_matrix_loader()
        self.load_ghosts()

    def load_ghosts(self):
        self.ghosts_list = []
        ghosts = [Blinky,Inky,Pinky,Clyde]
        curr_pad = 0
        for ghost in ghosts:
            ghost_pos = self.orig_ghost_pos.copy()
            ghost_pos[0] = ghost_pos[0] * (CELL_SIZE[0] // GHOST_SPEED_FAST)
            ghost_pos[1] = (ghost_pos[1] * (CELL_SIZE[0] // GHOST_SPEED_FAST)) + curr_pad
            ghost_obj = ghost(ghost_pos, 
                                self.start_x, self.start_y,
                                self.matrix_5px, 
                                self.matrix_2px, self.screen)
            self.ghosts_list.append(ghost_obj)
            curr_pad += 5

    def tiny_matrix_loader(self):
        self.matrix_5px = get_tiny_matrix(self.matrix, CELL_SIZE[0], GHOST_SPEED_FAST)
        self.matrix_2px = get_tiny_matrix(self.matrix, CELL_SIZE[0], GHOST_SPEED_SLOW)
