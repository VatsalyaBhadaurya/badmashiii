from pygame import QUIT

class EventHandler:
    def __init__(self, screen, game_state):
        self._screen = screen
        self._game_screen = game_state

    def pygame_quit(self):
        self._game_screen.running = False

    def handle_events(self, event):
        if event.type == QUIT:
            self.pygame_quit()