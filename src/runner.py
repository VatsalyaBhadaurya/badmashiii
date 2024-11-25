import pygame
import sys

from src.configs import *
from src.game.state_management import GameState
from src.game.event_management import EventHandler

from src.gui.screen_management import ScreenManager

class GameRun:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Py-Pacman")
        self.game_state = GameState()
        self.events =  EventHandler(self.screen, self.game_state)
        self.gui = ScreenManager(self.screen, self.game_state)

    def main(self):
        clock = pygame.time.Clock()
        while self.game_state.running:
            for event in pygame.event.get():
                self.events.handle_events(event)
            self.screen.fill(Colors.BLACK)
            self.gui.draw_screens()
            pygame.display.flip()
            clock.tick(self.game_state.fps)
        pygame.quit()
        sys.exit()

        

        
