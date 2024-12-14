from pygame.sprite import Sprite
from pygame import image, transform, draw
from pygame import time as pytime

from src.configs import *
from src.utils.coord_utils import (get_coords_from_idx, 
                                   get_tiny_matrix, 
                                   get_movable_locations,
                                   is_any_wall)
from src.utils.graph_utils import a_star
from src.sprites.sprite_configs import GHOST_PATHS

import random

class Ghost(Sprite):
    def __init__(self,
                 name: str,
                 ghost_pos: dict,
                 start_x: float,
                 start_y: float,
                 tiny_matrix_fast: list[list],
                 tiny_matrix_slow: list[list],
                 screen,
                 game_state,
                 paths=None,
                 frame_rate: int=5,
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
        self.mode = 'chase'
        self.released = False
        self.anim_jump = -self.speed
        self.start_time = pytime.get_ticks()
        self.game_state = game_state
        self.paths = paths
        self.xidx = None
        self.yidx = None
        self.curr_idx = 0

    def release_ghost(self, pos):
        self.released = True
        x, y = pos
        self.xidx = x
        self.yidx = y

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

    def animate_den(self):
        if self.released:
            return
        if self.frame_rate == 0:
            self.rect.y += self.anim_jump
            self.anim_jump = -self.anim_jump
            self.frame_rate = 1
            return
        if self.frame_rate == 1:
            self.rect.y += self.anim_jump
            self.anim_jump = -self.anim_jump
            self.frame_rate = 10
        self.frame_rate -= 1

    def is_movable(self, current_time):
        if not self.released:
            return False
        self.frame_rate -= 1
        if not self.paths:
            return True
        if self.target == (self.xidx, self.yidx):
            return True
        return False

    def set_paths(self, movables):
        target = random.choice(movables)
        start = (self.xidx, self.yidx)
        self.paths = a_star(self.tiny_matrix_fast, start, target)
        self.curr_idx = 0
        self.target = target

    def move_ghost(self):
        if not self.released:
            return
        if not self.paths or self.curr_idx >= len(self.paths) or \
                self.curr_idx < 0:
            return
        pos = self.paths[self.curr_idx]
        x, y = pos
        xcoord, ycoord = get_coords_from_idx((x, y),
                                         self.start_x,
                                         self.start_y,
                                         self.speed,
                                         self.speed,
                                         len(self.tiny_matrix_fast),
                                         len(self.tiny_matrix_fast[0]))
        self.ghost_x = xcoord
        self.ghost_y = ycoord
        draw.rect(self.screen, Colors.RED, (xcoord, ycoord, 5,5))
        self.xidx = x
        self.yidx = y
        self.curr_idx += 1

    def path_finding(self, movables):
        pass

    def update(self):
        self.draw_ghost()
        self.animate_den()
        self.move_ghost()

class Blinky(Ghost):
    def __init__(self, ghost_pos: dict, start_x: float, 
                 start_y: float, tiny_matrix_fast, tiny_matrix_slow,
                 screen, game_state, frame_rate: int = 1):
        super().__init__("blinky", ghost_pos, start_x, start_y, 
                         tiny_matrix_fast, 
                         tiny_matrix_slow, screen, 
                         game_state, frame_rate=frame_rate)
        self.release_delay = GHOST_DELAYS['blinky']
        self.release_time = self.release_delay + self.start_time
        self.target_change_delay = self.release_time + GHOST_TARGET_CHANGE['blinky']

    def path_finding(self, movables):
        ...
            

class Inky(Ghost):
    def __init__(self, ghost_pos: dict, start_x: float, 
                 start_y: float, tiny_matrix_fast, tiny_matrix_slow,
                 screen, game_state, frame_rate: int = 10):
        super().__init__("inky", ghost_pos, start_x, start_y, 
                         tiny_matrix_fast, 
                         tiny_matrix_slow, 
                         screen, game_state, frame_rate=frame_rate,
                        )
        self.release_delay = GHOST_DELAYS['inky']
        self.release_time = self.release_delay + self.start_time
        self.target_change_delay = self.release_time + GHOST_TARGET_CHANGE['inky']

    def path_finding(self, movables):
        ...

class Pinky(Ghost):
    def __init__(self, ghost_pos: dict, start_x: float, 
                 start_y: float, tiny_matrix_fast, tiny_matrix_slow,
                 screen, game_state, frame_rate: int = 4):
        super().__init__("pinky", ghost_pos, start_x, start_y, 
                         tiny_matrix_fast, 
                         tiny_matrix_slow, screen, 
                         game_state, frame_rate=frame_rate,
                         )
        self.release_delay = GHOST_DELAYS['pinky']
        self.release_time = self.release_delay + self.start_time
        self.target_change_delay = self.release_time + GHOST_TARGET_CHANGE['pinky']

    def path_finding(self, movables):
        ...

class Clyde(Ghost):
    def __init__(self, ghost_pos: dict, start_x: float, 
                 start_y: float, tiny_matrix_fast, tiny_matrix_slow,
                 screen, game_state, frame_rate: int = 0):
        super().__init__("clyde", ghost_pos, start_x, start_y, 
                         tiny_matrix_fast, tiny_matrix_slow, 
                         screen, game_state, frame_rate=frame_rate,
                         )
        self.release_delay = GHOST_DELAYS['clyde']
        self.release_time = self.release_delay + self.start_time
        self.target_change_delay = self.release_time + GHOST_TARGET_CHANGE['clyde']

    def path_finding(self, movables):
        ...

class GhostManager:
    def __init__(self,
                 ghost_pos: dict,
                 start_x: float,
                 start_y: float,
                 matrix: list[list],
                 elec_pos: list,
                 game_state,
                 screen):
        self.matrix = matrix
        self.game_state = game_state
        self.start_x = start_x
        self.start_y = start_y
        self.screen = screen
        self.orig_ghost_pos = ghost_pos
        self.tiny_matrix_loader()
        self.load_ghosts()
        self.elec_pos = [elec_pos[0] *  (CELL_SIZE[0] // GHOST_SPEED_FAST),
                         elec_pos[1] *  (CELL_SIZE[0] // GHOST_SPEED_FAST)]

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
                                self.matrix_2px, 
                                self.screen, 
                                self.game_state)
            self.ghosts_list.append(ghost_obj)
            curr_pad += 5
    
    def monitor_ghosts(self):
        for ghost in self.ghosts_list:
            if (not ghost.released) and \
                    (self.game_state.current_time >= ghost.release_time):
                ghost.release_ghost(self.elec_pos)
                elec_cords = get_coords_from_idx(self.elec_pos,
                                                 self.start_x,
                                                 self.start_y,
                                                 GHOST_SPEED_FAST,
                                                 GHOST_SPEED_FAST,
                                                 len(self.matrix_5px),
                                                 len(self.matrix_5px[0]))
                ghost.ghost_x = elec_cords[0]
                ghost.ghost_y = elec_cords[1]
    
    def prepare_ghosts(self):
        for ghost in self.ghosts_list:
            if not ghost.released:
                continue
            if ghost.is_movable(self.game_state.current_time):
                ghost.set_paths(self.movables_5px)
    
    def manage_ghosts(self):
        self.monitor_ghosts()
        self.prepare_ghosts()

    def tiny_matrix_loader(self):
        self.matrix_5px = get_tiny_matrix(self.matrix, CELL_SIZE[0], GHOST_SPEED_FAST)
        self.matrix_2px = get_tiny_matrix(self.matrix, CELL_SIZE[0], GHOST_SPEED_SLOW)
        self.movables_5px = get_movable_locations(self.matrix_5px, 
                                                  max_cell_size=CELL_SIZE[0],
                                                  cell_size=GHOST_SPEED_FAST)
        self.movables_2px = get_movable_locations(self.matrix_2px,
                                                  max_cell_size=CELL_SIZE[0],
                                                  cell_size=GHOST_SPEED_SLOW)
