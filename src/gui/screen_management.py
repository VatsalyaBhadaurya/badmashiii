from src.configs import *
from src.utils.coord_utils import center_element
from src.gui.pacman_grid import *

class ScreenManager:
    def __init__(self, screen, game_state, all_sprites):
        self._screen = screen
        self._game_state = game_state
        self.all_sprites = all_sprites
        self.pacman = PacmanGrid(screen, game_state)
        self.all_sprites.add(self.pacman.pacman)

    def draw_screens(self):
        self.pacman.draw_outliners()
        self.pacman.draw_level()