import pygame
import sys
import random

# Initialize Pygame
pygame.init()


# Constants
WIDTH, HEIGHT = 800, 600
RADIUS = 20
SQUARE_SIZE = 40
VELOCITY = 5
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move the Red Circle")

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

    def get_random_color(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))
    
    def update(self):
        elapsed_time = (pygame.time.get_ticks() - self.start_time) / 1000  # Convert to seconds
        color_elapsed_time = (pygame.time.get_ticks() - self.last_color_change_time) / 1000  # Convert to seconds

        if elapsed_time < 15:  # Show the color for 15 seconds
            if color_elapsed_time >= self.color_change_time:
                self.color_history.append(self.current_color)
                self.current_color = self.get_random_color()
                self.last_color_change_time = pygame.time.get_ticks()

            # Draw the square
            screen.fill(self.current_color)
            #pygame.draw.rect(screen, self.current_color, (self.x, self.y, SQUARE_SIZE, SQUARE_SIZE))
    
    def draw_color_history(self):
        # Fill the screen with white
        screen.fill(WHITE)

        # Draw small squares of each color in the color history in random order
        shuffled_colors = self.color_history[:]
        random.shuffle(shuffled_colors)
        for i, color in enumerate(shuffled_colors):
            pygame.draw.rect(screen, color, (10 + i * (SQUARE_SIZE + 5), HEIGHT - SQUARE_SIZE - 10, SQUARE_SIZE, SQUARE_SIZE))

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

# After the main loop, draw the color history
puzzle.draw_color_history()

# Update the display to show the color history
pygame.display.flip()

# Wait for a few seconds before quitting
pygame.time.wait(5000)

# Quit Pygame
pygame.quit()
sys.exit()
