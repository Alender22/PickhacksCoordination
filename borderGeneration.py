import pygame
import sys
from tkinter import Tk, filedialog
from concurrent.futures import ThreadPoolExecutor

def generate_borders(image_path, target_color, tolerance=35):
    # Initialize Pygame
    pygame.init()

    # Load the image
    image = pygame.image.load(image_path)
    image_rect = image.get_rect()

    # Get the pixel array of the image
    pixel_array = pygame.PixelArray(image)

    # List to store the borders
    borders = []

    def process_row(y):
        row_borders = []
        for x in range(image_rect.width):
            pixel_color = image.unmap_rgb(pixel_array[x, y])
            if all(abs(pixel_color[i] - target_color[i]) <= tolerance for i in range(3)):
                # Create a rect for the block of the target color
                rect = pygame.Rect(x, y, 1, 1)
                row_borders.append(rect)
        return row_borders

    # Use ThreadPoolExecutor to process rows in parallel
    with ThreadPoolExecutor() as executor:
        results = executor.map(process_row, range(image_rect.height))
        for row_borders in results:
            borders.extend(row_borders)

    # Merge adjacent rects to form larger borders
    merged_borders = merge_rects(borders)

    # Filter out isolated rects
    filtered_borders = filter_isolated_rects(merged_borders)

    # Clean up
    del pixel_array
    pygame.quit()

    return filtered_borders

def merge_rects(rects):
    # This function merges adjacent rects into larger rects
    merged = []
    while rects:
        rect = rects.pop(0)
        merged_rect = rect
        for other_rect in rects[:]:
            if merged_rect.colliderect(other_rect):
                merged_rect.union_ip(other_rect)
                rects.remove(other_rect)
        merged.append(merged_rect)
    return merged

def filter_isolated_rects(rects, sep=3):
    # This function filters out rects that are isolated by more than max_distance rects
    filtered = []
    for rect in rects:
        neighbors = 0
        for other_rect in rects:
            if rect != other_rect and ( -sep < rect[0] - other_rect[0] < sep and -sep < rect[1] - other_rect[1] < sep): #and (rect.colliderect(other_rect.inflate(max_distance, max_distance) or rect.inflate(max_distance, max_distance).colliderect(other_rect))):
                neighbors += 1
                if neighbors >= (sep*2)**2:
                    break
        if neighbors < (sep*2)**2:
            filtered.append(rect)
    return filtered

def pick_color_from_image(image_path):
    # Initialize Pygame
    pygame.init()

    # Load the image
    image = pygame.image.load(image_path)
    screen = pygame.display.set_mode(image.get_size())
    pygame.display.set_caption("Click to select color")

    # Display the image
    screen.blit(image, (0, 0))
    pygame.display.flip()

    # Wait for the user to click on the image
    running = True
    color = None
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                x, y = event.pos
                color = screen.get_at((x, y))[:3]
                running = False

    pygame.quit()
    return color

if __name__ == "__main__":
    if len(sys.argv) < 2 or len(sys.argv) > 3:
        print("Usage: python borderGeneration.py <image_path> [output_file]")
        sys.exit(1)

    image_path = sys.argv[1]
    output_file = sys.argv[2] if len(sys.argv) == 3 else "borders.txt"

    # Pick color from the image by clicking
    target_color = pick_color_from_image(image_path)
    if not target_color:
        print("No color selected.")
        sys.exit(1)

    borders = generate_borders(image_path, target_color)

    # Write borders to the output file
    with open(output_file, 'w') as f:
        for border in borders:
            f.write(f"{border.x},{border.y},{border.width},{border.height}\n")

    # Initialize Pygame to display the image with borders
    pygame.init()
    image = pygame.image.load(image_path)
    screen = pygame.display.set_mode(image.get_size())
    pygame.display.set_caption("Generated Borders")

    # Display the image
    screen.blit(image, (0, 0))

    # Draw the borders
    for border in borders:
        pygame.draw.rect(screen, (0, 255, 0), border, 1)  # Draw borders in green

    pygame.display.flip()

    # Wait for user input to close the window
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                running = False

    pygame.quit()
    sys.exit()