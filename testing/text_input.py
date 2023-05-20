import pygame

pygame.init()
screen = pygame.display.set_mode((1280, 720))
clock = pygame.time.Clock()
running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.TEXTINPUT:
            print(event.dict)
        if event.type == pygame.TEXTEDITING:
            print(event.dict)
        if event.type == pygame.KEYDOWN:
            print(event.dict)

    screen.fill("purple")

    # RENDER YOUR GAME HERE

    pygame.display.flip()

    clock.tick(60)

pygame.quit()