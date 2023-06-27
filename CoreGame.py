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

# Set up the player and obstacle
player = pygame.Rect(WIDTH / 2, HEIGHT - PLAYER_SIZE - 10, PLAYER_SIZE, PLAYER_SIZE)
obstacles = pygame.sprite.Group()

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
                if game_state == "start":
                    game_state = "running"
                elif game_state == "game over":
                    game_state = "start"
                    score = 0
                    player.x = WIDTH / 2
                    obstacles.empty()

    # Game logic
    if game_state == "running":
        # Player movement
        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.x - SPEED > 0:
            player.x -= SPEED
        if keys[pygame.K_RIGHT] and player.x + SPEED < WIDTH - PLAYER_SIZE:
            player.x += SPEED

        # Add new obstacles
        if not obstacles or obstacles.sprites()[-1].rect.y > 20:
            obstacle = pygame.sprite.Sprite()
            obstacle.rect = pygame.Rect(random.randrange(WIDTH - OBSTACLE_WIDTH), -OBSTACLE_HEIGHT, OBSTACLE_WIDTH, OBSTACLE_HEIGHT)
            obstacle.image = pygame.Surface((OBSTACLE_WIDTH, OBSTACLE_HEIGHT))
            obstacle.image.fill(RED)
            obstacles.add(obstacle)

        # Obstacle movement and collision detection
        for obstacle in obstacles:
            obstacle.rect.y += SPEED
            if player.colliderect(obstacle.rect):
                game_state = "game over"
            if obstacle.rect.y > HEIGHT:
                obstacles.remove(obstacle)
                score += 1

    # Drawing
    screen.fill((0, 0, 0))
    if game_state == "start":
        text = FONT.render("Press SPACE to start", True, WHITE)
        screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    elif game_state == "running":
        pygame.draw.rect(screen, WHITE, player)
        obstacles.draw(screen)
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