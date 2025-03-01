import pygame
import sys

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
RADIUS = 5
VELOCITY = 5
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)
pygame.display.set_caption("Move the Red Circle")

# Load background image
background_image = pygame.image.load('images/sntMap-01.png')
background_rect = background_image.get_rect()

# Initial position of the circle
x, y = WIDTH // 2, HEIGHT // 2

# Initial position of the background
bg_x, bg_y = 0, 0

# Main game loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.VIDEORESIZE:
            WIDTH, HEIGHT = event.w, event.h
            screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.RESIZABLE)

    keys = pygame.key.get_pressed()
    if keys[pygame.K_w]:
        if bg_y < 0 and y - VELOCITY < HEIGHT // 2:
            bg_y += VELOCITY
        else:
            y -= VELOCITY
    if keys[pygame.K_s]:
        if bg_y > HEIGHT - background_rect.height and y + VELOCITY > HEIGHT // 2:
            bg_y -= VELOCITY
        else:
            y += VELOCITY
    if keys[pygame.K_a]:
        if bg_x < 0 and x - VELOCITY < WIDTH // 2:
            bg_x += VELOCITY
        else:
            x -= VELOCITY
    if keys[pygame.K_d]:
        if bg_x > WIDTH - background_rect.width and x + VELOCITY > WIDTH // 2:
            bg_x -= VELOCITY
        else:
            x += VELOCITY

    # Ensure the circle stays within the window bounds
    x = max(RADIUS, min(WIDTH - RADIUS, x))
    y = max(RADIUS, min(HEIGHT - RADIUS, y))

    # Ensure the background stays within the window bounds
    bg_x = min(0, max(WIDTH - background_rect.width, bg_x))
    bg_y = min(0, max(HEIGHT - background_rect.height, bg_y))

    # Center the circle when the background is not clamped
    if not (bg_x == 0 or bg_x == WIDTH - background_rect.width):
        x = WIDTH // 2
    if not (bg_y == 0 or bg_y == HEIGHT - background_rect.height):
        y = HEIGHT // 2

    # Draw the background image
    screen.blit(background_image, (bg_x, bg_y))

    # Draw the red circle
    screen_x = x
    screen_y = y
    pygame.draw.circle(screen, RED, (screen_x, screen_y), RADIUS)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()