import pygame

pygame.init()
screen = pygame.display.set_mode((640, 480))

clock = pygame.time.Clock()
while True:
    clock.tick(60)

    pygame.display.flip()
