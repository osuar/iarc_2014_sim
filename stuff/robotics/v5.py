####################################
# This algorithm creates a list of 
# robots that are not headed toward 	
# the green line, and selects whichever
# robot is closest to the red line
# and turns that robot in 45 degree
# increments until it is facing the 
# green goal line. 
# The most recently turned robot is
# not in the list of potential new
# targets.
####################################

#TODO IMPLEMENT STOPPING IN FRONT OF ROBOT FOR 180 TURN
#TODO ALSO DO THE ROBOTS REALLY TURN 180 EVEN WHEN THEY HIT 
#	EACH OTHER FROM THE SIDE OR VERY SMALL ANGLES?
#TODO IMPLEMENT MOTION PLANNING TO AVOID THE AVOIDS
import numpy as np
import pygame
import math
import sys
from time import sleep

class Robot:
    def __init__(self, (x, y)):
        self.pos = np.array([float(x), float(y)])

        self.velocity = np.random.rand(2) - 0.5
        #robots always travel at 0.33 m/s
	vmag = math.sqrt(self.velocity[0]**2 + self.velocity[1]**2)
	self.velocity[0] = .33 * self.velocity[0] / vmag
	self.velocity[1] = .33 * self.velocity[1] / vmag
        # self.velocity = np.linalg.norm(self.velocity)

    def update(self, tick_length):
        self.pos += self.velocity * tick_length

class Copter (Robot):
    def pick_target(self, robots):
	#if robot is not headed toward green, then it is a possible target
	possible_targets = []
	for robot in robots:
	    if not is_toward_green(robot):
		possible_targets.append(robot)
	#if all good, then robot return to center
	if possible_targets == []:
            self.target = Robot((10,10))
	    return
	self.target = possible_targets[0]
	for robot in possible_targets:
	    #chose target closest to red line
	    if robot.pos[1] > self.target.pos[1]:
		if robot.velocity[1] > 0:
               	    self.target = robot

    def update(self, tick_length):
	#change velocity to be in direction of target, but have the same magnitude (speed)
	direction = [self.target.pos[0] - self.pos[0], self.target.pos[1] - self.pos[1]]
	dir_mag = math.sqrt(direction[0]**2 + direction[1]**2)
	self.velocity[0] = direction[0] / dir_mag
	self.velocity[1] = direction[1] / dir_mag
	#move
	self.pos += self.velocity * tick_length

class Avoid (Robot):
    #avoid robots move in a circle
    def update(self, tick_length):
        #rotate by rot degrees
        rot = math.pi / 720.0
        #rotate velocity vectors
        vx = self.velocity[0]
	vy = self.velocity[1]
	self.velocity[0] = vx * math.cos(rot) - vy * math.sin(rot)
	self.velocity[1] = vx * math.sin(rot) + vy * math.cos(rot)
	#move
        self.pos += self.velocity * tick_length

def m_to_px(meters):
    return int(round(meters * 20))

def is_toward_green(robot):
    if robot.velocity[1] > 0:
	return False
    # y=mx+b
    m = 0.0 - robot.velocity[1] / robot.velocity[0]
    b = 0.0 - robot.pos[1] - (m * robot.pos[0])
    x_intercept = 0.0 - b / m
    #if 0 < x-intercept < 20 then it is headed toward green
    if x_intercept > 0 and x_intercept < 20:
	return True
    return False

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

#turns the robot by increments of 45 degrees until towards green
def turn_toward_green(robot):
    while not is_toward_green(robot):
        x = robot.velocity[0]
        y = robot.velocity[1]
        robot.velocity[0] = (x - y) / math.sqrt(2)
        robot.velocity[1] = (x + y) / math.sqrt(2)

def robot_is_hit(copter, robot):
    if(abs(copter.pos[0] - robot.pos[0]) < .1 and abs(copter.pos[1] - robot.pos[1]) < .1):
	return True
    else:
	 return False

def robot_is_out(robot, score):
    if robot.pos[1] < 0:
	score[0] += 1
	print(score[0])
	return True
    if robot.pos[0] < 0 or robot.pos[0] > 20:
	return True
    if robot.pos[1] > 20:
	score[0] -= 1
	print(score[0])
	return True 
    return False

def distance_apart(robot1, robot2):
    return math.sqrt( (robot1.pos[0] - robot2.pos[0])**2 + (robot1.pos[1] - robot2.pos[1])**2 )

#turns both robots around 180 degrees
def hit_so_turn180(robot1, robot2):
    robot1.velocity[0] = 0.0 - robot1.velocity[0]
    robot1.velocity[1] = 0.0 - robot1.velocity[1]
    robot2.velocity[0] = 0.0 - robot2.velocity[0]
    robot2.velocity[1] = 0.0 - robot2.velocity[1]
    robot1.update(1.0 / 60)
    robot2.update(1.0 / 60)

#checks if any of the robots have colided
def check_hit(robots):
    for robot1 in robots:
	for robot2 in robots:
	    if robot1 != robot2:
		if distance_apart(robot1, robot2) < (2.0 * .33):
		    hit_so_turn180(robot1, robot2)

def game_over():
    print("GAME OVER MAN!!!")
    sys.exit()

#checks if robots hit an avoids or if frank hits an avoids
def check_hit_avoids(frank, robots, avoids):
    for robot in robots:
        for avoid in avoids:
	    if distance_apart(robot, avoid) < (2.0 * .33):
	        hit_so_turn180(avoid, robot)

    for avoid in avoids:
        if distance_apart(avoid, frank) < (2.0 * .33):
	    print("frank hit an avoid")
	    game_over()

pygame.init()
screen = pygame.display.set_mode((m_to_px(20) + 5, m_to_px(20) + 5))

robots = []
avoids = []
score = [0]
frank = Copter((2,2))
for x in range(9, 12):
    for y in range(9, 12):
        if x == 10 and y == 10:
            continue
        robots.append(Robot((x, y)))

for x in range(0,4):
    avoids.append(Avoid((15.0 * np.random.rand(2) + 2.5)))

frank.pick_target(robots)

clock = pygame.time.Clock()
while len(robots) > 0:
    clock.tick(60)
    # TODO: blit background
    screen.fill((0, 0, 0))

    draw_arena(screen)

    check_hit(robots)

    check_hit_avoids(frank, robots, avoids)

    for robot in robots:
        robot.update(1.0 / 60.0)

        px, py = m_to_px(robot.pos[0]), m_to_px(robot.pos[1])
        draw_robot(screen, (0, 0, 255), (px, py))
	if robot_is_out(robot, score):
	    robots.remove(robot)

    #DRAW FRANK - CHANGED FOR TESTING; SHOULD BE 1.0
    frank.update(2.0 / 60.0)
    draw_robot(screen, (255, 255, 255), (m_to_px(frank.pos[0]), m_to_px(frank.pos[1])))   
    
    #DRAW AVOID
    for avoid in avoids:
        avoid.update(1.0 / 60.0)
	px, py = m_to_px(avoid.pos[0]), m_to_px(avoid.pos[1])
	draw_robot(screen, (255, 0, 0), (px, py))
    

    if robot_is_hit(frank, frank.target):
    	turn_toward_green(frank.target)

    frank.pick_target(robots)
	

    pygame.display.flip()

print(score[0])
print("\n")
