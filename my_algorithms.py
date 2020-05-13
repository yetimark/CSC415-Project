from asciimatics.screen import Screen
from asciimatics.event import KeyboardEvent
from time import sleep
from grid import Grid
# ---- At least for now, this file will hold all of the algorithms ----

REST = 0.01 * 1
# 258A
def screen_print(screen, dest, color):
    screen.print_at('\u2588', dest[0], dest[1], color)


# move_look (visual cursor) this is a look and it pauses for REST
def move_look(screen, dest):
    screen_print(screen, dest, screen.COLOUR_YELLOW)
    screen.refresh()
    sleep(REST)

# display puts text on the screen below the visualization
def display_info(screen, info, height):
    screen.print_at(info, 0, height)
    screen.refresh()

# show will .. show something in the visualization on the grid
def show_stack(screen, stack):
    screen_print(screen, stack, screen.COLOUR_CYAN)
    screen.refresh()

def show_closed(screen, closed):
    screen_print(screen, closed, screen.COLOUR_MAGENTA)
    screen.refresh()


def reset_screen(screen, grid):
    for i in range(grid.collumns):
        for j in range(grid.rows):
            screen_print(screen, (i, j), screen.COLOUR_WHITE)

    # - start
    screen_print(screen, grid.start, screen.COLOUR_GREEN)
    # - end
    screen_print(screen, grid.end, screen.COLOUR_RED)
    # - walls
    for wall in grid.walls:
        screen_print(screen, wall, screen.COLOUR_BLACK)
    # - refresh
    screen.refresh()


def exit_algorithm(screen, grid):
    while True:
        event = screen.get_event()

        if event != None:
            code = event.key_code
            if code == -1:
                # esc return to execute mode 
                reset_screen(screen, grid)
                break


# screen  for visualization
def get_neighbors(grid, cell):
    neighbors = []

    up = grid.get_up(cell)
    right = grid.get_right(cell)
    down = grid.get_down(cell)
    left = grid.get_left(cell)

    if up is not False and not grid.is_wall(up):
        neighbors.append(up)
    if right is not False and not grid.is_wall(right):
        neighbors.append(right)
    if down is not False and not grid.is_wall(down):
        neighbors.append(down)
    if left is not False and not grid.is_wall(left):
        neighbors.append(left)

    neighbors.reverse()
    return neighbors


def color_path_from_closed(screen, grid, closed):
    path = [grid.end]
    next_cell = closed[grid.end]

    while closed[next_cell] != None:
        path.append(next_cell)
        next_cell = closed[next_cell]

    while path:
        screen_print(screen, path.pop(), screen.COLOUR_YELLOW)
        screen.refresh()
        sleep(REST * 0.75)


def depth_first_search(screen, grid):

    # -- Top of the stack is End of the list
    stack = [grid.start]
    show_stack(screen, grid.start)

    # - closed will have values as such {(current_cell) : (last_cell)} - 
    # -- this will allow for quick look up by using the in keyword and we can trace the correct path--
    closed = {}
    last_cell = None

    while len(stack) > 0:
        cell = stack.pop()
        move_look(screen, cell)                 # --- Visuals
                

        # - Solution Found
        if cell == grid.end:
            closed[cell] = last_cell
            color_path_from_closed(screen, grid, closed)
            break # goes to exit_algorithm

        # check for neighbors
        neighbors = get_neighbors(grid, cell)
        
        # put neighbors on stack
        for neighbor in neighbors:
            if neighbor not in closed:
                stack.append(neighbor)
                show_stack(screen, neighbor)

        # put cell in closed
        closed[cell] = last_cell
        show_closed(screen, cell)
        last_cell = cell


    exit_algorithm(screen, grid)


def breadth_first_search(screen, grid):

    # -- Top of the queue is End of the list // insert(0, x) and pop()
    queue = [grid.start]
    show_stack(screen, grid.start)

    closed = {}
    last_cell = None

    while len(queue) > 0:
        cell = queue.pop()
        move_look(screen, cell)

        if cell == grid.end:
            closed[cell] = last_cell
            color_path_from_closed(screen, grid, closed)
            break

        neighbors = get_neighbors(grid, cell)

        for neighbor in neighbors:
            if neighbor not in closed:
                queue.insert(0, neighbor)
                show_stack(screen, neighbor)

                closed[neighbor] = cell
                show_closed(screen, cell)
                # display_info(screen, str(queue), 25)
                # display_info(screen, str(closed), 26)
        last_cell = cell

    exit_algorithm(screen, grid)