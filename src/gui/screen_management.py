from src.configs import *
from src.utils.coord_utils import center_element
from src.gui.pacman_grid import *

class ScreenManager:
    def __init__(self, screen, game_state):
        self._screen = screen
        self._game_state = game_state
        self.pacman = PacmanGrid(screen, game_state)

    def draw_screens(self):
        # self.pacman.draw_outliners()
        self.pacman.draw_level()