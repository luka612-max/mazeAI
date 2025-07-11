import pygame
import random
from pygame import mixer
from collections import deque

# Constants
WIDTH, HEIGHT = 700, 700
ROWS, COLS = 25, 25 # Ensure odd numbers for paths
CELL_SIZE = WIDTH // COLS

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Directions for movement
DIRECTIONS = [(0, -2), (0, 2), (-2, 0), (2, 0)]  # Up, Down, Left, Right
MOVES = [(0, -1), (0, 1), (-1, 0), (1, 0)]  # AI moves step by step

# Initialize Pygame
pygame.init()
#background music
mixer.music.load('background.wav')
mixer.music.play(-1)
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Maze Solver AI")
clock = pygame.time.Clock()

pathimg = pygame.image.load('pathimg.png')
wallimg = pygame.image.load('wall.png')

# Maze grid (1 = wall, 0 = path)
maze = [[1 for _ in range(COLS)] for _ in range(ROWS)]

def draw_maze():
    """Draw the maze on the screen."""
    screen.fill(BLACK)
    for row in range(ROWS):
        for col in range(COLS):
            if maze[row][col] == 0:
                screen.blit(pathimg, (col*CELL_SIZE, row*CELL_SIZE))
            else:
                screen.blit(wallimg, (col*CELL_SIZE, row*CELL_SIZE))
            # color = WHITE if maze[row][col] == 0 else BLACK

            # pygame.draw.rect(screen, color, (col * CELL_SIZE, row * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.draw.rect(screen, GREEN, (1 * CELL_SIZE, 1 * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Start
    pygame.draw.rect(screen,RED , ((COLS-2) * CELL_SIZE, (ROWS-2) * CELL_SIZE, CELL_SIZE, CELL_SIZE))  # Exit
    pygame.display.flip()

def carve_passages(cx, cy):
    """Recursive DFS maze generation."""
    maze[cy][cx] = 0  # Mark as a passage
    random.shuffle(DIRECTIONS)  # Shuffle directions for randomness

    for dx, dy in DIRECTIONS:
        nx, ny = cx + dx, cy + dy
        mid_x, mid_y = cx + dx // 2, cy + dy // 2

        if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 1:
            maze[mid_y][mid_x] = 0  # Remove wall
            carve_passages(nx, ny)


def generate_maze():
    """Generate a maze using DFS."""
    carve_passages(1, 1)
    maze[1][1] = 0  # Entrance
    maze[ROWS-2][COLS-2] = 0  # Exit


def bfs_solve(start, end):
    """Find the shortest path using BFS."""
    queue = deque([(start, [start])])  # (current_position, path_taken)
    visited = set()

    while queue:
        (x, y), path = queue.popleft()
        if (x, y) == end:
            return path  # Return the path to the goal

        for dx, dy in MOVES:
            nx, ny = x + dx, y + dy
            if 0 <= nx < COLS and 0 <= ny < ROWS and maze[ny][nx] == 0 and (nx, ny) not in visited:
                queue.append(((nx, ny), path + [(nx, ny)]))
                visited.add((nx, ny))

    return []  # No path found


# Generate Maze
generate_maze()
draw_maze()

# AI start and end positions
start_pos = (1, 1)
end_pos = (COLS - 2, ROWS - 2)

# Solve Maze
path = bfs_solve(start_pos, end_pos)
k=0
# Main loop
for step in path:
    clock.tick(10)  # Control AI speed
    draw_maze()
    
    # Draw AI (blue square)
    pygame.draw.rect(screen, BLUE, (step[0] * CELL_SIZE, step[1] * CELL_SIZE, CELL_SIZE, CELL_SIZE))
    pygame.display.flip()
     
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            k=1
    if k==1:
        break
pygame.quit()
