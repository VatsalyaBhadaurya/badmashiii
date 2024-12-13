from src.configs import *
from src.gui.pacman_grid import *
from src.utils.coord_utils import center_element


class ScreenManager:
    def __init__(self, screen, game_state, all_sprites):
        self._screen = screen
        self._game_state = game_state
        self.all_sprites = all_sprites
        self.pacman = PacmanGrid(screen, game_state)
        self.all_sprites.add(self.pacman.pacman)
        for ghost in self.pacman.ghost.ghosts_list:
            self.all_sprites.add(ghost)

    def draw_screens(self):
        self.pacman.ghost.monitor_ghosts()
        self.pacman.draw_level()
