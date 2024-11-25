import json

from src.configs import *

class LevelBuilder:
    def __init__(self, screen, 
                 game_state, 
                 level_number,
                 start_x, 
                 start_y):
        self.function_mapper = {
            "void": self.draw_void,
            "wall":self.wall,
            "dot":self.dot,
            "spoint":self.special_point,
            "null":self.draw_void
        }
        self._screen = screen
        self._game_state = game_state
        self._level_number = level_number

    def get_json(self, path):
        with open(path) as fp:
            payload = json.load(fp)
        return payload

    def load_level(self, level_number):
        level_path = f"levels/level{level_number}.json"
        level_json = self.get_json(level_path)
        self._matrix = level_json['matrix']
        self._pacman_pos = level_json['pacman_start']

    def draw_level(self):
        ...
