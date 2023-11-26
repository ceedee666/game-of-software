import curses
import random
from curses import wrapper
from time import sleep

GLIDER = [[0, 1, 0], [0, 0, 1], [1, 1, 1]]

EIGHT = [
    [1, 1, 0, 0, 0, 0],
    [1, 1, 0, 1, 0, 0],
    [0, 0, 0, 0, 1, 0],
    [0, 1, 0, 0, 0, 0],
    [0, 0, 1, 0, 1, 1],
    [0, 0, 0, 0, 1, 1],
]


def init_grid(width, height):
    grid = []
    for _ in range(height):
        grid.append([False] * width)
    return grid


def randomize(grid):
    for y in range(len(grid)):
        for x in range(len(grid[y])):
            grid[y][x] = random.choice((True, False))
    return grid


def neighbours(x, y, grid):
    neighbours = []
    for dx in (-1, 0, 1):
        for dy in (-1, 0, 1):
            if (
                x + dx >= 0
                and x + dx < len(grid[0])
                and y + dy >= 0
                and y + dy < len(grid)
            ):
                if dx != 0 or dy != 0:
                    neighbours.append(grid[y + dy][x + dx])
    return neighbours


def init_pattern(name, grid, start_x=1, start_y=1):
    if name == "glider":
        for y in range(len(GLIDER)):
            for x in range(len(GLIDER[0])):
                if GLIDER[y][x] == 1:
                    grid[start_y + y][start_x + x] = True
    if name == "eight":
        for y in range(len(EIGHT)):
            for x in range(len(EIGHT[0])):
                if EIGHT[y][x] == 1:
                    grid[start_y + y][start_x + x] = True

    return grid


def next_generation(grid):
    new_grid = init_grid(len(grid[0]), len(grid))
    for x in range(len(grid[0])):
        for y in range(len(grid)):
            n = neighbours(x, y, grid)
            if grid[y][x] is True:
                if n.count(True) < 2:
                    new_grid[y][x] = False
                elif n.count(True) in (2, 3):
                    new_grid[y][x] = True
                elif n.count(True) > 3:
                    new_grid[y][x] = False
            else:
                if n.count(True) == 3:
                    new_grid[y][x] = True
    return new_grid


def main_window(stdscr):
    grid = init_grid(curses.COLS - 2, curses.LINES - 3)
    # grid = randomize(grid)
    grid = init_pattern("eight", grid, 5, 5)
    grid = init_pattern("glider", grid, 25, 5)

    generation = 0
    while True:
        stdscr.clear()
        # Draw the frame
        stdscr.addstr(0, 0, f"Conway's Game of Life - Generation {generation}")
        stdscr.hline(1, 0, "_", curses.COLS - 1)
        stdscr.hline(curses.LINES - 1, 0, "_", curses.COLS - 1)
        stdscr.vline(2, 0, "|", curses.LINES - 1)
        stdscr.vline(2, curses.COLS - 1, "|", curses.LINES - 1)

        # Draw the grid
        for x in range(len(grid[0])):
            for y in range(len(grid)):
                if grid[y][x]:
                    stdscr.addstr(y + 2, x + 1, "#")
                else:
                    stdscr.addstr(y + 2, x + 1, " ")
        stdscr.refresh()
        sleep(0.05)
        grid = next_generation(grid)
        generation += 1


if __name__ == "__main__":
    wrapper(main_window)
