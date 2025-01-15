import math


def get_lerp(curr_pos: tuple[float, float],
             target_pos: tuple[float, float],
             t: float,
             velocity: float):
    if t < 1:
        t += velocity
    else:
        t = 1
    x = (1 - t) * curr_pos[0] + t * target_pos[0]
    y = (1 - t) * curr_pos[1] + t * target_pos[1]
    return x, y

def eucliad_distance(point1, point2):
    return math.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

def get_direction(ghost_matrix_pos: tuple[int, int],
                target_matrix_pos: tuple[int, int],
                matrix: list[list[str]],
                prev: tuple[int, int]):
    g1, g2 = ghost_matrix_pos
    t1, t2 = target_matrix_pos
    num_rows, num_cols = len(matrix), len(matrix[0])
    directions = ['up', 'left', 'down',' right']
    blockers = ['wall', 'elec']
    curr_min = float('-inf')
    target_dir = None
    for direction in directions:
        coord_check = None
        match direction:
            case "right":
                if (g1 + 2 < num_cols) and \
                        (matrix[g1 + 2] not in blockers):
                    coord_check = (g1 + 1, g2)
            case "left":
                if (g1 - 1 >= 0) and \
                        (matrix[g1 - 1] not in blockers):
                    coord_check = (g1 - 1, g2)
            case "up":
                if(g2 - 1 >= 0) and \
                        (matrix[g2 - 1] not in blockers):
                    coord_check = (g1, g2 - 1)
            case "down":
                if (g2 + 2 < num_rows) and \
                        (matrix[g2 + 2] not in blockers):
                    coord_check = (g1, g2 + 1)
        if coord_check == prev:
            continue   
        distance = eucliad_distance(coord_check, (t1, t2))
        if distance < curr_min:
            curr_min = distance
            target_dir = direction
    if target_dir is None:
        raise ValueError("Oh my god, the ghost is stuck, The game crashed.")
    return target_dir

def is_intersection(ghost_pos: tuple[int, int], matrix: list[list[str]]) -> bool:
    curr_moves = 0
    p1, p2 = ghost_pos
    directions = ((-1, 0),
                  (2, 0),
                  (0, -1),
                  (0, 2))
    for direction in directions:
        t1, t2 = direction
        if matrix[p1 + t1][p2 + t2] not in ['wall', 'elec']:
            curr_moves += 1

    return curr_moves >= 2