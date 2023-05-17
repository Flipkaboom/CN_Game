import pygame


RESOLUTION_DEFAULT = (1920, 1080)

screen = pygame.display.set_mode((1280, 720), pygame.RESIZABLE)

canvas = pygame.Surface(RESOLUTION_DEFAULT)

hor_offset = 0
vert_offset = 0
scale_factor = 1

# def draw_scaled(surf:pygame.Rect, pos:tuple[int, int]):
#     pos = (pos[0] + hor_offset, pos[1] + vert_offset)
#     surf = pygame.transform.smoothscale_by(surf, scale_factor)
#     screen.fill('blue', surf)
#     screen.blit()
#     screen.fill(surf.)

def render_canvas():
    screen.fill('black')

    #start testing code
    canvas.fill('pink')
    canvas.fill('blue', pygame.Rect((200, 100), (100, 200)))
    #end testing code

    canvas_scaled = pygame.transform.smoothscale_by(canvas, scale_factor)
    screen.blit(canvas_scaled, (hor_offset, vert_offset))

    pygame.display.flip()

def update_screen_size():
    global hor_offset, vert_offset, scale_factor
    hor_scale_factor = screen.get_width() / RESOLUTION_DEFAULT[0]
    vert_scale_factor = screen.get_height() / RESOLUTION_DEFAULT[1]
    if hor_scale_factor < vert_scale_factor:
        scale_factor = hor_scale_factor
        proportional_height = scale_factor * RESOLUTION_DEFAULT[1]
        hor_offset = 0
        vert_offset = (screen.get_height() - proportional_height) / 2
    else:
        scale_factor = vert_scale_factor
        proportional_width = scale_factor * RESOLUTION_DEFAULT[0]
        vert_offset = 0
        hor_offset = (screen.get_width() - proportional_width) / 2