import pygame
import sys
from pygame.locals import *

pygame.init()

# Constants
WIDTH = 700
ROWS = 50
CELL_SIZE = WIDTH // ROWS
FPS = 30

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

# Initialize Pygame
font = pygame.font.SysFont(None, 30)
mainClock = pygame.time.Clock()
screen = pygame.display.set_mode((WIDTH, WIDTH))
pygame.display.set_caption('BFS and DFS Visualization')

class Spot:
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.x = row * CELL_SIZE
        self.y = col * CELL_SIZE
        self.color = WHITE
        self.neighbors = []

    def get_pos(self):
        return self.row, self.col

    def is_barrier(self):
        return self.color == BLACK

    def make_start(self):
        self.color = BLUE

    def make_end(self):
        self.color = GREEN

    def make_barrier(self):
        self.color = BLACK

    def make_path(self):
        self.color = RED

    def reset(self):
        self.color = WHITE

    def draw(self, win):
        pygame.draw.rect(win, self.color, (self.x, self.y, CELL_SIZE, CELL_SIZE))

    def update_neighbors(self, grid):
        self.neighbors = []
        # Check adjacent cells
        if self.row > 0:  # Up
            self.neighbors.append(grid[self.row - 1][self.col])
        if self.row < ROWS - 1:  # Down
            self.neighbors.append(grid[self.row + 1][self.col])
        if self.col > 0:  # Left
            self.neighbors.append(grid[self.row][self.col - 1])
        if self.col < ROWS - 1:  # Right
            self.neighbors.append(grid[self.row][self.col + 1])

def make_grid():
    return [[Spot(i, j) for j in range(ROWS)] for i in range(ROWS)]

def draw_grid(win):
    for i in range(ROWS):
        pygame.draw.line(win, BLACK, (0, i * CELL_SIZE), (WIDTH, i * CELL_SIZE))
    for j in range(ROWS):
        pygame.draw.line(win, BLACK, (j * CELL_SIZE, 0), (j * CELL_SIZE, WIDTH))

def draw(win, grid):
    win.fill(WHITE)
    for row in grid:
        for spot in row:
            spot.draw(win)
    draw_grid(win)
    pygame.display.update()

def bfs(draw, start, end):
    queue = [start]
    visited = set()
    parent = {}
    visited.add(start)
    while queue:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        current = queue.pop(0)
        if current == end:
            reconstruct_path(draw, parent, current)
            return
        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                parent[neighbor] = current
                queue.append(neighbor)
                neighbor.make_path()
        draw()
        if current != start:
            current.color = RED
    print("No solution!")

def dfs(draw, start, end):
    stack = [start]
    visited = set()
    parent = {}
    visited.add(start)
    while stack:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
        current = stack.pop()
        if current == end:
            reconstruct_path(draw, parent, current)
            return
        for neighbor in current.neighbors:
            if neighbor not in visited and not neighbor.is_barrier():
                visited.add(neighbor)
                parent[neighbor] = current
                stack.append(neighbor)
                neighbor.make_path()
        draw()
        if current != start:
            current.color = RED
    print("No solution!")

def reconstruct_path(draw, parent, current):
    while current in parent:
        current = parent[current]
        current.make_path()
        draw()

def get_clicked_pos(pos):
    x, y = pos
    row = x // CELL_SIZE
    col = y // CELL_SIZE
    return row, col

def main():
    grid = make_grid()
    start = None
    end = None
    run = True
    while run:
        draw(screen, grid)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if pygame.mouse.get_pressed()[0]:  # Left click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                spot = grid[row][col]
                if not start and spot != end:
                    start = spot
                    start.make_start()
                elif not end and spot != start:
                    end = spot
                    end.make_end()
                elif spot != start and spot != end:
                    spot.make_barrier()
            if pygame.mouse.get_pressed()[2]:  # Right click
                pos = pygame.mouse.get_pos()
                row, col = get_clicked_pos(pos)
                spot = grid[row][col]
                spot.reset()
                if spot == start:
                    start = None
                if spot == end:
                    end = None
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    bfs(lambda: draw(screen, grid), start, end)
                if event.key == pygame.K_d and start and end:
                    for row in grid:
                        for spot in row:
                            spot.update_neighbors(grid)
                    dfs(lambda: draw(screen, grid), start, end)
                if event.key == pygame.K_c:
                    grid = make_grid()
                    start = None
                    end = None
        mainClock.tick(FPS)

if __name__ == "__main__":
    main()
