import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
RADIUS = 20
VELOCITY = 5
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move the Red Circle")

# Initial position of the circle
x, y = WIDTH // 2, HEIGHT // 2

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        y -= VELOCITY
    if keys[pygame.K_s]:
        y += VELOCITY
    if keys[pygame.K_a]:
        x -= VELOCITY
    if keys[pygame.K_d]:
        x += VELOCITY

    # Ensure the circle stays within the window bounds
    x = max(RADIUS, min(WIDTH - RADIUS, x))
    y = max(RADIUS, min(HEIGHT - RADIUS, y))

    # Fill the screen with black
    screen.fill(WHITE)

    # Draw the red circle
    pygame.draw.circle(screen, RED, (x, y), RADIUS)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()