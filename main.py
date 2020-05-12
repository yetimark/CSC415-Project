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

def screen_print(screen, dest, color):
    screen.print_at(CELL, dest[0], dest[1], color)




# --- returns a tuple of the new location based on key event ---
def direction_handler(grid, code):

    if code == -204: # Up
        # go up, subtract from rows
        dest = (grid.cursor[0], grid.cursor[1] - 1)

    elif code == -203: # Left
        # go left, subtract from collumns
        dest = (grid.cursor[0] - 1, grid.cursor[1])

    elif code == -206: # Down
        # go down, add to rows
        dest = (grid.cursor[0], grid.cursor[1] + 1)

    elif code == -205: # Right
        # go right, add one to collumns
        dest = (grid.cursor[0] + 1, grid.cursor[1])

    else:
        # in case something else gets passed in here. send it to current cursor
        dest = grid.cursor

    # - now check and correct if out of bounds -
    #  -- return current cursor pos if out of bounds --
    if ((dest[0] < 0) or (dest[0] >= grid.collumns) or (dest[1] < 0) or (dest[1] >= grid.rows)):
        dest = grid.cursor
    
    return dest


def edit_mode(screen, grid):
    # - on edit mode start show cursor -
    screen_print(screen, grid.cursor, screen.COLOUR_CYAN)
    screen.refresh()

    while True:
        event = screen.get_event()

        if(event != None):
            code = event.key_code

            # - cursor movement -
            if(code < -100):
                prev_cursor = grid.cursor
                prev_colour = screen.get_from(prev_cursor[0], prev_cursor[1])[1]  # --- Foreground, I think this should be the color I want
                

                # print('**************************** ',prev_colour)
                dest = direction_handler(grid, code)

                # - set new color -
                grid.cursor = dest
                screen_print(screen, dest, screen.COLOUR_CYAN)

                # - set prev position color -
                # -- default white, check for start, end and wall --

                if prev_cursor == grid.start:   # start check
                    screen_print(screen, prev_cursor, screen.COLOUR_GREEN)
                
                elif prev_cursor == grid.end:   # end check
                    screen_print(screen, prev_cursor, screen.COLOUR_RED)

                elif grid.is_wall(prev_cursor):
                    screen_print(screen, prev_cursor, screen.COLOUR_BLACK)

                else:  
                    screen_print(screen, prev_cursor, screen.COLOUR_WHITE)

                
            # -- FIX: Known issue involved here for overlapping wall, start, and end --

            # --- Set old color to white for all first ---
            # - set new start - (s)
            elif code == 115:
                screen_print(screen, grid.start, screen.COLOUR_WHITE)
                grid.start = grid.cursor
                screen_print(screen, grid.start, screen.COLOUR_GREEN)

            # - set new end - (e)
            elif code == 101:
                screen_print(screen, grid.end, screen.COLOUR_WHITE)
                grid.end = grid.cursor
                screen_print(screen, grid.end, screen.COLOUR_RED)

            # - toggle wall - (w) 
            elif code == 119:
                if grid.is_wall(grid.cursor):
                    # - remove wall -
                    grid.remove_wall(grid.cursor)
                    screen_print(screen, grid.cursor, screen.COLOUR_WHITE)
                else:
                    # - add wall -
                    grid.add_wall(grid.cursor)
                    screen_print(screen, grid.cursor, screen.COLOUR_BLACK)

            # - exit edit mode - (esc)
            elif code == -1:
                # - hide cursor on exit
                screen_print(screen, grid.cursor, screen.COLOUR_WHITE)
                screen.refresh()
                break

        screen.refresh()
            
        



def test_codes(screen, grid):
    while True:
        event = screen.get_event()

        if(event != None):
            screen.print_at(str(event.key_code), grid.cursor[0], grid.cursor[1], screen.COLOUR_WHITE)
            screen.refresh()
            

def switch_algorithm(screen, grid, code):
    print('algorithm switched to', code)


def execute_mode(screen, grid):
    while True:
        event = screen.get_event()

        if(event != None):
            code = event.key_code

            if code == 10:
                print('run algorithm')

            elif code >= 49 and code <= 57:
                switch_algorithm(screen, grid, code)

            else:
                edit_mode(screen, grid)


def grid_init(screen):
    grid = Grid()

    for i in range(len(grid.cells[0])):
        for j in range(len(grid.cells)):
            screen.print_at(CELL, i, j, screen.COLOUR_WHITE)

    # - start
    screen.print_at(CELL, grid.start[0], grid.start[1], screen.COLOUR_GREEN)
    # - end
    screen.print_at(CELL, grid.end[0], grid.end[1], screen.COLOUR_RED)

    screen.refresh()

    # test_codes(screen, grid)
    # edit_mode(screen, grid)
    execute_mode(screen, grid)
    

Screen.wrapper(grid_init)