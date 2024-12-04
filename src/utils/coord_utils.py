def center_element(screen_width,
                   screen_height,
                   element_width,
                   element_height):
    return place_elements_offset(screen_width,
                   screen_height,
                   element_width,
                   element_height, 0.5, 0.6)

def place_elements_offset(screen_width,
                          screen_height,
                          element_width,
                          element_height,
                          xoffset,
                          yoffset):
    x = (screen_width - element_width) * xoffset
    y = (screen_height - element_height) * yoffset
    return x, y


def __get_x_y(pos, num_rows, num_cols):
    x = pos[0]
    y = pos[1]
    if pos[0] < 0:
        x = num_rows + x
    if pos[1] < 0:
        y = num_cols + y
    return x, y

def get_coords_from_idx(pacman_pos, 
                        start_x, 
                        start_y, 
                        cell_w, cell_h,
                        num_rows,
                        num_cols):
    x, y = __get_x_y(pacman_pos, num_rows, num_cols)
    x_coord = start_x + (y * cell_w)
    y_coord = start_y + (x * cell_h)
    return x_coord, y_coord

def precompute_matrix_coords(start_x, start_y,
                             cell_size,
                             num_rows, num_cols):
    matrix_coords = []
    col_start = start_y
    for _ in range(num_rows):
        row_start = start_x
        m = []
        for _ in range(num_cols):
            m.append([row_start, col_start])
            row_start += cell_size
        col_start += cell_size
        matrix_coords.append(m)
    return matrix_coords

def get_idx_from_coords(x_coord, 
                        y_coord, 
                        start_x,
                        start_y,
                        cell_size):
    x_pos = int((x_coord - start_x) // cell_size)
    y_pos = int((y_coord - start_y) // cell_size)
    return y_pos, x_pos #in matrix, horizontal is columns and vertical are rows

