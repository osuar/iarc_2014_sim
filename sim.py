###################################
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
import sys
import time
import math

SPEED_FACTOR = 3
hits_log = []
avoid_hits_log = []

class Hit(object):
    def __init__(self):
        robot1 = None
        robot2 = None

class Robot(object):
    SPEED = 0.33

    def __init__(self, (x, y)):
        self.init_pos = np.array([float(x), float(y)])
	self.init_time = time.clock()
	self.pos = self.init_pos
        self.velocity = np.random.rand(2) - 0.5

        # Normalize robot velocity to 0.33 m/s
        self.velocity = self.velocity / np.linalg.norm(self.velocity) * self.SPEED

    def update(self, tick_length):
	t = (time.clock() - self.init_time) * SPEED_FACTOR
	self.pos = [self.velocity[0]*t + self.init_pos[0] ,
	            self.velocity[1]*t + self.init_pos[1] ]

class Copter(Robot):
    SPEED = 1.0

    def pick_target(self, robots):
        #if robot is not headed toward green, then it is a possible target
        possible_targets = []
        for robot in robots:
            if not is_toward_green(robot):
                possible_targets.append(robot)

        #if all good, then robot return to center
        if possible_targets == []:
            self.target = Robot((10,10))
        else:
	    self.target = possible_targets[0]
            for robot in possible_targets:
                #chose target closest to red line
                if robot.pos[1] > self.target.pos[1]:
                    if robot.velocity[1] > 0:
                        self.target = robot
        # Change velocity to be in direction of target, but have the same magnitude (speed)
        direction = [self.target.pos[0] - self.pos[0] , 
	      	     self.target.pos[1] - self.pos[1] ]
        self.velocity = direction / np.linalg.norm(direction) * np.linalg.norm(self.velocity)
	self.init_time = time.clock()
	self.init_pos = self.pos
	
	
    def update(self, tick_length):
	#TODO TODO TODO To implement path planning, replace this function call with a call to something
	# more complicated (obviously). One idea is to check if frank will hit an avoid, and if so, change
	# his path to the following:
	# ave ctor function most likely of the form r(t) = <vx*t-rcos(at), vy*t-rsin(at)> + init position
	# this will cause a path that is a cosine wave undereath the normal path. Note more constants will 
	# be needed to calculated and added in order to flatted the wave, and to make sure the ending of the 
	# wave is at the target robot.
	# Also, come to think of it, you could just go in a line in a slightly different direction for a while
	# until you are no longer going to get hit. Then return to the target. Although this wouldn't be quite
	# as smooth, it would probably work just as well and be easier to implemennt. 
        super(Copter, self).update(tick_length)

class Avoid(Robot):
    SPEED = 0.33 #m/s
    RADIUS = 4 #meters
    # Avoid robots move in a circle
    def update(self, tick_length):
	a = self.SPEED / self.RADIUS
	t = (time.clock() - self.init_time) * SPEED_FACTOR
	self.pos = [self.RADIUS * math.cos(a*t) + self.init_pos[0] , 
	      	    self.RADIUS * math.sin(a*t) + self.init_pos[1] ]

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
        robot.velocity[0] = (x - y) / np.sqrt(2)
        robot.velocity[1] = (x + y) / np.sqrt(2)
	robot.init_time = time.clock()
	robot.init_pos = robot.pos


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
    return np.sqrt( (robot1.pos[0] - robot2.pos[0])**2 + (robot1.pos[1] - robot2.pos[1])**2 )

#turns both robots around 180 degrees
def hit_so_turn180(robot1, robot2):
    t = time.clock()
    robot1.velocity[0] = 0.0 - robot1.velocity[0]
    robot1.velocity[1] = 0.0 - robot1.velocity[1]
    robot1.init_time = t
    robot1.init_pos = robot1.pos

    robot2.velocity[0] = 0.0 - robot2.velocity[0]
    robot2.velocity[1] = 0.0 - robot2.velocity[1]
    robot2.init_time = time.clock()
    robot2.init_pos = robot2.pos

def already_logged(robot1, robot2):
    for hit in hits_log:
	if(robot1 == hit.robot1 or robot1 == hit.robot2):
	    if(robot2 == hit.robot1 or robot2 == hit.robot2):
		return True
    return False

def log_hit(robot1, robot2):
    h = Hit()
    h.robot1 = robot1
    h.robot2 = robot2
    hits_log.append(h)

#checks if any of the robots have colided
def check_hit(robots):
    for robot1 in robots:
        for robot2 in robots:
            if robot1 != robot2:
                if distance_apart(robot1, robot2) < (2.0 * .33):
		    if not already_logged(robot1, robot2):
		        log_hit(robot1, robot2)
                        hit_so_turn180(robot1, robot2)


def game_over():
    print("GAME OVER MAN!!!")
    pygame.event.post(pygame.event.Event(pygame.QUIT, {}))

def hit_avoid_so_turn_180(robot):
    t = time.clock()
    robot.velocity[0] = 0.0 - robot.velocity[0]
    robot.velocity[1] = 0.0 - robot.velocity[1]
    robot.init_time = t
    robot.init_pos = robot.pos

def already_logged_avoid(robot, avoid):
    for hit in hits_log:
	if(robot == hit.robot1):
	    if(avoid == hit.robot2):
		return True
    return False

def log_hit_avoid(robot, avoid):
    h = Hit()
    h.robot1 = robot
    h.robot2 = avoid
    hits_log.append(h)



#checks if robots hit an avoids or if frank hits an avoids
def check_hit_avoids(frank, robots, avoids):
    for robot in robots:
        for avoid in avoids:
            if distance_apart(robot, avoid) < (2.0 * .33):
	        if not already_logged_avoid(robot, avoid):
		    log_hit_avoid(robot, avoid)
                    hit_avoid_so_turn_180(robot)

    for avoid in avoids:
        if distance_apart(avoid, frank) < (2.0 * .33):
            print("frank hit an avoid")
            game_over()

def still_active(hit):
    if distance_apart(hit.robot1, hit.robot2) >= (2.0 * .33):
	return False
    return True

def update_logs():
    for hit in hits_log:
        if not still_active(hit):
	    hits_log.remove(hit)

    for hit in avoid_hits_log:
	if not still_active(hit):
	    hits_log_avoid.remove(hit)


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
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

    update_logs()

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
