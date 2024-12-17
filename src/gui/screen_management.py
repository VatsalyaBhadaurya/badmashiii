from src.configs import *
from src.gui.pacman_grid import *
from src.gui.loading_screen import LoadingScreen
from src.utils.coord_utils import center_element
from src.log_handle import get_logger
logger = get_logger(__name__)

class ScreenManager:
    def __init__(self, screen, game_state, all_sprites):
        logger.info("screen manager initializing")
        self._screen = screen
        self._game_state = game_state
        self.all_sprites = all_sprites
        self.loading_screen = LoadingScreen(self._screen)
        self.pacman = PacmanGrid(screen, game_state)
        logger.info("pacman grid created")
        self.all_sprites.add(self.pacman.pacman)
        for ghost in self.pacman.ghost.ghosts_list:
            self.all_sprites.add(ghost)
        logger.info("ghosts created")

    def draw_screens(self):
        self.pacman.ghost.manage_ghosts()
        self.pacman.draw_level()
        
