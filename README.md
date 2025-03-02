
import pygame
import sys

class PushPuzzle:
    def __init__(self, grids):
        self.grids = grids
        self.current_grid_index = 0
        self.grid = [list(row) for row in self.grids[self.current_grid_index]]
        self.player_pos = self.find_player()
        self.targets = self.find_targets()

    def find_player(self):
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 'P':
                    return (x, y)
        return None

    def find_targets(self):
        targets = []
        for y, row in enumerate(self.grid):
            for x, cell in enumerate(row):
                if cell == 'Y':
                    targets.append((x, y))
        return targets

    def move(self, direction):
        x, y = self.player_pos
        if direction == 'up':
            new_pos = (x, y - 1)
            push_pos = (x, y - 2)
        elif direction == 'down':
            new_pos = (x, y + 1)
            push_pos = (x, y + 2)
        elif direction == 'left':
            new_pos = (x - 1, y)
            push_pos = (x - 2, y)
        elif direction == 'right':
            new_pos = (x + 1, y)
            push_pos = (x + 2, y)
        elif direction == 'exit':
            return self.player_pos
        elif direction == 'reset':
            self.grid = self.grids[self.current_grid_index]
            self.player_pos = self.find_player()
            self.targets = self.find_targets()
            return self.player_pos
        else:
            return False

        if self.can_move(new_pos, push_pos):
            self.update_grid(new_pos, push_pos)
            self.player_pos = new_pos
            return True
        return False

    def can_move(self, new_pos, push_pos):
        x, y = new_pos
        if self.grid[y][x] == '#':
            return False
        if self.grid[y][x] == 'Y':
            return False 
        if self.grid[y][x] == 'B':
            px, py = push_pos
            if self.grid[py][px] in ['#', 'B']:
                return False
        return True

    def update_grid(self, new_pos, push_pos):
        x, y = self.player_pos
        nx, ny = new_pos
        self.grid[y][x] = ' '
        if self.grid[ny][nx] == 'B':
            px, py = push_pos
            self.grid[py][px] = 'B'
        self.grid[ny][nx] = 'P'

    def is_solved(self):
        for tx, ty in self.targets:
            if self.grid[ty][tx] != 'B':
                return False
        return True

    def display(self):
        for row in self.grid:
            print(''.join(row))
        print()

    def next_grid(self):
        if self.current_grid_index < len(self.grids) - 1:
            self.current_grid_index += 1
            self.grid = self.grids[self.current_grid_index]
            self.player_pos = self.find_player()
            self.targets = self.find_targets()
            return True
        return False

    def previous_grid(self):
        if self.current_grid_index > 0:
            self.current_grid_index -= 1
            self.grid = self.grids[self.current_grid_index]
            self.player_pos = self.find_player()
            self.targets = self.find_targets()
            return True
        return False

# Example usage
grids = [
    [
        "##########",
        "#        #",
        "#P     B #",
        "## B     #",
        "#Y    Y  #",
        "##########"
    ],
    [
        "##########",
        "#P       #",
        "#     #B #",
        "#    #   #",
        "#    B   #",
        "#        #",
        "# Y#Y    #",
        "##########"
    ],
    [
        "###########",
        "#         #",
        "#    B    #",
        "#    #    #",
        "# #       #",
        "#      Y#P#",
        "###########"
    ]
]

puzzle = PushPuzzle([[list(row) for row in grid] for grid in grids])

# Initialize pygame
pygame.init()

# Set up display
window_size = (800, 600)
window = pygame.display.set_mode(window_size)
pygame.display.set_caption('Push Puzzle')

# Set up colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)

# Set up fonts
font = pygame.font.SysFont(None, 55)

def draw_grid():
    window.fill(WHITE)
    for y, row in enumerate(puzzle.grid):
        for x, cell in enumerate(row):
            if cell == '#':
                color = BLACK
            elif cell == 'P':
                color = BLUE
            elif cell == 'B':
                color = RED
            elif cell == 'Y':
                color = GREEN
            else:
                color = WHITE
            pygame.draw.rect(window, color, pygame.Rect(x * 40, y * 40, 40, 40))
            pygame.draw.rect(window, BLACK, pygame.Rect(x * 40, y * 40, 40, 40), 1)

    pygame.display.flip()

# Main game loop
running = True
while running:
    draw_grid()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                puzzle.move('up')
            elif event.key == pygame.K_DOWN:
                puzzle.move('down')
            elif event.key == pygame.K_LEFT:
                puzzle.move('left')
            elif event.key == pygame.K_RIGHT:
                puzzle.move('right')
            elif event.key == pygame.K_r:
                puzzle.move('reset')
            elif event.key == pygame.K_n:
                puzzle.next_grid()
            elif event.key == pygame.K_p:
                puzzle.previous_grid()
            elif event.key == pygame.K_ESCAPE:
                running = False

    if puzzle.is_solved():
        if not puzzle.next_grid():
            running = False

pygame.quit()
sys.exit()
