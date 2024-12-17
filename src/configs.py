class Colors:
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    GREEN = (0, 255, 0)
    BLUE = (0, 0, 255)
    WALL = (112, 167, 255)
    YELLOW = (252, 186, 3)


SCREEN_WIDTH = 1024
SCREEN_HEIGHT = 768
CELL_SIZE = (20, 20)
NUM_ROWS = 31
NUM_COLS = 28
PACMAN = (32, 32)
GHOSTS = (32, 32)
PACMAN_SPEED = 5
GHOST_SPEED_FAST = 5
GHOST_SPEED_SLOW = 2

GHOST_DELAYS = {
    "inky": 12000,
    "pinky": 8000,
    "blinky": 4000,
    "clyde": 16000,
    "blue": 0
}
GHOST_TARGET_CHANGE = {
    "inky": 10,
    "pinky": 8,
    "blinky": 6,
    "clyde": 7,
    "blue": 7
}
loading_screen_gif = "assets/other/loading.gif"