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

def m_to_px(meters):
    return int(round(meters * 20))

def draw_arena_boundary(screen, color, (sx, sy), (fx, fy)):
    width = fx - sx
    height = fy - sy
    pygame.draw.rect(screen, color, (sx, sy, width + 5, height + 5))

def draw_arena(screen):
    # Sidelines
    draw_arena_boundary(screen, (255, 255, 255), (0, 0), (0, m_to_px(20)))
    draw_arena_boundary(screen, (255, 255, 255), (m_to_px(20), 0), (m_to_px(20), m_to_px(20)))
    draw_arena_boundary(screen, (255, 255, 255), (0, m_to_px(10)), (m_to_px(20), m_to_px(10)))

    # Top goal line
    draw_arena_boundary(screen, (0, 255, 0), (0, 0), (m_to_px(20), 0))

    # Bottom goal line
    draw_arena_boundary(screen, (255, 0, 0), (0, m_to_px(20)), (m_to_px(20), m_to_px(20)))

def draw_robot(screen, color, (x, y)):
    pygame.draw.circle(screen, color, (x, y), m_to_px(0.33))

pygame.init()
screen = pygame.display.set_mode((m_to_px(20) + 5, m_to_px(20) + 5))

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

        px, py = m_to_px(robot.pos[0]), m_to_px(robot.pos[1])
        draw_robot(screen, (0, 0, 255), (px, py))

    pygame.display.flip()
