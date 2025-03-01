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

# Define borders as a list of pygame.Rect objects
borders = [
    pygame.Rect(100, 100, 600, 10),  # Top border
    pygame.Rect(100, 490, 600, 10),  # Bottom border
    pygame.Rect(100, 100, 10, 400),  # Left border
    pygame.Rect(690, 100, 10, 400)   # Right border
]

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
        new_y = y - VELOCITY
        if bg_y < 0 and new_y < HEIGHT // 2:
            bg_y += VELOCITY
        else:
            y = new_y
    if keys[pygame.K_s]:
        new_y = y + VELOCITY
        if bg_y > HEIGHT - background_rect.height and new_y > HEIGHT // 2:
            bg_y -= VELOCITY
        else:
            y = new_y
    if keys[pygame.K_a]:
        new_x = x - VELOCITY
        if bg_x < 0 and new_x < WIDTH // 2:
            bg_x += VELOCITY
        else:
            x = new_x
    if keys[pygame.K_d]:
        new_x = x + VELOCITY
        if bg_x > WIDTH - background_rect.width and new_x > WIDTH // 2:
            bg_x -= VELOCITY
        else:
            x = new_x

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

    # Check for collisions with borders
    circle_rect = pygame.Rect(x - RADIUS, y - RADIUS, RADIUS * 2, RADIUS * 2)
    for border in borders:
        adjusted_border = border.move(bg_x, bg_y)
        if circle_rect.colliderect(adjusted_border):
            if keys[pygame.K_w]:
                y += VELOCITY
            if keys[pygame.K_s]:
                y -= VELOCITY
            if keys[pygame.K_a]:
                x += VELOCITY
            if keys[pygame.K_d]:
                x -= VELOCITY

    # Draw the background image
    screen.blit(background_image, (bg_x, bg_y))

    # Draw the borders
    for border in borders:
        adjusted_border = border.move(bg_x, bg_y)
        pygame.draw.rect(screen, BLACK, adjusted_border)

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