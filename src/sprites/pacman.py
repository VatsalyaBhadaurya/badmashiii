from pygame.sprite import Sprite
from pygame import image, transform
from pygame import draw

from src.sprites.sprite_configs import *
from src.configs import CELL_SIZE, Colors, PACMAN_SPEED
from src.utils.coord_utils import get_idx_from_coords

class Pacman(Sprite):
    def __init__(self, x, y, 
                 width, height,
                 game_state,
                 pacman_pos,
                 start_x,
                 start_y,
                 matrix,
                 screen,
                 coord_matrix,
                 tiny_matrix,
                 frame_rate=5):
        super().__init__()
        self.screen = screen
        self.load_all_frames(width, height)
        self.frames = self.right_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect_x, self.rect_y = x, y
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame_rate = frame_rate
        self.counter = 0
        self.game_state = game_state
        self.xidx, self.yidx = pacman_pos
        self.start_x = start_x
        self.start_y = start_y
        self.matrix = matrix
        self.coord_matrix = coord_matrix
        self.tiny_matrix = tiny_matrix
        self.subdiv = (CELL_SIZE[0] // PACMAN_SPEED)
        self.tiny_start_x = self.xidx * self.subdiv
        self.tiny_start_y = self.yidx * self.subdiv
        self.move_direction = self.game_state.direction

    def build_bounding_box(self, x, y):
        draw.rect(self.screen, Colors.GREEN, 
                  (x, y, CELL_SIZE[0] *2,
                   CELL_SIZE[0] * 2), 1)
        self.rect.x = x + (CELL_SIZE[0] * 2 - self.rect.width) // 2
        self.rect.y = y + (CELL_SIZE[1] * 2 - self.rect.height) // 2
    
    def load_all_frames(self, width, height):
        def frame_helper(direction):
            return [
                transform.scale(
                    image.load(path).convert_alpha(), 
                    (width, height)
                ) 
                for path in PACMAN_PATHS[direction]
            ]
        self.left_frames = frame_helper('left')
        self.right_frames = frame_helper('right')
        self.down_frames = frame_helper("down")
        self.up_frames = frame_helper("up")
        self.direction_mapper = {"l":self.left_frames,
                                 "r":self.right_frames,
                                 "u":self.up_frames,
                                 "d":self.down_frames}

    def frame_update(self):
        self.counter += 1
        if self.counter >= self.frame_rate:
            self.counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]
        self.build_bounding_box(self.rect_x, self.rect_y)
    
    def frame_direction_update(self):
        direc = self.game_state.direction
        if direc != "":
            self.frames = self.direction_mapper[direc]
    
    def move_pacman(self):
        def edges_helper_vertical(row, col, additive):
            for r in range(self.subdiv * 2):
                if self.tiny_matrix[row+r][col + additive] == 'wall':
                    return False
            return True
        
        def edge_helper_horizontal(row, col, additive):
            for c in range(self.subdiv * 2):
                if self.tiny_matrix[row + additive][col + c] == 'wall':
                    return False
            return True
        
        if self.game_state.direction == 'l':
            if edges_helper_vertical(self.tiny_start_x, self.tiny_start_y, -1):
                self.rect_x -= PACMAN_SPEED
                self.tiny_start_y -= 1
        elif self.game_state.direction == 'r':
            if edges_helper_vertical(self.tiny_start_x, self.tiny_start_y, self.subdiv * 2):
                self.rect_x += PACMAN_SPEED
                self.tiny_start_y += 1
        elif self.game_state.direction == 'u':
            if edge_helper_horizontal(self.tiny_start_x, self.tiny_start_y, -1):
                self.rect_y -= PACMAN_SPEED
                self.tiny_start_x -= 1
        elif self.game_state.direction == 'd':
            if edge_helper_horizontal(self.tiny_start_x, self.tiny_start_y, self.subdiv * 2):
                self.rect_y += PACMAN_SPEED
                self.tiny_start_x += 1
        
            
    def update(self):
        self.frame_update()
        self.frame_direction_update()
        self.move_pacman()

