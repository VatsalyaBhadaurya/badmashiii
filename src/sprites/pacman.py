from pygame.sprite import Sprite
from pygame import image, transform

from src.sprites.sprite_configs import *
from src.configs import PACMAN_SPEED, CELL_SIZE
from src.utils.coord_utils import get_idx_from_coords

class Pacman(Sprite):
    def __init__(self, x, y, 
                 width, height,
                 game_state,
                 pacman_pos,
                 start_x,
                 start_y,
                 matrix,
                 frame_rate=5):
        super().__init__()
        self.load_all_frames(width, height)
        self.frames = self.right_frames
        self.current_frame = 0
        self.image = self.frames[self.current_frame]
        self.rect = self.image.get_rect(topleft=(x, y))
        self.frame_rate = frame_rate
        self.counter = 0
        self.game_state = game_state
        self.xidx, self.yidx = pacman_pos
        self.start_x = start_x
        self.start_y = start_y
        self.matrix = matrix
    
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

    def frame_update(self):
        self.counter += 1
        if self.counter >= self.frame_rate:
            self.counter = 0
            self.current_frame = (self.current_frame + 1) % len(self.frames)
            self.image = self.frames[self.current_frame]

    def frame_direction_handler(self):
        if self.game_state.direction == 'l':
            if self.frames != self.left_frames:
                self.frames = self.left_frames
        if self.game_state.direction == 'r':
            if self.frames != self.right_frames:
                self.frames = self.right_frames
        if self.game_state.direction == 'u':
            if self.frames != self.up_frames:
                self.frames = self.up_frames
        if self.game_state.direction == 'd':
            if self.frames != self.down_frames:
                self.frames = self.down_frames
    
    def move_pacman(self):
        x_pos, y_pos = get_idx_from_coords(self.rect.x, 
                                           self.rect.y, 
                                           self.start_x,
                                           self.start_y,
                                           CELL_SIZE[0])
        if self.game_state.direction == 'r':
            if self.matrix[y_pos][x_pos + 2] not in ['wall', 'null']: #confusing
                self.rect.x += PACMAN_SPEED
        elif self.game_state.direction == 'l':
            if self.matrix[y_pos][x_pos ] not in ['wall', 'null']: #confusing
                self.rect.x -= PACMAN_SPEED
        elif self.game_state.direction == 'u':
            if self.matrix[y_pos][x_pos] not in ['wall', 'null']: #confusing
                self.rect.y -= PACMAN_SPEED
        elif self.game_state.direction == 'd':
            if self.matrix[y_pos + 2][x_pos] not in ['wall', 'null']: #confusing
                self.rect.y += PACMAN_SPEED

    def update(self):
        self.frame_update()
        self.frame_direction_handler()
        self.move_pacman()

