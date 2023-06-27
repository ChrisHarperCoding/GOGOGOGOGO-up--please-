import pygame
import random

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 800, 600
PLAYER_SIZE = 50
OBSTACLE_WIDTH, OBSTACLE_HEIGHT = 80, 20
SPEED = 5
WHITE = (255, 255, 255)
RED = (255, 0, 0)
FONT = pygame.font.Font(None, 36)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create a list of stars for the starfield effect
stars = []
for _ in range(100):
    x = random.randint(0, WIDTH)
    y = random.randint(0, HEIGHT)
    stars.append([x, y])

# Set up the player and obstacles
player = pygame.Rect(WIDTH / 2, HEIGHT - PLAYER_SIZE - 10, PLAYER_SIZE, PLAYER_SIZE)
obstacles = []

# Set up the clock
clock = pygame.time.Clock()

# Game state
game_state = "start"
score = 0

# Game loop
running = True
while running:
    # Event handling
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                if game_state == "start" or game_state == "game over":
                    game_state = "running"
                    score = 0
                    player = pygame.Rect(WIDTH / 2, HEIGHT - PLAYER_SIZE - 10, PLAYER_SIZE, PLAYER_SIZE)
                    obstacles = []

    # Game logic
    if game_state == "running":
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - SPEED > 0:
            player.x -= SPEED
        if keys[pygame.K_RIGHT] and player.x + SPEED < WIDTH - PLAYER_SIZE:
            player.x += SPEED

        # Add new obstacles
        if len(obstacles) == 0 or obstacles[-1][1] > 20:
            obstacle_x = random.randrange(WIDTH - OBSTACLE_WIDTH)
            obstacles.append([obstacle_x, -OBSTACLE_HEIGHT])

        # Obstacle movement and collision detection
        for obstacle in obstacles:
            obstacle[1] += SPEED
            if player.colliderect(pygame.Rect(obstacle[0], obstacle[1], OBSTACLE_WIDTH, OBSTACLE_HEIGHT)):
                game_state = "game over"
            if obstacle[1] > HEIGHT:
                obstacles.remove(obstacle)
                score += 1

    # Update the starfield
    for star in stars:
        star[1] += SPEED
        if star[1] > HEIGHT:
            star[1] = random.randint(-HEIGHT, 0)

    # Drawing
    # Draw the starfield background
    screen.fill((0, 0, 0))
    for star in stars:
        pygame.draw.circle(screen, WHITE, (star[0], star[1]), 1)

    if game_state == "start":
        text = FONT.render("Press SPACE to start", True, WHITE)
        screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    elif game_state == "running":
        pygame.draw.rect(screen, WHITE, player)
        for obstacle in obstacles:
            pygame.draw.rect(screen, RED, (obstacle[0], obstacle[1], OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
        text = FONT.render(f"Score: {score}", True, WHITE)
        screen.blit(text, (10, 10))
    elif game_state == "game over":
        text = FONT.render(f"Game Over! Score: {score}. Press SPACE to restart", True, WHITE)
        screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))

    # Flip the display
    pygame.display.flip()

    # Cap the frame rate
    clock.tick(60)

# Quit Pygame
pygame.quit()

