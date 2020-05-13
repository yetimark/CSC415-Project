# MAIN: Run this script for the solution

from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from time import sleep

from grid import Grid
from my_algorithms import depth_first_search, breadth_first_search


REST = 0.1


def screen_print(screen, dest, color):
    screen.print_at('\u2588', dest[0], dest[1], color)



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
                prev_colour = screen.get_from(prev_cursor[0], prev_cursor[1])[1]  # --- Foreground
                
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

                elif grid.get_cell_weight(prev_cursor) > 1:
                    screen_print(screen, prev_cursor, screen.COLOUR_BLUE)

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

            # - toggle wall - (w)       FIX: A good place for a proper event handler
            elif code == 119:
                if grid.is_wall(grid.cursor):
                    # - remove wall -
                    grid.remove_wall(grid.cursor)
                    screen_print(screen, grid.cursor, screen.COLOUR_WHITE)
                else:
                    # - add wall -
                    grid.add_wall(grid.cursor)
                    screen_print(screen, grid.cursor, screen.COLOUR_BLACK)

            # - toggle weight - (q) no good reason for q
            elif code == 113:
                if grid.get_cell_weight(grid.cursor) > 1:
                    # - remove weight -
                    grid.remove_cell_weight(grid.cursor)
                    screen_print(screen, grid.cursor, screen.COLOUR_WHITE)
                else:
                    # - add weight -
                    grid.add_cell_weight(grid.cursor)
                    screen_print(screen, grid.cursor, screen.COLOUR_BLUE)

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
            

def display_algorithm(screen, algorithm):
    screen.print_at('Current Algorithm: ' + algorithm[0], 0, 22)
    screen.refresh()


def execute_mode(screen, grid):

    algorithms = {  
        49 : ['Depth First Search     ', depth_first_search],
        50 : ['Breadth First Search   ', breadth_first_search],
        51 : ['Undefined Algorithm    ', None],
        52 : ['Undefined Algorithm    ', None],
        53 : ['Undefined Algorithm    ', None],
        54 : ['Undefined Algorithm    ', None],
        55 : ['Undefined Algorithm    ', None],
        56 : ['Undefined Algorithm    ', None],
        57 : ['Undefined Algorithm    ', None]
    }
    current_algorithm = algorithms[49]
    display_algorithm(screen, current_algorithm)

    while True:
        event = screen.get_event()

        if(event != None):
            code = event.key_code

            if code == 10:
                current_algorithm[1](screen, grid)

            elif code >= 49 and code <= 57:
                current_algorithm = algorithms[code]
                display_algorithm(screen, current_algorithm)

            elif code == -1:
                # escape
                break

            else:
                edit_mode(screen, grid)


def grid_init(screen):
    grid = Grid()

    for i in range(grid.collumns):
        for j in range(grid.rows):
            screen_print(screen, (i, j), screen.COLOUR_WHITE)

    # - start
    screen_print(screen, grid.start, screen.COLOUR_GREEN)
    # - end
    screen_print(screen, grid.end, screen.COLOUR_RED)
    # - walls for when layout swapping and saving is done
    for wall in grid.walls:
        screen_print(screen, wall, screen.COLOUR_BLACK)
    # - weights for when layout swapping and saving is done
    for weight in grid.weighted:
        screen_print(screen, weighted, screen.COLOUR_BLUE)

    screen.refresh()

    # test_codes(screen, grid)
    # edit_mode(screen, grid)
    execute_mode(screen, grid)
    

Screen.wrapper(grid_init)