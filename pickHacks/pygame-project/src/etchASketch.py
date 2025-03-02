import pygame
import sys
import time

# Initialize Pygame
pygame.init()

# Constants
WIDTH, HEIGHT = 800, 600
RADIUS = 2
VELOCITY = 1
RED = (255, 0, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PEAK = 20
LINE = 10

# Set up the display
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Move the Red Circle")
screen.fill(WHITE)

# Initial position of the circle
x, y = WIDTH // 2, HEIGHT // 2

# Main game loop
running = True

doZero = 0
doOnes = 0  # 1 = up, 0 = down
doLine = 0
doLower = 0
Left = False 
Up = False

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
    if keys[pygame.K_c]:
        screen.fill(WHITE)
    if keys[pygame.K_0]:
        doZero = PEAK
        doLine = LINE
        time.sleep(0.2)
    if keys[pygame.K_1]:
        doOnes = PEAK
        doLine = LINE
        time.sleep(0.2)
    if keys[pygame.K_SPACE]:
        doLine = LINE * 3
        time.sleep(0.2)
    if keys[pygame.K_l]:
        Left = True
    if keys[pygame.K_u]:
        Up = True
    if keys[pygame.K_m]:
        doLower = 50

    if doZero > 0:
        x += VELOCITY
        if doZero > PEAK / 2:
            y += VELOCITY
        else:
            y -= VELOCITY
        doZero -= 1 

    if doOnes > 0:
        x += VELOCITY
        if doOnes > PEAK / 2:
            y -= VELOCITY
        else:
            y += VELOCITY
        doOnes -= 1

    if doLine > 0 and doZero == 0 and doOnes == 0:
        x += VELOCITY
        doLine -= 1

    if doLower > 0:
        y += VELOCITY
        doLower -= 1

    if Left == True:
        x -= VELOCITY
        if x <= 30:
            Left = False 

    if Up == True: 
        y -= VELOCITY
        if y <= 30:
            Up = False
    

    # Ensure the circle stays within the window bounds
    x = max(RADIUS, min(WIDTH - RADIUS, x))
    y = max(RADIUS, min(HEIGHT - RADIUS, y))

    # Fill the screen with black
    #screen.fill(WHITE)

    # Draw the red circle
    pygame.draw.circle(screen, BLACK, (x, y), RADIUS)

    # Update the display
    pygame.display.flip()

    # Cap the frame rate
    pygame.time.Clock().tick(60)

# Quit Pygame
pygame.quit()
sys.exit()