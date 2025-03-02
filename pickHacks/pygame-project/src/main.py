import pygame
import sys
import pushpuzzle

def load_borders_from_files(file_paths):
    borders = []
    for file_path in file_paths:
        with open(file_path, 'r') as file:
            for line in file:
                x, y, width, height = map(int, line.strip().split(','))
                borders.append(pygame.Rect(x, y, width, height))
    return borders

def load_activation_areas(file_paths):
    # file_paths is an array of tuples, (file_path, game), where game is the name of the game to switch to
    activation_areas = {}
    for file_path in file_paths:
        game = file_path[1]
        with open(file_path[0], 'r') as file:
            for line in file:
                x, y, width, height = line.strip().split(',')
                activation_areas[f"{x}-{y}-{width}-{height}"] = game
    return activation_areas

def switch_to_another_game(game):
    if game == 'pushpuzzle':
        pushpuzzle.main()
    # Add more games here as needed
    else:
        print(f"Unknown game: {game}")

def check_collision_and_switch(activation_areas, circle_rect, bg_x, bg_y):
    global activation_hit
    for key, game in activation_areas.items():
        x, y, width, height = map(int, key.split('-'))
        rect = pygame.Rect(x, y, width, height)
        adjusted_rect = rect.move(bg_x, bg_y)
        if circle_rect.colliderect(adjusted_rect):
            if not activation_hit:
                print(f"Collision detected! Switching to {game}...")
                switch_to_another_game(game)
                activation_hit = True
            return True
    activation_hit = False
    return False

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

# List of border files
border_files = ['src/mapBoundaries-Buildings.txt']
activation_files = [('src/activationAreaHavener.txt', 'pushpuzzle')]
# Add more border files as needed

# Load borders from files
borders = load_borders_from_files(border_files)
activation_areas = load_activation_areas(activation_files)

# Initial position of the circle
x, y = WIDTH // 2, HEIGHT // 2

# Initial position of the background
bg_x, bg_y = 0, 0

activation_hit = False

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
    if keys[pygame.K_q]:
        running = False
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

    # Check for collisions with activation areas and switch game if needed
    check_collision_and_switch(activation_areas, circle_rect, bg_x, bg_y)

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