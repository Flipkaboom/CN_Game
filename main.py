import pygame
import drawing
import events

pygame.init()

pygame.display.set_caption("Don't forget to change this")
clock = pygame.time.Clock()

kill_game:bool = False


player = pygame.Rect((200, 100), (100, 200))

while not kill_game:
    events.handle_pygame_events()

    drawing.render_canvas()

    clock.tick(60)

# noinspection PyUnreachableCode
pygame.quit()