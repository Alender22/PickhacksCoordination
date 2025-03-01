import pygame
import sys
import random

# Initialize Pygame
pygame.init()


# Constants
WIDTH, HEIGHT = 800, 600
RADIUS = 20
SQUARE_SIZE = 152
VELOCITY = 5
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move to the colors in the order they appeared")

# Initial position of the circle
x, y = WIDTH // 2, HEIGHT // 2
class ColorPuzzle:
    def __init__(self):
        self.start_time = pygame.time.get_ticks()
        self.last_color_change_time = self.start_time
        self.x = WIDTH // 2
        self.y = HEIGHT // 2
        self.color_change_time = 3  # Time in seconds to change color
        self.current_color = self.get_random_color()
        self.color_history = []
        self.shuffled = []

    def get_random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    def update(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Convert to seconds
        color_elapsed_time = (pygame.time.get_ticks() - self.last_color_change_time) / 1000  # Convert to seconds

        if elapsed_time < 16:  # Show the color for 15 seconds
            if color_elapsed_time >= self.color_change_time:
                self.color_history.append(self.current_color)
                self.current_color = self.get_random_color()
                self.last_color_change_time = pygame.time.get_ticks()

            # Draw the square
            screen.fill(self.current_color)
    
    def shuffle_colors(self):
        shuffles = self.color_history[:]
        random.shuffle(shuffles)
        self.shuffled = shuffles[:]

    def draw_color_history(self):
        # Fill the screen with white
        screen.fill(WHITE)

        # Draw small squares of each color in the color history in random order
        for i, color in enumerate(self.shuffled):
            pygame.draw.rect(screen, color, (10 + i * (SQUARE_SIZE + 5), HEIGHT - SQUARE_SIZE - 10, SQUARE_SIZE, SQUARE_SIZE))

        pygame.draw.circle(screen, RED, (x, y), RADIUS)

# Main game loop
puzzle = ColorPuzzle()

running = True
while running:
    for event in pygame.event.get():
       if event.type == pygame.QUIT:
            running = False

    # Fill the screen with white
    screen.fill(WHITE)

    # Update and draw the puzzle
    puzzle.update()

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

    puzzle.shuffle_colors()

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

    puzzle.x = max(RADIUS, min(WIDTH - RADIUS, puzzle.x))
    puzzle.y = max(RADIUS, min(HEIGHT - RADIUS, puzzle.y))

    #pygame.draw.circle(screen, RED, (x, y), RADIUS)'''
    
    puzzle.draw_color_history()

    pygame.display.flip()
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()
