import pygame
import sys
from tkinter import Tk, filedialog
from concurrent.futures import ThreadPoolExecutor
import os

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

    print("Scanning for colors")

    def process_pixel(x, y):
        pixel_color = image.unmap_rgb(pixel_array[x, y])
        if all(abs(pixel_color[i] - target_color[i]) <= tolerance for i in range(3)):
            return pygame.Rect(x, y, 1, 1)
        return None

    # Use ThreadPoolExecutor to process pixels in parallel
    with ThreadPoolExecutor(max_workers=max(1, os.cpu_count() - 1)) as executor:
        futures = [executor.submit(process_pixel, x, y) for y in range(image_rect.height) for x in range(image_rect.width)]
        for future in futures:
            rect = future.result()
            if rect:
                borders.append(rect)

    print("Filtering borders")

    # Filter out isolated rects
    filtered_borders = filter_isolated_rects(borders, 1)

    print("Merging borders")

    # Merge adjacent rects to form larger borders
    #merged_borders = merge_rects(filtered_borders)
    merged_borders = filtered_borders

    # Clean up
    del pixel_array
    pygame.quit()

    return merged_borders

def merge_rects(rects):
    # This function merges adjacent rects into larger rects
    def merge_pair(rect):
        merged_rect = rect
        for other_rect in rects[:]:
            if merged_rect.colliderect(other_rect):
                merged_rect.union_ip(other_rect)
                rects.remove(other_rect)
        return merged_rect

    merged = []
    with ThreadPoolExecutor(max_workers=max(1, os.cpu_count() - 1)) as executor:
        futures = [executor.submit(merge_pair, rect) for rect in rects]
        for future in futures:
            merged.append(future.result())
    return merged

def filter_isolated_rects(rects, max_distance=3):
    # This function filters out rects that are completely surrounded by other rects within max_distance
    def is_surrounded(rect):
        directions = [
            (max_distance, 0), (-max_distance, 0), (0, max_distance), (0, -max_distance),
            (max_distance, max_distance), (max_distance, -max_distance),
            (-max_distance, max_distance), (-max_distance, -max_distance)
        ]
        for dx, dy in directions:
            neighbor_rect = rect.move(dx, dy)
            if not any(neighbor_rect.colliderect(other_rect) for other_rect in rects if other_rect != rect):
                return False
        return True

    with ThreadPoolExecutor(max_workers=max(1, os.cpu_count() - 1)) as executor:
        results = list(executor.map(is_surrounded, rects))

    filtered = [rect for rect, surrounded in zip(rects, results) if not surrounded]
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