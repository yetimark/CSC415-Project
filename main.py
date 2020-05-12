# MAIN: Run this script for the solution

from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from time import sleep
from grid import Grid

CELL = '\u2588'
REST = 0.1



def input_demo(screen):
    # screen.clear()

    while True:
        test = screen.get_event()
        # screen.print_at(test, 0,0)
        if(test != None):
            screen.print_at(CELL, 0, 0, screen.COLOUR_GREEN)
            screen.refresh()
            sleep(REST)
        else:
            screen.print_at(CELL, 0, 0, screen.COLOUR_RED)
            screen.refresh()
            sleep(REST)


def flash_cursor(screen, grid):

    while True:
        test = screen.get_event()
        # screen.print_at(test, 0,0)
        if(test != None):
            screen.print_at(CELL, grid.cursor[0], grid.cursor[1], screen.COLOUR_WHITE)
            screen.refresh()
            sleep(REST)
        else:
            screen.print_at(CELL, grid.cursor[0], grid.cursor[1], screen.COLOUR_CYAN)
            screen.refresh()
            sleep(REST)


def grid_init(screen):
    grid = Grid()

    for i in range(len(grid.cells[0])):
        for j in range(len(grid.cells)):
            screen.print_at(CELL, i, j, screen.COLOUR_WHITE)
    # - cursor
    screen.print_at(CELL, grid.cursor[0], grid.cursor[1], screen.COLOUR_CYAN)
    # - start
    screen.print_at(CELL, grid.start[0], grid.start[1], screen.COLOUR_GREEN)
    # - end
    screen.print_at(CELL, grid.end[0], grid.end[1], screen.COLOUR_RED)

    screen.refresh()

    flash_cursor(screen, grid)
    

Screen.wrapper(grid_init)