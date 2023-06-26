#python3 -m pip install pygame
#Copyright - ChrisHarperCoding

import pygame
import random

# Initialize Pygame
pygame.init()

# Set the dimensions of the game window
win_height = 600
win_width = 400
win = pygame.display.set_mode((win_width, win_height))

# Define the player object
class Player(object):
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = 5

    def draw(self, win):
        pygame.draw.rect(win, (255, 0, 0), (self.x, self.y, self.width, self.height))

# Define the obstacle object
class Obstacle(object):
    def __init__(self, x, y, width, height, vel):
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.vel = vel

    def draw(self, win):
        pygame.draw.rect(win, (0, 255, 0), (self.x, self.y, self.width, self.height))

    def move(self):
        self.y += self.vel

# Function to redraw the game window
def redraw_window():
    win.fill((0, 0, 0))
    player.draw(win)
    for obstacle in obstacles:
        obstacle.draw(win)
    pygame.display.update()

# Create player object
player = Player(200, 530, 40, 60)

# Create obstacles
obstacles = []
for i in range(5):
    obstacles.append(Obstacle(random.randint(0, win_width-50), random.randint(-i*150, -50), 50, 50, 2))

# Main game loop
run = True
while run:
    pygame.time.delay(100)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    for obstacle in obstacles:
        obstacle.move()
        if obstacle.y > win_height:
            obstacles.pop(obstacles.index(obstacle))
            obstacles.append(Obstacle(random.randint(0, win_width-50), -50, 50, 50, 2))
        if player.y < obstacle.y + obstacle.height:
            if player.x > obstacle.x and player.x < obstacle.x + obstacle.width or player.x + player.width > obstacle.x and player.x + player.width < obstacle.x + obstacle.width:
                run = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_LEFT] and player.x - player.vel > 0:
        player.x -= player.vel
    if keys[pygame.K_RIGHT] and player.x + player.vel < win_width - player.width:
        player.x += player.vel
    if keys[pygame.K_UP] and player.y - player.vel > 0:
        player.y -= player.vel
    if keys[pygame.K_DOWN] and player.y + player.vel < win_height - player.height:
        player.y += player.vel

    redraw_window()

pygame.quit()

