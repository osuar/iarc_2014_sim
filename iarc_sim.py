import pygame

def meters_to_pixels(meters):
    return int(round(meters * 20))

def draw_arena_boundary(screen, color, (sx, sy), (fx, fy)):
    width = fx - sx
    height = fy - sy
    pygame.draw.rect(screen, color, (sx, sy, width + 5, height + 5))

def draw_arena(screen):
    # Sidelines
    draw_arena_boundary(screen, (255, 255, 255), (0, 0), (0, meters_to_pixels(20)))
    draw_arena_boundary(screen, (255, 255, 255), (meters_to_pixels(20), 0), (meters_to_pixels(20), meters_to_pixels(20)))
    draw_arena_boundary(screen, (255, 255, 255), (0, meters_to_pixels(10)), (meters_to_pixels(20), meters_to_pixels(10)))

    # Top goal line
    draw_arena_boundary(screen, (0, 255, 0), (0, 0), (meters_to_pixels(20), 0))

    # Bottom goal line
    draw_arena_boundary(screen, (255, 0, 0), (0, meters_to_pixels(20)), (meters_to_pixels(20), meters_to_pixels(20)))

def draw_robot(screen, color, (x, y)):
    pygame.draw.circle(screen, color, (x, y), meters_to_pixels(0.33))

pygame.init()
screen = pygame.display.set_mode((meters_to_pixels(20) + 5, meters_to_pixels(20) + 5))

clock = pygame.time.Clock()
while True:
    clock.tick(60)

    draw_arena(screen)
    draw_robot(screen, (0, 0, 255), (meters_to_pixels(11), meters_to_pixels(9)))
    draw_robot(screen, (0, 0, 255), (meters_to_pixels(9),  meters_to_pixels(11)))
    draw_robot(screen, (0, 0, 255), (meters_to_pixels(11), meters_to_pixels(11)))
    draw_robot(screen, (0, 0, 255), (meters_to_pixels(9),  meters_to_pixels(9)))
    draw_robot(screen, (0, 0, 255), (meters_to_pixels(10), meters_to_pixels(9)))
    draw_robot(screen, (0, 0, 255), (meters_to_pixels(9),  meters_to_pixels(10)))
    draw_robot(screen, (0, 0, 255), (meters_to_pixels(10), meters_to_pixels(11)))
    draw_robot(screen, (0, 0, 255), (meters_to_pixels(11), meters_to_pixels(10)))

    pygame.display.flip()
