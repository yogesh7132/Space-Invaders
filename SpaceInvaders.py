import pygame

pygame.init()
screen = pygame.display.set_mode((800,600))

running = True
## Main Loop of Game
while running:
    for event in pygame.event.get():
        print(event)
        if event.type == pygame.QUIT:

            running = False