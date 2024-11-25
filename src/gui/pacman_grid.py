from src.configs import *
from pygame import draw
from src.utils.coord_utils import place_elements_offset, get_coords_from_idx
from src.utils.draw_utils import draw_rect, draw_circle
from src.sprites.pacman import Pacman

import json

class PacmanGrid:
    def __init__(self, screen, 
                 game_state):
        self.function_mapper = {
            "void": self.draw_void,
            "wall":self.draw_wall,
            "dot":self.draw_dot,
            "spoint":self.draw_special_point,
            "power":self.draw_power,
            "null":self.draw_void,
            "elec": self.draw_elec
        }
        self._screen = screen
        self._game_state = game_state
        self._level_number = self._game_state.level
        self.load_level(self._level_number)
        self.pacman = Pacman(self.pacman_x, 
                             self.pacman_y,
                             PACMAN[0],
                             PACMAN[1],
                             game_state,
                             self._pacman_pos,
                             self.start_x,
                             self.start_y,
                             self._matrix)

    def get_json(self, path):
        with open(path) as fp:
            payload = json.load(fp)
        return payload

    def load_level(self, level_number):
        level_path = f"levels/level{level_number}.json"
        level_json = self.get_json(level_path)
        num_rows = level_json['num_rows']
        num_cols = level_json['num_cols']
        self._matrix = level_json['matrix']
        # self._matrix[-9][15] = "power"
        self._pacman_pos = level_json['pacman_start']
        self.start_x, self.start_y = place_elements_offset(SCREEN_WIDTH,
                                                    SCREEN_HEIGHT,
                                                    CELL_SIZE[0]*num_cols,
                                                    CELL_SIZE[0]*num_rows,
                                                    0.15, 0.5)
        self.pacman_x, self.pacman_y = get_coords_from_idx(self._pacman_pos,
                                                           self.start_x, self.start_y,
                                                           CELL_SIZE[0], CELL_SIZE[1],
                                                           num_rows, num_cols,
                                                           )
        self.num_rows = num_rows
        self.num_cols = num_cols

    def draw_void(self, **kwargs):
        ...

    def draw_wall(self, **kwargs):
        draw_rect(kwargs['x'], 
                   kwargs['y'], 
                   kwargs['w'], 
                   kwargs['h'], self._screen, Colors.WALL)

    def draw_dot(self, **kwargs):
        dot_x = kwargs['x'] + kwargs['w']
        dot_y = kwargs['y'] + kwargs['h']
        draw_rect(dot_x, dot_y, 5, 
                  5, self._screen, Colors.WHITE)
    
    def draw_special_point(self):
        ...

    def draw_power(self, **kwargs):
        circle_x = kwargs['x'] + kwargs['w']
        circle_y = kwargs['y'] + kwargs['h']
        draw_circle(circle_x, circle_y, 
                    7, self._screen, Colors.YELLOW)
    
    def draw_elec(self, **kwargs):
        draw_rect(kwargs['x'], 
                  kwargs['y'], kwargs['w'], 
                  1, self._screen, Colors.RED)

    def draw_level(self):
        curr_x, curr_y = self.start_x, self.start_y
        for _, row in enumerate(self._matrix):
            for _, col in enumerate(row):
                draw_func = self.function_mapper[col]
                draw_func(x=curr_x, 
                          y=curr_y, 
                          w=CELL_SIZE[0],
                          h=CELL_SIZE[0])
                curr_x += CELL_SIZE[0]
            curr_x = self.start_x
            curr_y += CELL_SIZE[0]

    def draw_outliners(self):
        curr_x, curr_y = self.start_x, self.start_y
        for _ in range(self.num_rows):
            for _ in range(self.num_cols):
                draw.rect(self._screen, Colors.BLUE, 
                          (curr_x, curr_y, 
                           CELL_SIZE[0], 
                           CELL_SIZE[1]),
                            width=1)
                curr_x += CELL_SIZE[0]
            curr_y += CELL_SIZE[0]
            curr_x = self.start_x

    