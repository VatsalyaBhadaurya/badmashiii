from pygame import draw

def draw_rect(x, y, w, h, screen, color, fill=0):
    draw.rect(screen, color, (x, y, w, h), fill)

def draw_circle(x, y, radius, screen, color):
    draw.circle(screen, color, (x, y), radius)