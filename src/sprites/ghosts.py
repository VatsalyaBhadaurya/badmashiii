"""
module to handle ghost logics
Ghosts
1) Blinky: attacks pacman directly
2) pinky: targets 4 tiles ahead of pacman
3) Inky: calculates its target using Blinky and Inkpy positions
4) Clyde: Odd one out. If pacman is within 8 tiles, he attacks pacman directly, else, he scatters.

Ghost object needs
1) screen
2) game_state
3) matrix
4) Ghost original position in the matrix, the ghost house.

how ghost moves?
now, i brought ghost out of the den. Initially, ghost will have velocity of 0.01 (increase to 0.015 for blinky), t will be 0
movement direction is None.
write a method, that will check if movement direction is none, if yes then it will check pacman coords,
"""
from pygame.sprite import Sprite
from pygame import Surface
from pygame import image, transform
import pygame.time as pytime

from src.game.state_management import GameState
from src.sprites.sprite_configs import GHOST_PATHS
from src.configs import PACMAN, CELL_SIZE, GHOST_SPEED_FAST, GHOST_DELAYS
from src.utils.coord_utils import get_coords_from_idx, get_idx_from_coords
from src.utils.ghost_movement_utils import get_direction

class Ghost(Sprite):
    def __init__(self,
                 name: str,
                 ghost_matrix_pos: tuple[int, int],
                 grid_start_pos: tuple[int | float, int | float],
                 matrix: list[list[str]],
                 game_state: GameState
                 ):
        super().__init__()
        self.name = name
        self._ghost_matrix_pos = ghost_matrix_pos
        self._grid_start_pos = grid_start_pos
        self._matrix = matrix
        self._game_state = game_state
        self._is_released = False
        self._creation_time = pytime.get_ticks()
        self._dead_wait = GHOST_DELAYS[self.name]
        self.load_images()
        
    def build_bounding_boxes(self, x, y):
        self.rect.x = x + (CELL_SIZE[0] * 2 - self.rect.width) // 2
        self.rect.y = y + (CELL_SIZE[1] * 2 - self.rect.height) // 2

    def load_images(self):
        ghost_images = GHOST_PATHS[self.name][0]
        self.image = transform.scale(image.load(ghost_images).convert_alpha(),
                                     PACMAN)
        x, y = get_coords_from_idx(self._ghost_matrix_pos,
                                   *self._grid_start_pos,
                                   *CELL_SIZE,
                                   len(self._matrix),
                                   len(self._matrix[0]))
        self.rect = self.image.get_rect(topleft=(x, y))
        self.rect_x = x
        self.rect_y = y
    
    def check_is_released(self):
        if self._is_released:
            return
        curr_time = pytime.get_ticks()
        if (curr_time - self._creation_time) > self._dead_wait:
            self._is_released = True
            self._dead_wait = 1000
            self.rect_y -= CELL_SIZE[0] * 3 #going outside the ghost den

    def update(self, dt):
        self.build_bounding_boxes(self.rect_x, self.rect_y)
        self.check_is_released()

class GhostManager:
    def __init__(self,
                 screen: Surface,
                 game_state: GameState,
                 matrix: list[list[str]],
                 ghost_matrix_pos: tuple[int, int],
                 grid_start_pos: tuple[int, int],
                 ):
        self.screen = screen
        self.game_state = game_state
        self.matrix = matrix
        self.ghost_matrix_pos = ghost_matrix_pos
        self.grid_start_pos = grid_start_pos
        self.ghosts_list = []
        self.load_ghosts()
    
    def load_ghosts(self):
        ghost_pos = self.ghost_matrix_pos
        self.ghosts_list.append(Ghost('blinky',
                                      self.ghost_matrix_pos,
                                      self.grid_start_pos,
                                      self.matrix,
                                      self.game_state))
