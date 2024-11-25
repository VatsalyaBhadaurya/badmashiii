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