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
powerups = pygame.sprite.Group()  # Create a group to store power-ups

# Set up the clock
clock = pygame.time.Clock()

# Game state
game_state = "start"
score = 0

# Power-up class
class PowerUp(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.image = pygame.Surface((30, 30))
        self.image.fill((0, 255, 0))  # Green color for invincibility power-up
        self.rect = self.image.get_rect()
        self.rect.center = (x, y)
    
    def update(self):
        # Add any additional behavior for the power-up
        pass

# Starfield class
class Starfield(pygame.sprite.Sprite):
    def __init__(self, width, height, num_stars):
        super().__init__()
        self.image = pygame.Surface((width, height))
        self.rect = self.image.get_rect()
        self.stars = []
        self.generate_stars(width, height, num_stars)
    
    def generate_stars(self, width, height, num_stars):
        for _ in range(num_stars):
            x = random.randint(0, width)
            y = random.randint(0, height)
            size = random.randint(1, 3)
            self.stars.append((x, y, size))
    
    def update(self):
        self.image.fill((0, 0, 0))
        for star in self.stars:
            x, y, size = star
            pygame.draw.circle(self.image, WHITE, (x, y), size)
    
    def scroll(self):
        for i in range(len(self.stars)):
            x, y, size = self.stars[i]
            y += SPEED // 2  # Adjust the scroll speed
            if y > HEIGHT:
                y = 0
            self.stars[i] = (x, y, size)

# Create the starfield
starfield = Starfield(WIDTH, HEIGHT, 100)  # Adjust the number of stars as desired

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

        # Add new power-ups
        if not powerups or powerups.sprites()[-1].rect.y > 200:
            powerup = PowerUp(random.randrange(WIDTH - 30), -30)
            powerups.add(powerup)

        # Obstacle movement and collision detection
        for obstacle in obstacles:
            obstacle.rect.y += SPEED
            if player.colliderect(obstacle.rect):
                game_state = "game over"
            if obstacle.rect.y > HEIGHT:
                obstacles.remove(obstacle)
                score += 1

        # Power-up movement and collision detection
        for powerup in powerups:
            powerup.rect.y += SPEED
            if player.colliderect(powerup.rect):
                powerups.remove(powerup)
                # Add any power-up behavior here
                score += 5  # Increase score for collecting power-ups

    # Update the starfield
    starfield.scroll()

    # Drawing
    screen.fill((0, 0, 0))
    starfield.update()
    screen.blit(starfield.image, starfield.rect)

    if game_state == "start":
        text = FONT.render("Press SPACE to start", True, WHITE)
        screen.blit(text, (WIDTH / 2 - text.get_width() / 2, HEIGHT / 2 - text.get_height() / 2))
    elif game_state == "running":
        pygame.draw.rect(screen, WHITE, player)
        obstacles.draw(screen)
        powerups.draw(screen)
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