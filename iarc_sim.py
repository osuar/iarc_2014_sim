import numpy as np
import pygame

class Robot:
    def __init__(self, (x, y)):
        self.pos = np.array([float(x), float(y)])

        self.velocity = np.random.rand(2) - 0.5
        # TODO: robots always travel at 0.33 m/s
        # self.velocity = np.linalg.norm(self.velocity)

    def update(self, tick_length):
        self.pos += self.velocity * tick_length

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

robots = []
for x in range(9, 12):
    for y in range(9, 12):
        if x == 10 and y == 10:
            continue

        robots.append(Robot((x, y)))

clock = pygame.time.Clock()
while True:
    clock.tick(60)
    # TODO: blit background
    screen.fill((0, 0, 0))

    draw_arena(screen)

    for robot in robots:
        robot.update(1.0 / 60.0)

        px, py = meters_to_pixels(robot.pos[0]), meters_to_pixels(robot.pos[1])
        draw_robot(screen, (0, 0, 255), (px, py))

    pygame.display.flip()
